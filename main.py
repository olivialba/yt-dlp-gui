import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
from src.utils import *
import os


dpg.create_context()
dpg.create_viewport(title='Request Checker', small_icon='src/img/small.ico', large_icon='src/img/large.ico', 
                    height=700, width=1000)

with dpg.font_registry():
    default_font = dpg.add_font("src/font/Roboto-Regular.ttf", 20)
    dpg.add_font("src/font/Roboto-Medium.ttf", 20)
dpg.bind_font(default_font)

# MAIN WINDOW
with dpg.window(tag="main_window"):
    with dpg.table(header_row=False, borders_innerH=True, borders_innerV=True, 
                   borders_outerH=True, borders_outerV=True):
        dpg.add_table_column()
        
        # First ROW
        with dpg.table_row():
            with dpg.table(header_row=False, borders_innerH=True, borders_innerV=False, 
                        borders_outerH=False, borders_outerV=False):
                dpg.add_table_column()
                dpg.add_table_column(width_fixed=True, init_width_or_weight=550)
                dpg.add_table_column()
                with dpg.table_row():
                    space(0) # Empty first Column
                    with dpg.group(): # Second Column
                        with dpg.group(indent=10):
                            space(10)
                            with dpg.group(horizontal=True):
                                dpg.add_text("VIDEO LINK: ")
                                dpg.add_input_text(hint='Input Request URL', tag='request_url', width=-1)

                        space(20)
                        dpg.add_button(label='Check Link For Video', tag='send_request_button', callback=send_request, width=-1, height=30)
                        space(20)

        # Second ROW
        with dpg.table_row():
            with dpg.table(header_row=False, borders_innerH=False, borders_innerV=True, 
                        borders_outerH=False, borders_outerV=False, resizable=False):
                dpg.add_table_column()
                dpg.add_table_column(width_fixed=True, init_width_or_weight=600)
                dpg.add_table_column()
                with dpg.table_row():
                    space(0)
                    with dpg.group():
                        dpg.add_text('', tag='request_response', wrap=565, indent=20)
                        dpg.add_text('', tag='request_download_progress', show=False)
                        dpg.add_text('', tag='request_download_speed', show=False)
                        dpg.add_text('', tag='request_download_elapsed', show=False)
                        setLog("Inserisci un YouTube link per iniziare..")
                with dpg.table_row():
                    pass

                        
        # Third Row
        with dpg.table_row():
            with dpg.table(header_row=False, borders_innerH=False, borders_innerV=True, 
                        borders_outerH=False, borders_outerV=False):
                dpg.add_table_column()
                dpg.add_table_column(width_fixed=True, init_width_or_weight=800)
                dpg.add_table_column()
                with dpg.table_row():
                    space(0) # Empty first Column
                    with dpg.group(): # Second Column
                        with dpg.group(indent=10):
                            space(15)
                            dpg.add_text("", tag='request_title', wrap=700, show=False)
                            dpg.add_text("", tag='request_url_info', show=False)
                            dpg.add_text("", tag='request_author', wrap=200, show=False)
                            dpg.add_text("", tag='request_length', wrap=150, show=False)
                            with dpg.group(tag="video_info_group", horizontal=True):
                                with dpg.group(tag='request_quality_group'):
                                    dpg.add_text('Resolution', tag='request_quality_title', show=False)
                                    dpg.add_radio_button([], tag='request_quality', show=False)
                            space(5)
                            dpg.add_button(label='Download', tag='request_download_video', callback=downloadVideo,
                                           width=-1, height=40, show=False)
                            space(5)
                            
                
                
#demo.show_demo()

# Setup
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main_window", True)
dpg.start_dearpygui()
dpg.destroy_context()