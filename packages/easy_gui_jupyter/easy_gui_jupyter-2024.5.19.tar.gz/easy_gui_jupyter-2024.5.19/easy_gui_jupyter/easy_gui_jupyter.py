"""
A module to help simplify the create of GUIs in Jupyter notebooks using ipywidgets.
"""

import yaml
from ipyfilechooser import FileChooser

import ipywidgets as widgets
from IPython.display import display, clear_output

from pathlib import Path

CONFIG_FILE = Path.home() / ".easy_gui" / "easy_gui.yml"


def get_config(title: str):
    """
    Get the configuration dictionary without needing to initialize the GUI.

    :param title: title of the GUI
    """

    if not CONFIG_FILE.exists():
        return {}

    with open(CONFIG_FILE, "r") as f:
        cfg = yaml.load(f, Loader=yaml.SafeLoader)

    if title is None:
        return cfg
    elif title in cfg:
        return cfg[title]
    else:
        return {}


def save_config(title: str, cfg: dict):
    """
    Save the configuration dictionary to a file.

    :param title: title of the GUI
    :param cfg: configuration dictionary
    """
    CONFIG_FILE.parent.mkdir(exist_ok=True)

    base_config = get_config(None)  # loads the config file
    base_config[title] = cfg

    with open(CONFIG_FILE, "w") as f:
        yaml.dump(base_config, f)


class EasyGUI:
    """
    A class to simplify the creation of GUIs in Jupyter notebooks using ipywidgets.

    Args:
        title (str): The title of the GUI.
        width (str): The width of the widget container (e.g., "50%").

    Attributes:
        _layout (ipywidgets.Layout): The layout for widgets.
        _style (dict): Style configuration for widgets.
        _widgets (dict): A dictionary to store widgets.
        _nLabels (int): The number of labels added to the GUI.
        _main_display (ipywidgets.VBox): The main output widget for the GUI.
        _title (str): The title of the GUI.
        _cfg (dict): Configuration dictionary to store widget values.
        cfg (dict): Alias for the _cfg dictionary associated with the GUI.

    Methods:
        add_label: Add a label widget to the GUI.
        add_button: Add a button widget to the GUI.
        add_text: Add a text widget to the GUI.
        add_int_slider: Add an integer slider widget to the GUI.
        add_float_slider: Add a float slider widget to the GUI.
        add_checkbox: Add a checkbox widget to the GUI.
        add_int_text: Add an integer text widget to the GUI.
        add_float_text: Add a float text widget to the GUI.
        add_dropdown: Add a dropdown widget to the GUI.
        add_file_upload: Add a file upload widget to the GUI.
        save_settings: Save widget values to a configuration file.
        show: Display the GUI with its widgets.
        clear: Clear all widgets from the GUI.

    Note:
        This class simplifies the creation of GUIs in Jupyter notebooks using ipywidgets. It provides a variety of methods for adding different types of widgets to the GUI, and it allows for saving and loading widget values to maintain user settings across sessions.
    """

    def __init__(self, title="basic_gui", width="50%"):
        """
        Container for widgets.
        :param title: title of the widget container
        :param width: width of the widget container
        """
        self._layout = widgets.Layout(width=width)
        self._style = {"description_width": "initial"}
        self._widgets = {}
        self._nLabels = 0
        self._main_display = widgets.VBox()
        self._title = title
        self.cfg = get_config(title)

    def __getitem__(self, tag: str) -> widgets.Widget:
        return self._widgets[tag]

    def __len__(self) -> int:
        return len(self._widgets)

    def add_label(self, *args, **kwargs):
        """
        Add a label widget to the container.
        :param args: args for the widget
        :param kwargs: kwargs for the widget
        """
        self._nLabels += 1
        self._widgets[f"label_{self._nLabels}"] = widgets.Label(
            *args, **kwargs, layout=self._layout, style=self._style
        )

    def add_button(self, tag, *args, **kwargs):
        """
        Add a button widget to the container.
        :param tag: tag to identify the widget
        :param args: args for the widget
        :param kwargs: kwargs for the widget
        """
        self._widgets[tag] = widgets.Button(
            *args, **kwargs, layout=self._layout, style=self._style
        )

    def add_text(self, tag, *args, remember_value=False, **kwargs):
        """
        Add a text widget to the container.
        :param tag: tag to identify the widget
        :param args: args for the widget
        :param remember_value: remember the last value
        :param kwargs: kwargs for the widget

        Example:
            >>> gui = EasyGUI()
            >>> gui.add_text("text", value="Hello, world!")
        """
        if remember_value and tag in self.cfg:
            kwargs["value"] = str(self.cfg[tag])

        self._widgets[tag] = widgets.Text(
            *args, **kwargs, layout=self._layout, style=self._style
        )

    def add_textarea(self, tag, *args, remember_value=False, **kwargs):
        """
        Add a textarea widget to the container.
        :param tag: tag to identify the widget
        :param args: args for the widget
        :param remember_value: remember the last value
        :param kwargs: kwargs for the widget
        """
        if remember_value and tag in self.cfg:
            kwargs["value"] = str(self.cfg[tag])
        self._widgets[tag] = widgets.Textarea(
            *args, **kwargs, layout=self._layout, style=self._style
        )

        self._widgets[tag] = widgets.Textarea(
            *args, **kwargs, layout=self._layout, style=self._style
        )

    def add_int_slider(self, tag, *args, remember_value=False, **kwargs):
        """
        Add a integer slider widget to the container.
        :param tag: tag to identify the widget
        :param args: args for the widget
        :param remember_value: remember the last value
        :param kwargs: kwargs for the widget
        """
        if (
            remember_value
            and tag in self.cfg
            and kwargs["min"] <= self.cfg[tag] <= kwargs["max"]
        ):
            kwargs["value"] = int(self.cfg[tag])
        self._widgets[tag] = widgets.IntSlider(
            *args, **kwargs, layout=self._layout, style=self._style
        )

    def add_float_slider(self, tag, *args, remember_value=False, **kwargs):
        """
        Add a float slider widget to the container.
        :param tag: tag to identify the widget
        :param args: args for the widget
        :param remember_value: remember the last value
        :param kwargs: kwargs for the widget
        """
        if remember_value and tag in self.cfg:
            kwargs["value"] = self.cfg[tag]
        self._widgets[tag] = widgets.FloatSlider(
            *args, **kwargs, layout=self._layout, style=self._style
        )

    def add_checkbox(self, tag, *args, remember_value=False, **kwargs):
        """
        Add a checkbox widget to the container.
        :param tag: tag to identify the widget
        :param args: args for the widget
        :param remember_value: remember the last value
        :param kwargs: kwargs for the widget
        """
        if remember_value and tag in self.cfg:
            kwargs["value"] = self.cfg[tag]
        self._widgets[tag] = widgets.Checkbox(
            *args, **kwargs, layout=self._layout, style=self._style
        )

    def add_int_text(self, tag, *args, remember_value=False, **kwargs):
        """
        Add a integer text widget to the container.
        :param tag: tag to identify the widget
        :param args: args for the widget
        :param remember_value: remember the last value
        :param kwargs: kwargs for the widget
        """
        if remember_value and tag in self.cfg:
            kwargs["value"] = self.cfg[tag]

        self._widgets[tag] = widgets.IntText(
            *args, **kwargs, layout=self._layout, style=self._style
        )

    def add_float_text(self, tag, *args, remember_value=False, **kwargs):
        """
        Add a float text widget to the container.
        :param tag: tag to identify the widget
        :param args: args for the widget
        :param remember_value: remember the last value
        :param kwargs: kwargs for the widget
        """
        if remember_value and tag in self.cfg:
            kwargs["value"] = self.cfg[tag]
        self._widgets[tag] = widgets.FloatText(
            *args, **kwargs, layout=self._layout, style=self._style
        )

    def add_dropdown(self, tag, *args, remember_value=False, **kwargs):
        """
        Add a dropdown widget to the container.
        :param tag: tag to identify the widget
        :param args: args for the widget
        :param remember_value: remember the last value
        :param kwargs: kwargs for the widget

        Example:
            >>> gui = EasyGUI()
            >>> gui.add_dropdown("dropdown", options=["A", "B", "C"])
        """
        if remember_value and tag in self.cfg and self.cfg[tag] in kwargs["options"]:
            kwargs["value"] = self.cfg[tag]
        self._widgets[tag] = widgets.Dropdown(
            *args, **kwargs, layout=self._layout, style=self._style
        )

    def add_file_upload(self, tag, *args, accept=None, multiple=False, **kwargs):
        """
        Add a file upload widget to the container.
        :param tag: tag to identify the widget
        :param args: args for the widget
        :param accept: file types to accept
        :param multiple: allow multiple files to be uploaded
        :param kwargs: kwargs for the widget
        """
        self._widgets[tag] = FileChooser()
        if accept is not None:
            self._widgets[tag].filter_pattern = accept

    def save_settings(self):
        # remember widget values for next time and store them in a config file
        for tag in self._widgets:
            if tag.startswith("label_"):
                pass
            elif hasattr(self._widgets[tag], "value"):
                self.cfg[tag] = self._widgets[tag].value

        save_config(self._title, self.cfg)

    def restore_default_settings(self):
        # restore default settings
        save_config(self._title, {})
        self.clear()
        self.show()

    def show(self):
        """
        Show the widgets in the container.
        """
        # display the widgets
        self._main_display.children = tuple(self._widgets.values())
        clear_output()
        display(self._main_display)

    def clear(self):
        """
        Clear the widgets in the container.
        """
        self._widgets = {}
        self._nLabels = 0
        self._main_display.children = ()
