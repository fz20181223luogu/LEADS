from tkinter import Misc as _Misc, ARC as _ARC
from typing import override as _override, Literal as _Literal

from customtkinter import DoubleVar as _DoubleVar
from numpy import pi as _pi, sin as _sin, cos as _cos

from leads import require_config as _require_config
from leads_gui.prototype import parse_color, CanvasBased, TextBased
from leads_gui.types import Font as _Font, Color as _Color


class Speedometer(TextBased):
    def __init__(self,
                 master: _Misc,
                 theme_key: str = "CTkButton",
                 width: float = 0,
                 height: float = 0,
                 variable: _DoubleVar | None = None,
                 style: _Literal[0, 1, 2] = 0,
                 next_style_on_click: bool = True,
                 maximum: float = 200,
                 font: tuple[_Font, _Font, _Font] | None = None,
                 text_color: _Color | None = None,
                 fg_color: _Color | None = None,
                 hover_color: _Color | None = None,
                 bg_color: _Color | None = None,
                 corner_radius: int | None = None) -> None:
        super().__init__(master, theme_key, width, height, None, text_color, fg_color, hover_color, bg_color,
                         corner_radius, next_style_on_click,
                         lambda _: self.next_style() if next_style_on_click else lambda _: None)
        self._variable: _DoubleVar = variable if variable else _DoubleVar(master)
        self._style: _Literal[0, 1, 2] = style
        self._maximum: float = maximum
        cfg = _require_config()
        self._font: tuple[_Font, _Font, _Font] = font if font else (("Arial", cfg.font_size_x_large),
                                                                    ("Arial", cfg.font_size_large),
                                                                    ("Arial", cfg.font_size_small))
        self._variable.trace_add("write", lambda _, __, ___: self.render())

    def next_style(self) -> None:
        self._style = (self._style + 1) % 3

    def style(self, style: _Literal[0, 1, 2] | None) -> _Literal[0, 1, 2] | None:
        if style is None:
            return self._style
        self._style = style

    @_override
    def raw_renderer(self, canvas: CanvasBased) -> None:
        canvas.clear()
        v = self._variable.get()
        w, h = canvas.winfo_width(), canvas.winfo_height()
        hc, vc = w * .5, h * .5
        font = self._font[self._style]
        canvas.configure(height=20)
        if (target_font_size := h - 28 if self._style == 0 else h - 48) < font[1]:
            font = (font[0], target_font_size)
        canvas.draw_fg(canvas)
        if self._style > 0:
            r = min(hc, vc) + 10
            x, y = hc, vc + r * .25
            p = min(v / self._maximum, 1)
            color = parse_color(("#" + str(hex(int(0xbf - p * 0xbf)))[2:] * 3,
                                 "#" + str(hex(int(0x4d + 0xb2 * p)))[2:] * 3))
            canvas._ids.append(canvas.create_arc(x - r, y - r, x + r, y + r, start=-30, extent=240, width=4,
                                                 style=_ARC, outline=color))
            canvas._ids.append(canvas.create_text(x, y - r * .6, text="KM / H", fill="gray", font=("Arial", 8)))
            canvas._ids.append(canvas.create_text(x - r * .7, y + r * .4, text="0", fill="gray", font=("Arial", 8)))
            canvas._ids.append(canvas.create_text(x + r * .7, y + r * .4, text=str(self._maximum), fill="gray",
                                                  font=("Arial", 8)))
            rad = p * 4 * _pi / 3 - _pi / 6
            canvas._ids.append(canvas.create_line(*(x, y) if self._style == 2 else (x - _cos(rad) * (r - 8),
                                                                                    y - _sin(rad) * (r - 8)),
                                                  x - _cos(rad) * (r + 8), y - _sin(rad) * (r + 8), width=4,
                                                  fill=color))
            canvas._ids.append(canvas.create_text(x, y * .95 if self._style == 1 else y + (r - font[1]) * .5,
                                                  text=str(int(v)), fill=self._text_color, font=font))
        else:
            canvas._ids.append(canvas.create_text(hc, vc, text=str(int(v)), fill=self._text_color, font=font))