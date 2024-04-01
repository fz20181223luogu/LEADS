from time import time as _time

from leads import require_config as _require_config


class PerformanceChecker(object):
    def __init__(self) -> None:
        self._refresh_rate: int = _require_config().refresh_rate
        self._fps: float = 0
        self._average_delay: float = 0
        self._last_frame: float = _time()

    def fps(self) -> float:
        return self._fps

    def record_frame(self) -> None:
        delay = (t := _time()) - self._last_frame
        self._fps = 1 / delay
        self._average_delay = (self._average_delay * (self._refresh_rate - 1) + delay) / self._refresh_rate
        self._last_frame = t

    def average_delay(self) -> float:
        return self._average_delay * 1000
