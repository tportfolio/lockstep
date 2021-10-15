import PySimpleGUI as sg
import base64
from os.path import dirname, join

from src.gui.constants import CallbackKey


class MainLayout(object):
    """
    GUI framework for file synchronization.
    Skeleton inspired by Demo Programs Browser sample for PySimpleGUI.
    """
    SPLIT_PANE = "SPLIT_PANE"
    SOURCE = "Source"
    DESTINATION = "Destination"

    SYNC_OPTIONS = ["One-way", "Two-way", "Update"]

    def __init__(self) -> None:
        sg.theme("DarkBlue13")

        gui_directory = dirname(__file__)
        # credit to MUI for original SVG path of this icon
        self.icon = base64.b64encode(open(join(gui_directory, "res/lock.png"), 'rb').read())
        self.run_taskbar_icon_boilerplate()

    @staticmethod
    def run_taskbar_icon_boilerplate() -> None:
        """
        Enables ability to set taskbar icon in Windows.
        See: https://stackoverflow.com/a/1552105
        :return: None
        """
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('arbitrary string')

    def create_sync_method_dropdown(self) -> sg.Column:
        components = [[
            sg.T('Select style of synchronization:'),
            sg.Combo(
                self.SYNC_OPTIONS,
                k=CallbackKey.SYNC_DROPDOWN,
                default_value="<none>",
                size=(30, 30),
                enable_events=True,
                readonly=True
            )
        ]]

        return sg.Column(components, element_justification='c', expand_x=True)

    @staticmethod
    def create_file_panel(direction: str, folder_name: str) -> sg.Column:
        components = [
            [sg.T(f"{direction}:"), sg.I(size=35), sg.FolderBrowse(k=direction)],
            [sg.Multiline(k=folder_name, size=(60, 30), write_only=True)]
        ]

        return sg.Column(components, element_justification='c', expand_x=True, expand_y=True)

    @staticmethod
    def create_bottom_buttons() -> sg.Column:
        button_pairs = [('Settings', CallbackKey.SETTINGS), ('Synchronize...', CallbackKey.SYNCHRONIZE), ('Exit', 'Exit')]
        components = [[sg.B(x, k=key) for (x, key) in button_pairs]]
        return sg.Column(components, element_justification='c', expand_x=True)

    def create_layout(self) -> list:
        return [
            [sg.T('Lockstep', font='Calibri 20')],
            [self.create_sync_method_dropdown()],
            [sg.Pane(
                [self.create_file_panel(self.SOURCE, "Folder 1"), self.create_file_panel(self.DESTINATION, "Folder 2")],
                k=self.SPLIT_PANE,
                orientation='h',
                pad=(30, 20)
            )],
            [self.create_bottom_buttons()]
        ]

    def create_window(self) -> sg.Window:
        window = sg.Window(
            'Lockstep',
            self.create_layout(),
            finalize=True,
            resizable=True,
            use_default_focus=False,
            icon=self.icon
        )

        window.set_min_size(window.size)
        window[self.SPLIT_PANE].expand(True, True, True)

        window.bring_to_front()
        return window
