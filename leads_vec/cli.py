from leads import *
from leads_dashboard import *
from datetime import datetime
from dearpygui import dearpygui as dpg

from .__version__ import __version__


def render():
    with dpg.table(header_row=False):
        dpg.add_table_column()
        dpg.add_table_column()
        dpg.add_table_column()
        with dpg.table_row():
            dpg.bind_item_font(dpg.add_text("", tag="time"), BODY2)
            dpg.bind_item_font(dpg.add_button(label="", tag="speed", width=-1, height=200), H1)


def main(main_controller: Controller,
         srw_mode: bool = True,
         analysis_rate: float = .01,
         update_rate: float = .5) -> int:
    context = Leads(srw_mode=srw_mode)
    rd = RuntimeData()

    class CustomListener(EventListener):
        def on_update(self, e: UpdateEvent):
            dpg.set_value("time", "LEADS for VeC\n"
                                  f"VERSION {__version__.upper()}\n\n"
                                  f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                                  f"{int(rd.frame_counter * analysis_rate / 60)} MIN {int((rd.frame_counter % (60 / analysis_rate)) * analysis_rate)} SEC\n\n"
                                  f"{'SRW MODE' if srw_mode else 'DRW MODE'}\n"
                                  f"ANALYSIS RATE: {int(1 / analysis_rate)} TPS")
            dpg.set_item_label("speed", f"{context.data().front_wheel_speed}")

    context.set_event_listener(CustomListener())
    start(render, context, main_controller, analysis_rate, update_rate, rd)
    return 0
