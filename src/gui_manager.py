import PySimpleGUI as sg
from os.path import exists, dirname, basename
from threading import Thread

from src.gui.main_layout import MainLayout
from src.gui.constants import CallbackKey
from src.file_diff.file_diff_evaluator import FileDiffEvaluator


class GuiManager(object):
    def __init__(self):
        self.file_diff_evaluator = FileDiffEvaluator(
            lambda diff: self.emit_event(CallbackKey.EVALUATION_COMPLETE, diff))
        self.window = MainLayout().create_window()
        self.values = {}

        self.callbacks = {
            CallbackKey.SETTINGS: self.placeholder_callback,
            CallbackKey.EVALUATE: self.evaluate_file_diff,
            CallbackKey.EVALUATION_COMPLETE: self.display_file_diff,
            CallbackKey.SYNCHRONIZE: self.placeholder_callback,
            CallbackKey.SYNC_DROPDOWN: self.placeholder_callback,
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

    def evaluate_path_validity(self, key: str) -> None:
        filepath = self.values[key]
        if filepath:
            background_color = "#a4db9e" if exists(filepath) else "#f7cddb"
            self.window[key].update(background_color=background_color)

        src = self.values[CallbackKey.SOURCE_FOLDER]
        dst = self.values[CallbackKey.DESTINATION_FOLDER]

        evaluate_button_disabled = not (exists(src) and exists(dst))
        self.window[CallbackKey.EVALUATE].update(disabled=evaluate_button_disabled)

    def evaluate_file_diff(self) -> None:
        src = self.values[CallbackKey.SOURCE_FOLDER]
        dst = self.values[CallbackKey.DESTINATION_FOLDER]
        sync_style = self.values[CallbackKey.SYNC_DROPDOWN]
        Thread(target=self.file_diff_evaluator.generate_file_diff, args=[src, dst, sync_style]).start()

    def display_file_diff(self) -> None:
        left, right = self.values[CallbackKey.EVALUATION_COMPLETE]
        self.window[CallbackKey.SOURCE_TREE].update(self.gen_treedata(sorted(left)))
        self.window[CallbackKey.DESTINATION_TREE].update(self.gen_treedata(sorted(right)))

    @staticmethod
    def gen_treedata(data) -> sg.TreeData:
        treedata = sg.TreeData()

        for path in data:
            parent_folder = dirname(path)
            folders = parent_folder.split("/")
            filename = basename(path)

            # iteratively add parent folders as keys to tree, if necessary
            for i, folder in enumerate(folders):
                parent = "/".join(folders[:i])
                if not parent:
                    parent = ''

                curr = "/".join(folders[:i+1])
                val = folders[i]
                if curr not in treedata.tree_dict:
                    treedata.insert(parent, curr, val, values=[])

            # insert file into tree
            treedata.insert(parent_folder, path, filename, values=[])

        return treedata
