import PySimpleGUI as sg
from os.path import exists
from threading import Thread

from src.gui.main_layout import MainLayout
from src.gui.constants import CallbackKey, SyncOptions
from src.file_diff.file_diff_evaluator import FileDiffEvaluator
from src.file_diff.file_synchronizer import FileSynchronizer
from src.gui.utilities import gen_treedata
from src.gui.images import ADD_ICON, REMOVE_ICON


class GuiManager(object):
    def __init__(self):
        self.file_diff_evaluator = FileDiffEvaluator(
            lambda diff: self.emit_event(CallbackKey.EVALUATION_COMPLETE, diff))
        self.file_synchronizer = FileSynchronizer()

        self.window = MainLayout().create_window()
        self.values = {}

        self.callbacks = {
            CallbackKey.EVALUATE: self.evaluate_file_diff,
            CallbackKey.EVALUATION_COMPLETE: self.display_file_diff,
            CallbackKey.SYNCHRONIZE: self.sync_folders,
            CallbackKey.SYNC_DROPDOWN: self.on_sync_dropdown,
            CallbackKey.SOURCE_FOLDER: lambda: self.evaluate_path_validity(CallbackKey.SOURCE_FOLDER),
            CallbackKey.DESTINATION_FOLDER: lambda: self.evaluate_path_validity(CallbackKey.DESTINATION_FOLDER)
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

    def emit_event(self, key, value):
        self.window.write_event_value(key, value)

    def has_callback(self, key: str) -> bool:
        return key in self.callbacks

    def execute_callback(self, key: str, values: dict) -> None:
        self.values = values
        self.callbacks[key]()

    def placeholder_callback(self) -> None:
        print(self.values)

    def get_path_state(self):
        return [self.values[key] for key in [
            CallbackKey.SOURCE_FOLDER,
            CallbackKey.DESTINATION_FOLDER,
            CallbackKey.SYNC_DROPDOWN
        ]]

    def update_button_states(self) -> None:
        src, dst, sync_style = self.get_path_state()

        evaluate_button_disabled = not (exists(src) and exists(dst))
        self.window[CallbackKey.EVALUATE].update(disabled=evaluate_button_disabled)

        synchronize_button_disabled = evaluate_button_disabled or sync_style not in SyncOptions.values()
        self.window[CallbackKey.SYNCHRONIZE].update(disabled=synchronize_button_disabled)

    def on_sync_dropdown(self) -> None:
        self.update_button_states()

    def evaluate_path_validity(self, key: str) -> None:
        filepath = self.values[key]
        if filepath:
            background_color = "#a4db9e" if exists(filepath) else "#f7cddb"
            self.window[key].update(background_color=background_color)

        self.update_button_states()

    def evaluate_file_diff(self) -> None:
        Thread(target=self.file_diff_evaluator.generate_file_diff, args=[*self.get_path_state()]).start()

    def display_file_diff(self) -> None:
        left, right = self.values[CallbackKey.EVALUATION_COMPLETE]
        self.window[CallbackKey.SOURCE_TREE].update(gen_treedata(sorted(left), ADD_ICON))
        self.window[CallbackKey.DESTINATION_TREE].update(gen_treedata(sorted(right), REMOVE_ICON))

    def sync_folders(self) -> None:
        Thread(target=self.file_synchronizer.run_sync, args=[*self.get_path_state()]).start()
