from abc import ABCMeta as _ABCMeta
from json import dumps as _dumps
from time import time as _time


class DataContainer(object, metaclass=_ABCMeta):
    def __init__(self, *speeds: int | float) -> None:
        self._time_stamp: int = int(_time() * 1000)
        self.speed: int | float = min(speeds)

    def __str__(self) -> str:
        return _dumps(self.to_dict())

    def reset_time_stamp(self) -> None:
        """
        Reset the data's time stamp to now.
        """
        self._time_stamp = int(_time() * 1000)

    def get_time_stamp(self) -> int:
        """
        Get the data's time stamp.
        :return: the time stamp (ms)
        """
        return self._time_stamp

    def to_dict(self) -> dict:
        """
        Convert the data into a dictionary.
        :return: a dictionary that contains all custom attributes of the container
        """
        attributes = dir(self)
        r = {"t": self._time_stamp}
        for n in attributes:
            if n.startswith("_"):
                continue
            v = self.__getattribute__(n)
            if type(v) in (int, float, str):
                r[n] = v
        return r

    def encode(self) -> bytes:
        """
        Encode the data into bytes for network transaction purposes.
        :return: JSON in bytes
        """
        return str(self).encode()


class SRWDataContainer(DataContainer):
    def __init__(self,
                 front_wheel_speed: int | float = 0,
                 rear_wheel_speed: int | float = 0,
                 ) -> None:
        super().__init__(front_wheel_speed, rear_wheel_speed)
        self.front_wheel_speed: int | float = front_wheel_speed
        self.rear_wheel_speed: int | float = rear_wheel_speed


class DRWDataContainer(DataContainer):
    def __init__(self,
                 front_wheel_speed: int | float = 0,
                 left_rear_wheel_speed: int | float = 0,
                 right_rear_wheel_speed: int | float = 0,
                 ) -> None:
        super().__init__(front_wheel_speed, left_rear_wheel_speed, left_rear_wheel_speed)
        self.front_wheel_speed: int | float = front_wheel_speed
        self.left_rear_wheel_speed: int | float = left_rear_wheel_speed
        self.right_rear_wheel_speed: int | float = right_rear_wheel_speed
