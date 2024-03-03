from typing import Callable as _Callable

from leads.context import ContextAssociated
from leads.dt import Device
from leads.event import SuspensionEvent
from leads.logger import L


def mark_system(device: Device, system: str, *related: str) -> None:
    if hasattr(device, "__device_system__"):
        setattr(device, "__device_system__", getattr(device, "__device_system__") + related)
    setattr(device, "__device_system__", [system, *related])


def read_marked_system(device: Device) -> list[str] | None:
    return getattr(device, "__device_system__") if hasattr(device, "__device_system__") else None


class SystemFailureTracer(ContextAssociated):
    def __init__(self) -> None:
        super().__init__()
        self.on_fail: _Callable[[Device, SuspensionEvent], None] = lambda _, __: None
        self.on_recover: _Callable[[Device, SuspensionEvent], None] = lambda _, __: None

    def fail(self, device: Device, exception: Exception) -> None:
        if not (systems := read_marked_system(device)):
            raise RuntimeWarning("No system marked for device " + str(device))
        for system in systems:
            self.on_fail(device, e := SuspensionEvent(context := self.require_context(), system, str(exception)))
            context.suspend(e)
            L.error(f"{system} error: {repr(exception)}")

    def recover(self, device: Device) -> None:
        if not (systems := read_marked_system(device)):
            raise RuntimeWarning("System not marked for device " + str(device))
        for system in systems:
            self.on_recover(device, SuspensionEvent(self._context, system, "Recovered"))
            L.info(system + " recovered")


SFT: SystemFailureTracer = SystemFailureTracer()
