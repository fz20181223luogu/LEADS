from typing import Sequence as _Sequence, Any as _Any, SupportsFloat as _SupportsFloat

from leads.data_persistence.analyzer import utils as _utils
from .._computational import array as _array


class DynamicProcessor(object):
    def __init__(self, data_seq: _Sequence[dict[str, _Any]]) -> None:
        self._data_seq: _Sequence[dict[str, _Any]] = data_seq
        self._origin_x: float = 0
        self._origin_y: float = 0

    def to_tensor(self, channels: tuple[str, ...] = ("time", "speed", "latitude", "longitude")) -> _array:
        r = []
        for row in self._data_seq:
            r_row = []
            for channel in channels:
                d = row[channel]
                if not isinstance(d, _SupportsFloat):
                    raise TypeError(f"{d} ({channel}) is not a float and cannot be converted to a float")
                if getattr(_utils, f"{channel}_invalid", lambda _: False)(d):
                    raise ValueError(f"Invalid value for {channel} ({d}) at row {len(r)}")
                r_row.append(d)
            r.append(r_row)
        return _array(r)
