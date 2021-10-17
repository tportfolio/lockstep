import PySimpleGUI as sg

from src.gui.constants import CallbackKey, SettingsKey, SyncOptions
from src.gui.images import LOCK_ICON


class MainLayout(object):
    """
    GUI framework for file synchronization.
    Skeleton inspired by Demo Programs Browser sample for PySimpleGUI.
    """
    def __init__(self) -> None:
        sg.theme("DarkBlue13")
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

    @staticmethod
    def create_sync_method_dropdown() -> sg.Column:
        components = [[
            sg.T('Select style of synchronization:'),
            sg.Combo(
                sorted(SyncOptions.values()),
                k=CallbackKey.SYNC_DROPDOWN,
                default_value="<none>",
                size=(30, 30),
                enable_events=True,
                readonly=True
            )
        ]]

        return sg.Column(components, element_justification='c', expand_x=True)

    @staticmethod
    def create_configuration_dropdown() -> sg.Column:
        components = [[
            sg.T('Select/create configuration:'),
            sg.Combo(
                [],
                k=CallbackKey.CONFIGURATION_DROPDOWN,
                default_value="<none>",
                size=(30, 30),
                enable_events=True
            ),
            sg.B('Save', k=CallbackKey.SAVE_CONFIGURATION)
        ]]

        return sg.Column(components, element_justification='c', expand_x=True)

    @staticmethod
    def create_file_panel(direction: str, multiline_key: str, input_key: str) -> sg.Column:
        components = [
            [sg.T(f"{direction}:"), sg.I(size=35, enable_events=True, k=input_key), sg.FolderBrowse(k=direction)],
            [sg.Tree(data=sg.TreeData(), k=multiline_key, headings=[""], visible_column_map=[False], expand_x=True,
                     expand_y=True)]
        ]

        return sg.Column(components, element_justification='c', expand_x=True, expand_y=True)

    @staticmethod
    def create_bottom_buttons() -> sg.Column:
        button_pairs = [
            ("Evaluate", CallbackKey.EVALUATE, True),
            ("Synchronize...", CallbackKey.SYNCHRONIZE, True),
            ('Exit', 'Exit', False)
        ]
        components = [[sg.B(x, k=key, disabled=disabled) for (x, key, disabled) in button_pairs]]
        return sg.Column(components, element_justification='c', expand_x=True)

    def create_sync_tab(self) -> sg.Tab:
        return sg.Tab("Synchronize", [
            [self.create_configuration_dropdown()],
            [sg.Pane(
                [
                    self.create_file_panel("Source", CallbackKey.SOURCE_TREE, CallbackKey.SOURCE_FOLDER),
                    self.create_file_panel("Destination", CallbackKey.DESTINATION_TREE, CallbackKey.DESTINATION_FOLDER)
                ],
                orientation='h',
                pad=(30, 5),
                expand_x=True,
                expand_y=True
            )],
            [self.create_sync_method_dropdown()],
            [self.create_bottom_buttons()]
        ])

    @staticmethod
    def create_settings_tab():
        return sg.Tab("Settings", [
            [sg.Checkbox("Enable file purge on sync", k=SettingsKey.ENABLE_PURGE, enable_events=True, pad=(10, 10))]
        ])

    def create_layout(self) -> list:
        return [
            [sg.T('Lockstep', font='Calibri 20')],
            [sg.TabGroup([[self.create_sync_tab(), self.create_settings_tab()]], k=CallbackKey.TAB_GROUP)]
        ]

    def create_window(self) -> sg.Window:
        window = sg.Window(
            'Lockstep',
            self.create_layout(),
            finalize=True,
            resizable=True,
            use_default_focus=False,
            icon=LOCK_ICON
        )

        window.set_min_size(window.size)
        window[CallbackKey.TAB_GROUP].expand(True, True, True)

        for tree in [CallbackKey.SOURCE_TREE, CallbackKey.DESTINATION_TREE]:
            window[tree].Widget.heading("#0", text="File Path")  # workaround to set data in column 0

        window.bring_to_front()
        return window
