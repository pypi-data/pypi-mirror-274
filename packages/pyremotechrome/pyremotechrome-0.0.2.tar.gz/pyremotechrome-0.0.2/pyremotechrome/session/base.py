from __future__ import annotations
from re import search
from requests import get as requests_get
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionBuilder
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from pyremotechrome.session.monitor.display import BrowserDisplay
from pyremotechrome.session.support.options import FFMpegOptions
from pyremotechrome.session.support.common import Directory
from pyremotechrome.session.support.common import Info
from pyremotechrome.session.support.common import Vector
from pyremotechrome.util import get_absolute_path
from pyremotechrome.util import Numbers


class Base(webdriver.Chrome):

    _id: str
    _cursor: Vector
    _position: Vector
    _border_width: Vector
    _scale: Numbers
    _data_dir: Directory
    _default_url: str
    display: BrowserDisplay
    new_handles: list[str]
    special_handles: list[str]
    info: Info
    url_rules: list[str]

    def __init__(
        self,
        id: str,
        scale: Numbers,
        data_dir: str,
        default_url: str,
        size: Vector,
        screen_size: Vector,
        wave_url: str,
        user_agent: str,
        webdriver_exec: str,
        ffmpeg_options: FFMpegOptions = FFMpegOptions(),
        url_rules: list[str] = []
    ) -> None:

        """Initialize a chrome with video capturing enabled"""
        if id == "":
            raise ValueError()

        url = wave_url.split("/")
        url.pop()
        try:
            requests_get("/".join(url), timeout=60)
        except Exception:
            raise Exception("SERVER_NO_RESPONSE")

        self._id = id
        self.info = Info()
        self._cursor = Vector(0, 0)
        self._position = Vector(0, 0)
        self._scale = scale
        self._data_dir = Directory(data_dir)
        self._default_url = default_url
        self.new_handles = []
        self.special_handles = []
        self.url_rules = url_rules

        _, log_dir = self._data_dir.set_dir("log", "log/ffmpeg")
        _, video_dir = self._data_dir.set_dir("video", "video")
        screen_width, screen_height = screen_size()
        screen_width = int(screen_width * self._scale)
        screen_height = int(screen_height * self._scale)
        self.display = BrowserDisplay(screen_width, screen_height, scale, log_dir, video_dir)
        self.display.start()

        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"--user-agent={user_agent}")
        options.add_argument("--disable-extensions")

        _, download_dir = self._data_dir.set_dir("download_dir", "downloads")

        prefs = {
            "download.prompt_for_download": False,
            "download.default_directory": download_dir,
            "download.directory_upgrade": True,
            "profile.default_content_settings.popups": 0,
        }

        options.add_experimental_option('prefs', prefs)
        options.add_experimental_option("detach", True)
        service = Service(executable_path=webdriver_exec)
        super().__init__(options=options,service=service)
        
        bw, bh = self.execute_script("""
            var w=window;
            return [
                w.outerWidth - w.innerWidth,
                w.outerHeight - w.innerHeight
            ];
        """)
        self._border_width = Vector(bw, bh)
        
        width, height = size()
        self.set_window_size(width, height)
        self.set_window_position(0, 0)
        self.set_page_load_timeout(60)
        self.zoom()

        self.nav(wave_url)
        self.left_click()
        self.execute_script("document.getElementById('loop_player').play();")
        self.special_handles.append(self.get_current_window())

        self.set_current_window(self.open_new_tab())
        self.display.init_audio(self.service.process.pid)
        self.display.init_ffmpeg(ffmpeg_options)
        self.display.start_capturing(bw, bh, width, height)

    # Zoom
    def zoom(self) -> None:
        self.get("chrome://settings/")
        self.execute_script("chrome.settingsPrivate.setDefaultZoom(arguments[0]);", self._scale)
        self.get(self._default_url)

    # Window rect
    def get_current_html_rect(self) -> Vector:
        position = self.get_window_position()
        x, y = position["x"], position["y"]
        bw, bh = self._border_width()
        width, height = self.get_window_raw_size()
        return Vector(x, y, bw, bh, width, height)
    
    def get_window_border_size(self) -> tuple[int, int]:
        """DOCSTRING"""
        return self._border_width()

    def get_window_raw_size(self) -> tuple[int, int]:
        """Return window actual size"""
        width, height = self.execute_script("""
            var w=window;
            return [w.innerWidth, w.innerHeight];
        """)
        return width, height

    def get_window_size(self) -> tuple[Numbers, Numbers]:
        """Return window display size"""
        width, height = self.get_window_raw_size()
        return width / self._scale, height / self._scale

    def set_window_size(self, width: Numbers, height: Numbers) -> None:
        """DOCSTRING"""
        x, y, bw, bh, _, _ = self.get_current_html_rect()()
        width = int(width * self._scale)
        height = int(height * self._scale)
        super().set_window_size(width + bw, height + bh)
        self.display.restart_capturing(x + bw, y + bh, width, height)

    def set_window_position(self, x: Numbers, y: Numbers) -> dict:
        """DOCSTRING"""
        _, _, bw, bh, width, height = self.get_current_html_rect()()
        x = int(x * self._scale)
        y = int(y * self._scale)
        res = super().set_window_position(x, y)
        self.display.restart_capturing(x + bw, y + bh, width, height)
        return res

    # Window handle
    def get_current_window(self) -> str:
        """Return current window handle"""
        curr_handle = self.current_window_handle
        if curr_handle not in self.window_handles:
            return ""

        return curr_handle

    def set_current_window(self, window_handle: str) -> None:
        """
        Switch to tab at the specified index.
        Raise IndexError if tab_index out of range

        Preconditions:
            - window_handle in self.window_handles
        """

        if window_handle not in self.window_handles:
            raise ValueError()

        old = self.get_current_html_rect()
        if self.get_current_window() != window_handle:
            self.switch_to.window(window_handle)
            new = self.get_current_html_rect()
            if new != old:
                x, y, bw, bh, w, h = new()
                self.display.restart_capturing(x + bw, y + bh, w, h)

    def open_new_tab(self) -> str:
        """Open a new tab and focus"""
        self.switch_to.new_window('tab')
        return self.current_window_handle

    def close_window(self) -> None:
        """
        Close the tab at the specified tab_index

        Preconditions:
            - window_handle in self.window_handles
        """

        if len(self.window_handles) > 1:
            super().close()
        else:
            super().get(self._default_url)

    def quit(self, clear_cache: bool = False) -> None:
        """Quit webdriver"""
        del self.display

        if clear_cache:
            self._data_dir.remove_dir()

        super().quit()

    # Navigation
    def nav(self, url: str) -> list[str]:
        for rule in self.url_rules:
            if search(rule, url) is not None:
                self.mute()
                super().get(url)
                return self.new_handles

    # Mouse Emulator
    def get_cursor_position(self) -> tuple[int, int]:
        """Return current mouse position"""
        return self._cursor()

    def mouse_move(self, x: int, y: int) -> None:
        """Set cursor position"""

        action = ActionBuilder(self)
        action.pointer_action.move_to_location(
            int(x * self._scale),
            int(y * self._scale)
        )
        action.perform()
        self._cursor = Vector(x, y)

    def mouse_hold(self) -> None:
        """Mouse hold"""
        action = ActionBuilder(self)
        action.pointer_action.click_and_hold()
        action.perform()

    def mouse_release(self) -> None:
        """Mouse release"""
        action = ActionBuilder(self)
        action.pointer_action.release()
        action.perform()

    def left_click(self) -> None:
        """Emulate a left click of a mouse"""
        action = ActionChains(self)
        action.click()
        action.perform()

    def right_click(self) -> None:
        """Emulate a right click of a mouse"""

        action = ActionChains(self)
        action.context_click()
        action.perform()

    def double_click(self) -> None:
        """Emulate double click of a mouse"""

        action = ActionChains(self)
        action.double_click()
        action.perform()

    def scroll(self, delta_x: int, delta_y: int) -> None:
        """Emulate mouse scroll"""

        action = ActionChains(self)
        action.scroll_by_amount(
            int(delta_x * self._scale),
            int(delta_y * self._scale)
        )
        action.perform()
    
    # Keyboard Emulator
    def key(self, keys: tuple[str, str]) -> None:
        """Emulate pressing a key"""
        action = ActionChains(self)
        action_mapping = {"d": action.key_down, "u": action.key_up, "": action.send_keys}

        if keys[0] not in action_mapping:
            return

        action_mapping[keys[0]](keys[1])
        action.perform()

    def key_seq(self, key_seqs: list[tuple[str, str]]) -> None:
        """Emulate pressing a sequence of keys"""
        for keys in key_seqs:
            self.key(keys)

    # Copy and Paste
    def _create_clipboard(self) -> WebElement:
        """Create an invisble text_area"""
        textarea_id = f"mega-clipboard-{self._id}-{self.get_current_window_handle()}"
        css_selector = f"textarea#{textarea_id}"
        try:
            self.select(css_selector)
        except NoSuchElementException:
            self.execute_script(f"""
                input = document.createElement('textarea');
                input.style.width = '0px';
                input.style.height = '0px';
                input.style.opacity = '0';
                input.id = '{textarea_id}';
                input.tabIndex = -1;
                document.body.append(input);
            """)
        return self.select(css_selector)

    def _get_copy(self) -> str:
        """DOCSTRING"""
        paste_key = [["d", Keys.CONTROL], ["", "v"], ["u", Keys.CONTROL]]
        clipboard = self._create_clipboard()
        clipboard.click()
        clipboard.clear()
        self.key_seq(paste_key)
        return clipboard.get_attribute("value")

    def cut(self) -> str:
        """Emulate cut"""
        copy_key = [["d", Keys.CONTROL], ["", "x"], ["u", Keys.CONTROL]]
        self.key_seq(copy_key)
        return self._get_copy()

    def copy(self) -> str:
        """Emulate copy"""
        copy_key = [["d", Keys.CONTROL], ["", "c"], ["u", Keys.CONTROL]]
        self.key_seq(copy_key)
        return self._get_copy()

    def paste(self, value: str) -> None:
        """Emulate paste"""
        super().key(["", value])

    # Capture Screenshot
    def capture_screenshot(self) -> str:
        """
        Capture screenshot and save to the file path
        """
        if self.get_current_window() in self.special_handles:
            return ""

        display_dir, save_dir = self._data_dir.set_dir('current_window', f"cache/{self.get_current_window()}")
        display_path = f"{display_dir}/screenshot.png"
        save_path = f"{save_dir}/screenshot.png"
        self.get_screenshot_as_file(save_path)
        return display_path

    # DOM Element
    def select(self, css_selector: str) -> WebElement:
        """Select the specified html element"""
        return self.find_element(By.CSS_SELECTOR, css_selector)

    # Get Pid
    def get_pid(self) -> None:
        return self.service.process.pid

    # Retrieve Other Information
    def get_current_url(self) -> str:
        """DOCSTRING"""
        return self.current_url

    def get_current_title(self) -> str:
        """DOCSTRING"""
        title = self.execute_script("return document.title;")
        if title == "":
            try:
                title = self.select("title").get_attribute("innerText")
            except Exception:
                title = self.current_url

        return title

    def get_current_icon(self) -> str:
        """DOCSTRING"""
        display_dir, save_dir = self._data_dir.set_dir('current_window', f"cache/{self.get_current_window}")
        display_path = f"{display_dir}/favicon.ico"
        save_path = f"{save_dir}/favicon.ico"
        try:
            # Try default favicon location
            icon_url = get_absolute_path(self.current_url, "favicon.ico")
            img_data = requests_get(icon_url).content
            with open(save_path, "wb") as handler:
                handler.write(img_data)

            return display_path
        except Exception:
            try:
                # Try favicon location in html
                icon_url = self.select("link[rel~='icon']").get_attribute("src")
                icon_url = get_absolute_path(self.current_url, icon_url)
                img_data = requests_get(icon_url).content
                with open(save_path, "wb") as handler:
                    handler.write(img_data)

                return display_path
            except Exception:
                # No favicon is found
                return ""

    def update_and_get_info(self) -> dict[str, dict[str, str]]:
        """reset and get title, icon and url"""
        self.info.update("title", self.get_current_title())
        self.info.update("icon", self.get_current_icon())
        self.info.update("url", self.get_current_url())
        return self.info.to_dict()

    # Other methods
    def mute(self) -> None:
        """DOCSTRING"""
        try:
            self.execute_script("""
                var video_doms = document.getElementsByTagName('video');
                var audio_doms = document.getElementsByTagName('video');
                for(var i=0;i<video_doms.length;i++){
                    video_doms[i].muted = true;
                }
                for(var i=0;i<audio_doms.length;i++){
                    audio_doms[i].muted = true;
                }
            """)
        except Exception:
            pass
    
    def hide_scrollbar(self) -> None:
        """DOCSTRING"""
        try:
            self.execute_script("""
                if (document.styleSheets.length > 0){
                    var sheet = document.styleSheets[0];
                    var len = sheet.cssRules.length;
                    sheet.insertRule('*{}', len);
                    var rule = sheet.cssRules[len];
                    rule.selectorText = 'body::-webkit-scrollbar';
                    rule.style.display = 'none';
                }
            """)
        except Exception:
            pass