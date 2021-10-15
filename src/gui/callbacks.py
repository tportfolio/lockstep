import PySimpleGUI as sg

from src.gui.constants import CallbackKey


class Callbacks(object):
    def __init__(self, window: sg.Window) -> None:
        self.window = window
        self.values = {}
        self.callbacks = {
            CallbackKey.SETTINGS: self.placeholder_callback,
            CallbackKey.SYNCHRONIZE: self.placeholder_callback,
            CallbackKey.SYNC_DROPDOWN: self.placeholder_callback
        }

    def has_callback(self, key) -> bool:
        return key in self.callbacks

    def execute_callback(self, key: str, values: dict) -> None:
        self.values = values
        self.callbacks[key]()

    def placeholder_callback(self) -> None:
        print(self.values)
