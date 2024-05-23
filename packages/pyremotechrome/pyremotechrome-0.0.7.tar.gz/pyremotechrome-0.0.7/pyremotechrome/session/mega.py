from selenium.webdriver.support.events import EventFiringWebDriver
from selenium.webdriver.support.events import AbstractEventListener
from pyremotechrome.session import Base
from pyremotechrome.session.support.options import FFMpegOptions
from pyremotechrome.session.support.common import Vector
from pyremotechrome.util import Numbers


class CustomEventListeners(AbstractEventListener):
    """DOCSTRING"""

    before: set[str]

    def __init__(self) -> None:
        self.before = set()
        super().__init__()

    def before_navigate_to(self, url: str, driver: Base) -> None:
        self.before = set(driver.window_handles)

    def after_navigate_to(self, url: str, driver: Base) -> None:
        driver.hide_scrollbar(driver)
        driver.new_handles = list(set(driver.window_handles).difference(self.old_handles))

    def after_navigate_back(self, driver: Base) -> None:
        driver.hide_scrollbar(driver)

    def after_navigate_forward(self, driver: Base) -> None:
        driver.hide_scrollbar()


class MegaBase(EventFiringWebDriver):

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

        """DOCSTRING"""
        super().__init__(
            Base(
                id,
                scale,
                data_dir,
                default_url,
                size,
                screen_size,
                wave_url,
                user_agent,
                webdriver_exec,
                ffmpeg_options,
                url_rules
            ),
            CustomEventListeners()
        )

    def quit(self, clear_cache: bool = False) -> None:
        """Quit the browser"""
        super().wrapped_driver.quit(clear_cache)
