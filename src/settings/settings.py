from os.path import expanduser, exists, join
from os import makedirs
from typing import Any
import json

from src.gui.constants import SettingsKey


class GuiSettings(object):
    """
    This class is responsible for reading/writing GUI settings from/to disk.
    """
    def __init__(self) -> None:
        self.base_folder = join(expanduser("~"), ".lockstep")
        self.settings_file = join(self.base_folder, "settings.json")
        self.configurations_file = join(self.base_folder, "configurations.json")

        self.__gui_settings = {SettingsKey.ENABLE_PURGE: False}
        self.__configurations = {}

    def load_settings(self) -> None:
        """
        Read GUI settings/configurations from file, if possible.
        :return: None
        """
        if not exists(self.base_folder):
            makedirs(self.base_folder)

        if not exists(self.settings_file):
            self.save_to_file(self.settings_file, self.gui_settings)
        else:
            with open(self.settings_file, "r") as sf:
                self.gui_settings = json.load(sf)

        if exists(self.configurations_file):
            with open(self.configurations_file, "r") as sf:
                self.configurations = json.load(sf)

        print(f"GUI settings are: {self.gui_settings}")
        print(f"Configurations are: {self.configurations}")

    @staticmethod
    def save_to_file(filename: str, data: dict) -> None:
        """
        Write dictionary to file.
        :param filename: filename
        :param data: dictionary (settings/config)
        :return: None
        """
        with open(filename, "w") as sf:
            json.dump(data, sf, indent=4)

    @property
    def gui_settings(self) -> dict:
        """
        Get GUI settings.
        :return: GUI settings
        """
        return self.__gui_settings

    @gui_settings.setter
    def gui_settings(self, settings: dict) -> None:
        """
        Set GUI settings.
        :param settings: GUI settings
        :return: None
        """
        self.__gui_settings = settings

    @property
    def configurations(self) -> dict:
        """
        Get configurations.
        :return: configurations dictionary
        """
        return self.__configurations

    @configurations.setter
    def configurations(self, configurations: dict):
        """
        Set configurations.
        :param configurations: configurations dictionary
        :return: None
        """
        self.__configurations = configurations

    def update_gui_setting(self, k: str, v: Any) -> None:
        """
        Commit GUI setting change locally and to file.
        :param k: setting key
        :param v: value
        :return: None
        """
        self.gui_settings[k] = v
        self.save_to_file(self.settings_file, self.gui_settings)

    def update_configuration(self, k: str, kv_pairs: dict) -> None:
        """
        Commit configuration change locally and to file.
        :param k: configuration key
        :param kv_pairs: configuration values
        :return: None
        """
        self.configurations[k] = kv_pairs
        self.save_to_file(self.configurations_file, self.configurations)
