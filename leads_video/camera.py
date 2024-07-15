from typing import override as _override

from PIL.Image import fromarray as _fromarray, Image as _Image
from cv2 import VideoCapture as _VideoCapture, cvtColor as _cvtColor, COLOR_BGR2RGB as _COLOR_BGR2RGB
from numpy import ndarray as _ndarray, pad as _pad, array as _array

from leads import Device as _Device, ShadowDevice as _ShadowDevice
from leads_video.utils import base64_encode


class Camera(_Device):
    def __init__(self, port: int, resolution: tuple[int, int] | None = None) -> None:
        super().__init__(port)
        self._resolution: tuple[int, int] | None = resolution
        self._video_capture: _VideoCapture | None = None

    @_override
    def initialize(self, *parent_tags: str) -> None:
        super().initialize(*parent_tags)
        self._video_capture = _VideoCapture(self._pins[0])

    @_override
    def write(self, payload: tuple[int, int] | None) -> None:
        """
        :param payload: [width, height]
        """
        self._resolution = payload

    def transform(self, x: _ndarray) -> _ndarray:
        height, width = x.shape[:-1]
        resolution_width, resolution_height = self._resolution
        target_ratio = resolution_height / resolution_width
        target_height = int(target_ratio * width)
        pad_left, pad_right, pad_top, pad_bottom = 0, 0, 0, 0
        if height > target_height:
            target_width = int(height / target_ratio)
            pad_left = (target_width - width) // 2
            pad_right = target_width - width - pad_left
        else:
            pad_top = (target_height - height) // 2
            pad_bottom = target_height - height - pad_top
        return _array(_fromarray(_pad(x, ((pad_left, pad_right), (pad_top, pad_bottom), (0, 0)))).resize(
            self._resolution))

    @_override
    def read(self) -> _ndarray | None:
        ret, frame = self._video_capture.read()
        return _cvtColor(self.transform(frame) if self._resolution else frame, _COLOR_BGR2RGB).transpose(
            2, 0, 1) if ret else None

    def read_numpy(self) -> _ndarray | None:
        return self.read()

    def read_pil(self) -> _Image | None:
        return None if (frame := self.read_numpy()) is None else _fromarray(frame)

    @_override
    def close(self) -> None:
        self._video_capture.release()


class Base64Camera(Camera, _ShadowDevice):
    def __init__(self, port: int, resolution: tuple[int, int] | None = None) -> None:
        Camera.__init__(self, port, resolution)
        _ShadowDevice.__init__(self, port)
        self._original: _ndarray | None = None
        self._base64: str = ""

    @_override
    def loop(self) -> None:
        if self._video_capture:
            self._original = super().read()
            self._base64 = base64_encode(self._original)

    @_override
    def read(self) -> str:
        return self._base64

    @_override
    def read_numpy(self) -> _ndarray | None:
        return self._original
