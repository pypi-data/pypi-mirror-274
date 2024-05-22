import os

from typing import Union
from copy import deepcopy
from simba.mixins.pop_up_mixin import PopUpMixin
from simba.ui.tkinter_functions import CreateLabelFrameWithIcon, FileSelect, FolderSelect, DropDownMenu, Entry_Box
from simba.utils.enums import Keys, Links, Options
from simba.utils.checks import check_file_exist_and_readable, check_if_dir_exists, check_str
from simba.video_processors.video_processing import watermark_video, superimpose_elapsed_time, superimpose_video_progressbar, superimpose_overlay_video, superimpose_video_names, superimpose_freetext, roi_blurbox
from simba.utils.lookups import get_color_dict
from simba.utils.read_write import get_video_meta_data
import threading
from tkinter import *
import numpy as np
from simba.utils.errors import InvalidInputError
from simba.utils.read_write import get_video_meta_data, str_2_bool
from simba.utils.enums import Formats
from simba.video_processors.video_processing import video_bg_subtraction, video_bg_substraction_mp

class BackgroundRemoverPopUp(PopUpMixin):
    def __init__(self):
        PopUpMixin.__init__(self, title="REMOVE BACKGROUND IN VIDEOS")
        self.clr_dict = get_color_dict()
        settings_frm = CreateLabelFrameWithIcon(parent=self.main_frm, header="SETTINGS", icon_name=Keys.DOCUMENTATION.value, icon_link=Links.VIDEO_TOOLS.value)
        self.video_path = FileSelect(settings_frm, "VIDEO PATH:", title="Select a video file", file_types=[("VIDEO", Options.ALL_VIDEO_FORMAT_OPTIONS.value)], lblwidth=30)
        self.bg_video_path = FileSelect(settings_frm, "BACKGROUND REFERENCE VIDEO PATH:", title="Select a video file", file_types=[("VIDEO", Options.ALL_VIDEO_FORMAT_OPTIONS.value)], lblwidth=30)
        self.bg_clr_dropdown = DropDownMenu(settings_frm, "BACKGROUND COLOR:", list(self.clr_dict.keys()), labelwidth=30)
        self.fg_clr_dropdown = DropDownMenu(settings_frm, "FOREGROUND COLOR:", list(self.clr_dict.keys()), labelwidth=30)
        self.slice_frm = LabelFrame(self.main_frm, text='SLICE', font=Formats.LABELFRAME_HEADER_FORMAT.value)
        self.bg_start_time_eb = Entry_Box(parent=self.slice_frm, labelwidth=30, entry_box_width=15, fileDescription='BACKGROUND VIDEO START TIME:')
        self.bg_end_time_eb = Entry_Box(parent=self.slice_frm, labelwidth=30, entry_box_width=15, fileDescription='BACKGROUND VIDEO END TIME:')
        self.bg_start_frm_eb = Entry_Box(parent=self.slice_frm, labelwidth=30, entry_box_width=15, fileDescription='BACKGROUND VIDEO START FRAME:', validation='numeric')
        self.bg_end_frm_eb = Entry_Box(parent=self.slice_frm, labelwidth=30, entry_box_width=15, fileDescription='BACKGROUND VIDEO END FRAME:', validation='numeric')
        self.slice_frm.grid(row=1, column=0, sticky=NW)

        self.bg_slice_setting = DropDownMenu(settings_frm, "BACKGROUND REFERENCE SLICE:", ['FRAME', 'TIME', 'NONE'], labelwidth=30, com=lambda k: self.update_slice(k))
        self.update_slice('TIME')
        self.multiprocessing_var = BooleanVar()
        self.multiprocess_cb = Checkbutton(settings_frm, text="Multiprocess videos (faster)", variable=self.multiprocessing_var, command=lambda: self.enable_dropdown_from_checkbox(check_box_var=self.multiprocessing_var, dropdown_menus=[self.multiprocess_dropdown]))
        self.multiprocess_dropdown = DropDownMenu(settings_frm, "CPU cores:", list(range(2, self.cpu_cnt)), "12")
        self.multiprocess_dropdown.setChoices(2)
        self.multiprocess_dropdown.disable()
        self.bg_slice_setting.setChoices('NONE')
        self.bg_clr_dropdown.setChoices('Black')
        self.fg_clr_dropdown.setChoices('White')

        settings_frm.grid(row=0, column=0, sticky=NW)
        self.video_path.grid(row=0, column=0, sticky=NW)
        self.bg_video_path.grid(row=1, column=0, sticky=NW)
        self.bg_slice_setting.grid(row=2, column=0, sticky=NW)
        self.bg_clr_dropdown.grid(row=3, column=0, sticky=NW)
        self.fg_clr_dropdown.grid(row=4, column=0, sticky=NW)
        self.multiprocess_cb.grid(row=5, column=0, sticky=NW)
        self.multiprocess_dropdown.grid(row=5, column=1, sticky=NW)
        self.main_frm.mainloop()


    def update_slice(self, x):
        if x == 'TIME':
            self.bg_start_time_eb.grid(row=0, column=0, sticky=NW)
            self.bg_end_time_eb.grid(row=1, column=0, sticky=NW)
            self.bg_start_time_eb.set_state(NORMAL)
            self.bg_end_time_eb.set_state(NORMAL)
        elif x == 'FRAME':
            self.bg_start_frm_eb.grid(row=0, column=0, sticky=NW)
            self.bg_end_frm_eb.grid(row=1, column=0, sticky=NW)
            self.bg_start_frm_eb.set_state(NORMAL)
            self.bg_end_frm_eb.set_state(NORMAL)
        else:
            self.bg_start_time_eb.set_state(DISABLED)
            self.bg_end_time_eb.set_state(DISABLED)
            self.bg_start_frm_eb.set_state(DISABLED)
            self.bg_end_frm_eb.set_state(DISABLED)
        self.create_run_frm(run_function=self.run)


    def run(self):
        pass








    #self.bg_slice_setting = FileSelect(settings_frm, "BACKGROUND REFERENCE TIME SLICE:", title="Select a video file", file_types=[("VIDEO", Options.ALL_VIDEO_FORMAT_OPTIONS.value)], lblwidth=30)





        # self.bg_start_frm_eb = Entry_Box(parent=settings_frm, labelwidth=30, entry_box_width=15, fileDescription='BACKGROUND VIDEO START FRAME:', validation='numeric')
        # self.bg_end_frm_eb = Entry_Box(parent=settings_frm, labelwidth=30, entry_box_width=15, fileDescription='BACKGROUND VIDEO END FRAME:', validation='numeric')
        # self.bg_start_time_eb = Entry_Box(parent=settings_frm, labelwidth=30, entry_box_width=15, fileDescription='BACKGROUND VIDEO START TIME:')
        # self.bg_end_time_eb = Entry_Box(parent=settings_frm, labelwidth=30, entry_box_width=15, fileDescription='BACKGROUND VIDEO END TIME:')
        #








        # self.multiprocessing_var = BooleanVar()
        # self.multiprocess_cb = Checkbutton(settings_frm, text="Multiprocess videos (faster)", variable=self.multiprocessing_var, command=lambda: self.enable_dropdown_from_checkbox(check_box_var=self.multiprocessing_var, dropdown_menus=[self.multiprocess_dropdown]))
        # self.multiprocess_dropdown = DropDownMenu(settings_frm, "CPU cores:", list(range(2, self.cpu_cnt)), "12")
        # self.multiprocess_dropdown.setChoices(2)
        # self.multiprocess_dropdown.disable()
        # self.bg_start_time_eb.entry_set('00:00:00')
        # self.bg_end_time_eb.entry_set('00:00:10')
        # self.bg_clr_dropdown.setChoices('Black')
        # self.fg_clr_dropdown.setChoices('White')
        #
        # settings_frm.grid(row=0, column=0, sticky=NW)
        # self.video_path.grid(row=0, column=0, sticky=NW)
        # self.bg_video_path.grid(row=1, column=0, sticky=NW)
        # self.bg_start_time_eb.grid(row=2, column=0, sticky=NW)
        # self.bg_end_time_eb.grid(row=3, column=0, sticky=NW)
        # self.bg_start_frm_eb.grid(row=4, column=0, sticky=NW)
        # self.bg_end_frm_eb.grid(row=5, column=0, sticky=NW)
        # self.bg_clr_dropdown.grid(row=6, column=0, sticky=NW)
        # self.fg_clr_dropdown.grid(row=7, column=0, sticky=NW)
        # self.multiprocess_cb.grid(row=8, column=0, sticky=NW)
        # self.multiprocess_dropdown.grid(row=8, column=1, sticky=NW)
        # self.create_run_frm(run_function=self.run)
        # self.main_frm.mainloop()
    #
    # def run(self):
    #     video_path = self.video_path.file_path
    #     _ = get_video_meta_data(video_path=video_path)
    #     bg_video = self.bg_video_path.file_path
    #     if not os.path.isfile(bg_video):
    #         bg_video = deepcopy(video_path)
    #     else:
    #         _ = get_video_meta_data(video_path=bg_video)
    #     start_time, end_time = self.bg_start_time_eb.entry_get.strip(), self.bg_end_time_eb.entry_get.strip()
    #     start_frm, end_frm = self.bg_start_frm_eb.entry_get.strip(), self.bg_end_frm_eb.entry_get.strip()
    #     if ((start_frm is not '') or (end_frm is not '')) and ((start_time is not '') or (end_time is not '')):
    #         raise InvalidInputError(msg=f'Provide start frame and end frame OR start time and end time', source=self.__class__.__name__)
    #     elif type(start_frm) != type(end_frm):
    #         raise InvalidInputError(msg=f'Pass start frame and end frame', source=self.__class__.__name__)
    #     elif type(start_time) != type(end_time):
    #         raise InvalidInputError(msg=f'Pass start time and end time', source=self.__class__.__name__)
    #     bg_clr = self.clr_dict[self.bg_clr_dropdown.getChoices()]
    #     fg_clr = self.clr_dict[self.fg_clr_dropdown.getChoices()]
    #
    #     if not self.multiprocess_var.get():
    #         video_bg_subtraction(video_path=video_path,
    #                              bg_video_path=bg_video,
    #                              )
    #



BackgroundRemoverPopUp()





