from pyremotechrome.util import Numbers


class FFMpeg():
    
    ffmpeg_exec: str
    segment_time: Numbers
    fps: Numbers
    queue_size_multiplier: Numbers

    def __init__(self, ffmpeg_exec: str = "ffmpeg", segment_time: Numbers = 1, fps: int = 10, queue_size_multiplier: int = 8) -> None:
        """DOCSTRING"""
        self.ffmpeg_exec = ffmpeg_exec
        self.segment_time = segment_time
        self.fps = fps
        self.queue_size_multiplier = queue_size_multiplier
