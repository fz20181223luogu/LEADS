from leads import *
from time import time
from leads_dashboard import *
from datetime import datetime
from keyboard import add_hotkey
from dearpygui import dearpygui as dpg

from .__version__ import __version__


class CustomRuntimeData(RuntimeData):
    m2_mode: int = 0


def main(main_controller: Controller,
         srw_mode: bool = True,
         analysis_rate: float = .01,
         update_rate: float = .25) -> int:
    context = Leads(srw_mode=srw_mode)
    rd = CustomRuntimeData()

    class CustomListener(EventListener):
        def on_update(self, e: UpdateEvent):
            duration = int(time()) - rd.start_time
            dpg.set_value("info",
                          "LEADS for VeC\n"
                          f"VERSION {__version__.upper()}\n\n"
                          f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                          f"{duration // 60} MIN "
                          f"{duration % 60} SEC\n\n"
                          f"{'SRW MODE' if srw_mode else 'DRW MODE'}\n"
                          f"ANALYSIS RATE: {int(1 / analysis_rate)} TPS\n"
                          f"UPDATE RATE: {int(1 / update_rate)} TPS")
            dpg.set_item_label("speed", f"{context.data().front_wheel_speed}")

    def switch_dtcs():
        context.set_dtcs(not (dtcs_enabled := context.is_dtcs_enabled()))
        dpg.set_item_label("dtcs", f"DTCS {'OFF' if dtcs_enabled else 'ON'}")

    add_hotkey("1", switch_dtcs)

    def switch_abs():
        context.set_abs(not (abs_enabled := context.is_abs_enabled()))
        dpg.set_item_label("abs", f"ABS {'OFF' if abs_enabled else 'ON'}")

    add_hotkey("2", switch_abs)

    def switch_ebi():
        context.set_ebi(not (ebi_enabled := context.is_ebi_enabled()))
        dpg.set_item_label("ebi", f"EBI {'OFF' if ebi_enabled else 'ON'}")

    add_hotkey("3", switch_ebi)

    def switch_atbs():
        context.set_atbs(not (atbs_enabled := context.is_atbs_enabled()))
        dpg.set_item_label("atbs", f"ATBS {'OFF' if atbs_enabled else 'ON'}")

    add_hotkey("4", switch_atbs)

    def render():
        with dpg.table(header_row=False):
            dpg.add_table_column()
            dpg.add_table_column()
            dpg.add_table_column()
            with dpg.table_row():
                dpg.bind_item_font(dpg.add_text("", tag="info"), BODY2)
                dpg.bind_item_font(dpg.add_button(label="0", tag="speed", width=-1, height=140), H1)
                dpg.bind_item_font(m2 := dpg.add_button(label="0.0v", tag="voltage", width=-1, height=140), H1)

                def switch_m2_mode():
                    rd.m2_mode = (rd.m2_mode + 1) % 3
                    if rd.m2_mode == 0:
                        dpg.set_item_font(m2, H1)
                        dpg.set_item_label(m2, "0.0v")
                    elif rd.m2_mode == 1:
                        dpg.set_item_font(m2, BODY)
                        dpg.set_item_label(m2, "LAP TIME\n\nLAP1 10s\nLAP2 12s")
                    else:
                        dpg.set_item_font(m2, BODY)
                        dpg.set_item_label(m2, "G Force")

                dpg.set_item_callback(m2, switch_m2_mode)
        with dpg.table(header_row=False):
            dpg.add_table_column()
            dpg.add_table_column()
            dpg.add_table_column()
            dpg.add_table_column()
            with dpg.table_row():
                dpg.bind_item_font(dpg.add_button(label="DTCS ON", tag="dtcs", width=-1, callback=switch_dtcs), H2)
                dpg.bind_item_font(dpg.add_button(label="ABS ON", tag="abs", width=-1, callback=switch_abs), H2)
                dpg.bind_item_font(dpg.add_button(label="EBI ON", tag="ebi", width=-1, callback=switch_ebi), H2)
                dpg.bind_item_font(dpg.add_button(label="ATBS ON", tag="atbs", width=-1, callback=switch_atbs), H2)

    context.set_event_listener(CustomListener())
    start(render, context, main_controller, analysis_rate, update_rate, rd)
    return 0
