import PySimpleGUI as sg
from os.path import exists
from threading import Thread

from src.file_diff.file_diff_evaluator import FileDiffEvaluator
from src.file_diff.file_synchronizer import FileSynchronizer
from src.gui.main_layout import MainLayout
from src.gui.constants import CallbackKey, SettingsKey, SyncOptions
from src.gui.utilities import gen_treedata
from src.gui.images import ADD_ICON, REMOVE_ICON
from src.settings.settings import GuiSettings


class GuiManager(object):
    """
    This class handles events from the GUI and runs callback methods based on the event value(s).
    """
    def __init__(self) -> None:
        self.gui_settings = GuiSettings()
        self.gui_settings.load_settings()

        # TODO: pass these as arguments to support daemon service
        self.file_diff_evaluator = FileDiffEvaluator(
            lambda diff: self.emit_event(CallbackKey.EVALUATION_COMPLETE, diff))
        self.file_synchronizer = FileSynchronizer(self.gui_settings.gui_settings[SettingsKey.ENABLE_PURGE])

        self.window = MainLayout().create_window()
        self.window[CallbackKey.CONFIGURATION_DROPDOWN].update(values=list(self.gui_settings.configurations.keys()))
        self.values = {}

        self.callbacks = {
            CallbackKey.EVALUATE: self.__evaluate_file_diff,
            CallbackKey.EVALUATION_COMPLETE: self.__display_file_diff,
            CallbackKey.SYNCHRONIZE: self.__sync_folders,
            CallbackKey.SYNC_DROPDOWN: self.__on_sync_dropdown,
            CallbackKey.CONFIGURATION_DROPDOWN: self.__on_configuration_dropdown,
            CallbackKey.SAVE_CONFIGURATION: self.__on_configuration_save,
            CallbackKey.SOURCE_FOLDER: lambda: self.__evaluate_path_validity(CallbackKey.SOURCE_FOLDER),
            CallbackKey.DESTINATION_FOLDER: lambda: self.__evaluate_path_validity(CallbackKey.DESTINATION_FOLDER),
            SettingsKey.ENABLE_PURGE: self.__purge_checkbox
        }

    def run(self) -> None:
        """
        Run in continuous loop until window is exited.
        :return: None
        """
        while True:
            event, values = self.window.read()
            if event in (sg.WINDOW_CLOSED, 'Exit'):
                break
            elif self.__has_callback(event):
                self.__execute_callback(event, values)
            else:
                print(f"Unexpected key: {event}")

        self.window.close()

    def emit_event(self, key: str, value: str) -> None:
        """
        Manually create event for window.
        :param key: event
        :param value: value
        :return: None
        """
        self.window.write_event_value(key, value)

    def __has_callback(self, key: str) -> bool:
        """
        Wrapper for existence of key in callback dictionary.
        :param key: event name
        :return: boolean indicating existing of corresponding callback
        """
        return key in self.callbacks

    def __execute_callback(self, key: str, values: dict) -> None:
        """
        Store incoming values from window and execute callback.
        :param key: callback key
        :param values: values from window
        :return: None
        """
        self.values = values
        self.callbacks[key]()

    def __get_path_state(self) -> list:
        """
        Grabs most commonly used state values for sync paths.
        :return: list of values (src, dst, sync style)
        """
        return [self.values[key] for key in [
            CallbackKey.SOURCE_FOLDER,
            CallbackKey.DESTINATION_FOLDER,
            CallbackKey.SYNC_DROPDOWN
        ]]

    def __update_button_states(self) -> None:
        """
        Update button states based on changes to paths and sync option.
        :return: None
        """
        src, dst, sync_style = self.__get_path_state()

        evaluate_button_disabled = not (exists(src) and exists(dst))
        self.window[CallbackKey.EVALUATE].update(disabled=evaluate_button_disabled)

        synchronize_button_disabled = evaluate_button_disabled or sync_style not in SyncOptions.values()
        self.window[CallbackKey.SYNCHRONIZE].update(disabled=synchronize_button_disabled)

    def __on_sync_dropdown(self) -> None:
        """
        Update button states when sync dropdown option changes.
        :return: None
        """
        self.__update_button_states()

    def __on_configuration_dropdown(self) -> None:
        """
        Populate configuration details into GUI.
        :return: None
        """
        key = self.values[CallbackKey.CONFIGURATION_DROPDOWN]
        if key not in self.gui_settings.configurations:  # shouldn't happen
            print(f"Unexpected key in configurations: {key}")
            return

        metadata = self.gui_settings.configurations[key]
        src, dst, sync = metadata["src"], metadata["dst"], metadata["sync"]

        self.values[CallbackKey.SOURCE_FOLDER] = src
        self.values[CallbackKey.DESTINATION_FOLDER] = dst
        self.values[CallbackKey.SYNC_DROPDOWN] = sync

        self.window[CallbackKey.SOURCE_FOLDER].update(src)
        self.window[CallbackKey.DESTINATION_FOLDER].update(dst)
        self.window[CallbackKey.SYNC_DROPDOWN].update(sync)

        for key in [CallbackKey.SOURCE_FOLDER, CallbackKey.DESTINATION_FOLDER]:
            self.__evaluate_path_validity(key)

    def __on_configuration_save(self) -> None:
        """
        Save configuration to file.
        :return: None
        """
        key = self.values[CallbackKey.CONFIGURATION_DROPDOWN]
        self.gui_settings.update_configuration(key, dict(zip(["src", "dst", "sync"], self.__get_path_state())))

    def __evaluate_path_validity(self, key: str) -> None:
        """
        Reflect existence of path with background color in each folder field.
        :param key: folder key
        :return: None
        """
        filepath = self.values[key]
        if filepath:
            background_color = "#a4db9e" if exists(filepath) else "#f7cddb"
            self.window[key].update(background_color=background_color)

        self.__update_button_states()

    def __evaluate_file_diff(self) -> None:
        """
        Run file diff evaluator.
        :return: None
        """
        Thread(target=self.file_diff_evaluator.generate_file_diff, args=[*self.__get_path_state()]).start()

    def __display_file_diff(self) -> None:
        """
        Take file diff and transform it into file trees for source and destination folders.
        :return: None
        """
        left, right = self.values[CallbackKey.EVALUATION_COMPLETE]
        self.window[CallbackKey.SOURCE_TREE].update(gen_treedata(sorted(left), ADD_ICON))
        self.window[CallbackKey.DESTINATION_TREE].update(gen_treedata(sorted(right), REMOVE_ICON))

    def __sync_folders(self) -> None:
        """
        Run file sync process.
        :return: None
        """
        Thread(target=self.file_synchronizer.run_sync, args=[*self.__get_path_state()]).start()

    def __purge_checkbox(self) -> None:
        """
        Globally update enable purge checkbox state.
        :return: None
        """
        value = self.values[SettingsKey.ENABLE_PURGE]
        self.gui_settings.update_gui_setting(SettingsKey.ENABLE_PURGE, value)
        self.file_synchronizer.enable_purge = value
