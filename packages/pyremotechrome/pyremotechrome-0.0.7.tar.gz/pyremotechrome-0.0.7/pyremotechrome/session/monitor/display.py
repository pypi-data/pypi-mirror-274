from __future__ import annotations
from io import TextIOWrapper
from pyvirtualdisplay import Display
from subprocess import Popen, STDOUT
from pyremotechrome.session.monitor.audio import Audio
from pyremotechrome.session.support.options import FFMpegOptions
from pyremotechrome.util import get_utc_timestr, Numbers


class BrowserDisplay(Display):

    width: Numbers
    height: Numbers
    scale: Numbers
    _sink_name: str
    _video_dir: str
    ffmpeg_options: FFMpegOptions
    _ffmpeg_process: Popen
    _log_dir: str
    _log_file: TextIOWrapper

    def __init__(self, width: Numbers, height: Numbers, scale: Numbers, log_dir: str, video_dir: str) -> None:
        """Initialize a monitor with display and audio output"""

        self.width = width
        self.height = height
        self.scale = scale
        self._sink_name = ""
        self._video_dir = video_dir
        self._log_dir = log_dir
        self._log_file = None
        self.ffmpeg_options = None
        self._ffmpeg_process = None

        super().__init__(
            visible=False,
            size=(int(width * scale), int(height * scale)),
            bgcolor="white",
            extra_args=["-nocursor"]
        )

    def init_audio(self, browser_pid: int) -> None:
        """Set browser's sink input to the corresponding sink device"""
        audio_manager = Audio(browser_pid)
        self._sink_name = audio_manager.get_monitor()
        del audio_manager

    def init_ffmpeg(self, ffmpeg_options: FFMpegOptions) -> None:
        self.ffmpeg_options = ffmpeg_options

    def start_capturing(self, x: Numbers, y: Numbers, width: Numbers, height: Numbers) -> None:

        """Start capturing the screen"""
        if self._ffmpeg_process is not None:
            return
        if self.ffmpeg_options is None:
            return

        width = int(width * self.scale)
        height = int(height * self.scale)

        ffmpeg_exec = self.ffmpeg_options.ffmpeg_exec
        segment_time = self.ffmpeg_options.segment_time
        fps = self.ffmpeg_options.fps
        queue_size_multiplier = self.ffmpeg_options.queue_size_multiplier
        queue_size = queue_size_multiplier * fps
        screen_id = self.env()["DISPLAY"]
        
        proc_args = [ffmpeg_exec, "-probesize", "42M"]

        proc_args.extend([
            "-video_size", f"{width}x{height}", "-framerate", str(fps), "-f", "x11grab",
            "-thread_queue_size", str(queue_size), "-i", f"{screen_id}+{x},{y}",
            "-r", str(queue_size_multiplier)
        ])

        # audio
        proc_args.extend([
            "-itsoffset", "0.3", "-f", "pulse", "-i", f"{self._sink_name}"
        ])

        # combine audio and image and separate output
        proc_args.extend([
            "-f", "hls", "-hls_time", str(segment_time), "-reset_timestamps",
            "1", "-g", str(fps * segment_time), "-sc_threshold", "0",
            "-force_key_frames",  f"expr:gte(t,n_forced*{segment_time})", "-c:v",
            "libx264", "-preset", "ultrafast", "-b:v", "160M", "-maxrate", "160M",
            "-bufsize", "80M", "-pix_fmt", "yuv420p", "-crf", "28", "-c:a",
            "aac", "-preset", "ultrafast", "-tune", "zerolatency", f"{self._video_dir}/.m3u8"
        ])

        self._log_file = open(f"{self._log_dir}/{get_utc_timestr('%d.%b.%Y__%H_%M_%S')}.log", "w")
        self._ffmpeg_process = Popen(proc_args, stdout=self._log_file, stderr=STDOUT)

    def stop_capturing(self) -> None:
        """DOCSTRING"""
        if self._ffmpeg_process is not None:
            self._ffmpeg_process.terminate()
            self._ffmpeg_process.wait()
            self._ffmpeg_process = None
            self._log_file.close()

    def restart_capturing(self, x: Numbers, y: Numbers, width: Numbers, height: Numbers) -> None:
        """DOCSTRING"""
        if self._ffmpeg_process is not None:
            self.stop_capturing()
            self.start_capturing(x, y, width, height)

    def __del__(self) -> None:
        self.stop_capturing()
        super().stop()
        self._log_file.close()
