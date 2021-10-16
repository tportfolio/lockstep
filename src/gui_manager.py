import PySimpleGUI as sg
from os.path import exists

from src.gui.main_layout import MainLayout
from src.gui.constants import CallbackKey


class GuiManager(object):
    def __init__(self):
        self.window = MainLayout().create_window()
        self.values = {}
        self.callbacks = {
            CallbackKey.SETTINGS: self.placeholder_callback,
            CallbackKey.SYNCHRONIZE: self.placeholder_callback,
            CallbackKey.SYNC_DROPDOWN: self.placeholder_callback,
            CallbackKey.SOURCE_FOLDER: lambda: self.evaluate_filepath(CallbackKey.SOURCE_FOLDER),
            CallbackKey.DESTINATION_FOLDER: lambda: self.evaluate_filepath(CallbackKey.DESTINATION_FOLDER)
        }

    def run(self):
        while True:
            event, values = self.window.read()
            if event in (sg.WINDOW_CLOSED, 'Exit'):
                break
            elif self.has_callback(event):
                self.execute_callback(event, values)
            else:
                print(f"Unexpected key: {event}")

        self.window.close()

    def has_callback(self, key: str) -> bool:
        return key in self.callbacks

    def execute_callback(self, key: str, values: dict) -> None:
        self.values = values
        self.callbacks[key]()

    def placeholder_callback(self) -> None:
        print(self.values)

    def evaluate_filepath(self, key: str) -> None:
        print(f"Evaluating {key} for path validity")
        filepath = self.values[key]
        if not filepath:
            return

        background_color = "#a4db9e" if exists(filepath) else "#f7cddb"
        self.window[key].update(background_color=background_color)
