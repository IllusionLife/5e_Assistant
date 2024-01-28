from abc import ABC

import customtkinter
from enum import Enum

import util
from Base.exit_codes import *
from Base.exceptions import BaseExceptionRPG
from Base.logs import logger
from Base.config_handler import ConfigHandlerRPG


class GUIExceptionRPG(BaseExceptionRPG):
    """Raised when there is an issue, related to file reading/writing"""

    def __init__(self, msg, *add_info):
        super().__init__(msg, *add_info)

    def log_exception(self):
        logger().log_error(self.msg)
        pass


class OrderType(Enum):
    ORDER_PACK = 1
    ORDER_GRID = 2


class FrameWidgetRPG(ABC):
    def __init__(self, parent, widget_id, classinstance):
        self.parent = parent
        self.widget_id = widget_id
        self.instance = classinstance

    def config_widget(self, **kwargs):
        for key, value in kwargs.items():
            try:
                if key == "row" or key == "col":
                    continue
                self.instance.configure(**{key: value})
            except ValueError as exc:
                logger().log_error("Configuration <$1> is not supported for widget_id <$2>. Skipping."
                                   , key
                                   , self.widget_id)
                continue
        return EXIT_SUCCESS

    def disable_widget(self):
        self.config_widget(state="disabled")
        return EXIT_SUCCESS

    def pack_widget(self, **kwargs):
        if self.parent.get_order_type() == OrderType.ORDER_GRID:
            self.instance.grid(row=kwargs["row"]
                               , column=kwargs["col"]
                               , padx=kwargs.get("padx", None)
                               , pady=kwargs.get("pady", None)
                               , sticky=kwargs.get("sticky", None))
        else:
            self.instance.pack()


class WindowFrameRPG(customtkinter.CTkFrame, ABC):
    def __init__(self, parent, frame_id, order_type=1):
        if order_type not in OrderType.__members__:
            order_type = OrderType.ORDER_PACK
        self.frame_id = frame_id
        self.order_type = order_type
        self.parent = parent
        super().__init__(parent)
        self.widgets = dict()

    def get_order_type(self):
        return self.order_type

    def set_order_type(self, ordertype):
        if ordertype == "grid":
            self.order_type = OrderType.ORDER_GRID
        else:
            self.order_type = OrderType.ORDER_PACK

    def set_id(self, frame_id):
        self.frame_id = frame_id

    def get_id(self):
        return self.frame_id

    def get_parent(self):
        return self.parent

    def get_widget(self, widget_id):
        widget_id = util.str_to_id(widget_id)
        if not self.widget_exists(widget_id):
            return EXIT_DOESNT_EXISTS
        return self.widgets[widget_id]

    def __check_grid_requirements(self, widget_id, **kwargs):
        if self.order_type == OrderType.ORDER_GRID \
                and ("row" not in kwargs or "col" not in kwargs):
            raise GUIExceptionRPG("Row and/or column not provided for widget_id <$1>.", widget_id)
        return EXIT_SUCCESS

    def __log_selection(self, widget_id, selection=None):
        if selection is None:
            selection = self.get_widget(widget_id).get()
        if "#" in widget_id:
            widget_id = widget_id.split("#")[0]
        logger().log_debug("Selected <$1> from widget <$2> in frame <$3>.", selection, widget_id, self.get_id())
        return EXIT_SUCCESS

    def __on_button_clicked(self, command, widget_id):
        if "#" in widget_id:
            widget_id = widget_id.split("#")[0]
        logger().log_info("Clicked button <$1>", widget_id)
        if command is not None:
            return command()

    def widget_exists(self, widget_id):
        widget_id = util.str_to_id(widget_id)
        if widget_id in self.widgets.keys():
            return True
        return False

    def add_button(self, widget_id, text, command, **kwargs):
        try:
            self.__check_grid_requirements(widget_id, **kwargs)
            if command is not None and not callable(command):
                raise GUIExceptionRPG("Linked to button command is not a function.")
            widget_id = util.str_to_id(widget_id) + "#button"
            if self.widget_exists(widget_id):
                raise GUIExceptionRPG("Button with id <$1> already exists", widget_id)
            button = customtkinter.CTkButton(self.parent
                                             , text=text
                                             , command=lambda: self.__on_button_clicked(command, widget_id))
            self.widgets[widget_id] = FrameWidgetRPG(self, widget_id, button)
            self.widgets[widget_id].config_widget(**kwargs)
            self.widgets[widget_id].pack_widget(**kwargs)
        except GUIExceptionRPG as exc:
            return EXIT_ALREADY_EXISTS
        return self.widgets[widget_id]

    def add_checkbox(self, widget_id, text, **kwargs):
        try:
            self.__check_grid_requirements(widget_id, **kwargs)
            widget_id = util.str_to_id(widget_id) + "#checkbox"
            if self.widget_exists(widget_id):
                raise GUIExceptionRPG("Checkbox with id <$1> already exists", widget_id)
            checkbox = customtkinter.CTkCheckBox(self.parent
                                                 , text=text
                                                 , command=lambda: self.__log_selection(widget_id))
            self.widgets[widget_id] = FrameWidgetRPG(self, widget_id, checkbox)
            self.widgets[widget_id].config_widget(**kwargs)
            self.widgets[widget_id].pack_widget(**kwargs)
        except GUIExceptionRPG as exc:
            return EXIT_ALREADY_EXISTS
        return self.widgets[widget_id]

    def add_combo_box(self, widget_id, values: list, **kwargs):
        try:
            self.__check_grid_requirements(widget_id, **kwargs)
            widget_id = util.str_to_id(widget_id) + "#combo"
            if self.widget_exists(widget_id):
                raise GUIExceptionRPG("Combo box with id <$1> already exists", widget_id)
            combo_box = customtkinter.CTkComboBox(self.parent
                                                  , values=values
                                                  , command=lambda x: self.__log_selection(widget_id, x))
            self.widgets[widget_id] = FrameWidgetRPG(self, widget_id, combo_box)
            self.widgets[widget_id].config_widget(**kwargs)
            self.widgets[widget_id].pack_widget(**kwargs)
        except GUIExceptionRPG as exc:
            return EXIT_ALREADY_EXISTS
        return self.widgets[widget_id]

    def add_entry(self, widget_id, placeholder_text="", **kwargs):
        try:
            self.__check_grid_requirements(widget_id, **kwargs)
            widget_id = util.str_to_id(widget_id) + "#entry"
            if self.widget_exists(widget_id):
                raise GUIExceptionRPG("Entry with id <$1> already exists", widget_id)
            entrywidget = customtkinter.CTkEntry(self.parent
                                                 , placeholder_text=placeholder_text)
            self.widgets[widget_id] = FrameWidgetRPG(self, widget_id, entrywidget)
            self.widgets[widget_id].config_widget(**kwargs)
            self.widgets[widget_id].pack_widget(**kwargs)
        except GUIExceptionRPG as exc:
            return EXIT_ALREADY_EXISTS
        return self.widgets[widget_id]

    def add_label(self, widget_id, label_text, **kwargs):
        try:
            self.__check_grid_requirements(widget_id, **kwargs)
            widget_id = util.str_to_id(widget_id) + "#label"
            if self.widget_exists(widget_id):
                raise GUIExceptionRPG("Label with id <$1> already exists", widget_id)
            labelwidget = customtkinter.CTkLabel(self.parent
                                                 , text=label_text)
            self.widgets[widget_id] = FrameWidgetRPG(self, widget_id, labelwidget)
            self.widgets[widget_id].config_widget(**kwargs)
            self.widgets[widget_id].pack_widget(**kwargs)
        except GUIExceptionRPG as exc:
            return EXIT_ALREADY_EXISTS
        return self.widgets[widget_id]

    def add_textbox(self, widget_id, width, **kwargs):
        try:
            self.__check_grid_requirements(widget_id, **kwargs)
            widget_id = util.str_to_id(widget_id) + "#textbox"
            if self.widget_exists(widget_id):
                raise GUIExceptionRPG("Textbox with id <$1> already exists", widget_id)
            textbox = customtkinter.CTkTextbox(self.parent
                                               , width=width)
            if "text" in kwargs:
                textbox.insert("0.0", kwargs["text"])
                del (kwargs["text"])
            self.widgets[widget_id] = FrameWidgetRPG(self, widget_id, textbox)
            self.widgets[widget_id].config_widget(**kwargs)
            self.widgets[widget_id].pack_widget(**kwargs)
        except GUIExceptionRPG as exc:
            return EXIT_ALREADY_EXISTS
        return self.widgets[widget_id]

    def add_switch(self, widget_id, label, **kwargs):
        try:
            self.__check_grid_requirements(widget_id, **kwargs)
            widget_id = util.str_to_id(widget_id) + "#switch"
            if self.widget_exists(widget_id):
                raise GUIExceptionRPG("Switch with id <$1> already exists", widget_id)
            switchwidget = customtkinter.CTkSwitch(self.parent
                                                   , text=label)
            self.widgets[widget_id] = FrameWidgetRPG(self, widget_id, switchwidget)
            self.widgets[widget_id].config_widget(**kwargs)
            self.widgets[widget_id].pack_widget(**kwargs)
        except GUIExceptionRPG as exc:
            return EXIT_ALREADY_EXISTS
        return self.widgets[widget_id]

    def add_tabview(self, widget_id, **kwargs):
        try:
            self.__check_grid_requirements(widget_id, **kwargs)
            widget_id = util.str_to_id(widget_id) + "#tabview"
            if self.widget_exists(widget_id):
                raise GUIExceptionRPG("Tab view with id <$1> already exists", widget_id)
            tabview = customtkinter.CTkTabview(self.parent)
            self.widgets[widget_id] = FrameWidgetRPG(self, widget_id, tabview)
            self.widgets[widget_id].config_widget(**kwargs)
            self.widgets[widget_id].pack_widget(**kwargs)
        except GUIExceptionRPG as exc:
            return EXIT_ALREADY_EXISTS
        return self.widgets[widget_id]

    def add_tab(self, widget, tabtext, **kwargs):
        if isinstance(widget, str):
            widget = widget + "#tabview"
            if not self.widget_exists(widget):
                raise GUIExceptionRPG("Widget <$1> doesn't exist!", widget)
            widget = self.widgets[widget]
        key_list = list(self.widgets.keys())
        val_list = list(self.widgets.values())
        widget_id = util.str_to_id(tabtext) \
                    + "@" \
                    + key_list[val_list.index(widget)] \
                    + "#tab"
        if self.widget_exists(widget_id):
            raise GUIExceptionRPG("Tab with id <$1> for tabview <$2> already exists"
                                  , widget_id
                                  , key_list[val_list.index(widget)])
        widget.add(tabtext)
        self.widgets[widget_id] = WindowFrameRPG(widget_id, widget.tab(tabtext))
        self.widgets[widget_id].config_widget(**kwargs)
        return self.widgets[widget_id]

    def add_tabs(self, tabview, list_of_tabs: list):
        for tabtext in list_of_tabs:
            try:
                self.add_tab(tabview, tabtext)
            except GUIExceptionRPG as exc:
                continue

    def get_tab(self, tabview, tabtext):
        tabview = util.str_to_id(tabview)
        if isinstance(tabview, str):
            tabview = tabview + "#tabview"
            if not self.widget_exists(tabview):
                raise GUIExceptionRPG("Tabview <$1> doesn't exist!", tabview)
            tabview = self.widgets[tabview]
        key_list = list(self.widgets.keys())
        val_list = list(self.widgets.values())
        tab_id = util.str_to_id(tabtext) \
                 + "@" \
                 + key_list[val_list.index(tabview)] \
                 + "#tab"
        if not self.widget_exists(tab_id):
            raise GUIExceptionRPG("Tab with label <$1> doesn't exist in tabview <$2>"
                                  , tabtext
                                  , key_list[val_list.index(tabview)])
        return self.widgets[tab_id]


class WindowRPG(customtkinter.CTk):
    def __init__(self, title=None):
        super().__init__()
        self.conf = ConfigHandlerRPG("gui.conf")
        if title is not None:
            title = "RPG assistant - " + title
        else:
            title = "RPG assistant"
        self.title(title)
        self.toggle_fullscreen()
        if self.conf.get_conf('FULLSCREEN', 0) == 0:
            self.toggle_fullscreen()
        self.lift()
        self.attributes('-topmost', True)
        self.after_idle(self.attributes, '-topmost', False)
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.close_window)
        self.frames = dict()
        self.nameless_count = 0

    def toggle_fullscreen(self, _=None):
        if self.attributes("-fullscreen"):
            self.attributes("-fullscreen", False)
            width = self.conf.get_conf('WINDOW_WIDTH', 800)
            height = self.conf.get_conf('WINDOW_HEIGHT', 600)
            width_screen = self.winfo_screenwidth()
            height_screen = self.winfo_screenheight()
            self.geometry('%dx%d+%d+%d' % (width
                                           , height
                                           , (width_screen - width) / 2
                                           , (height_screen - height) / 2))
        else:
            self.attributes("-fullscreen", True)
            width_screen = self.winfo_screenwidth()
            height_screen = self.winfo_screenheight()
            self.geometry('%dx%d' % (width_screen, height_screen))
        self.update()

    def close_window(self, _event):
        self.destroy()
        return EXIT_CLOSE

    def loop(self):
        self.mainloop()

    def create_frame(self, frame_id=""):
        if frame_id == "":
            frame_id = self.nameless_count + 1
        if frame_id in self.frames:
            return EXIT_ALREADY_EXISTS
        self.frames[frame_id] = WindowFrameRPG(self, frame_id)
        self.nameless_count += 1
        return self.frames[frame_id]

    def get_frame(self, frame_id):
        if frame_id not in self.frames:
            return EXIT_DOESNT_EXISTS
        return self.frames[frame_id]
