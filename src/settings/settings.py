from os.path import expanduser, exists, join
from os import makedirs
from typing import Any
import json

from src.gui.constants import SettingsKey


class GuiSettings(object):
    def __init__(self) -> None:
        self.base_folder = join(expanduser("~"), ".lockstep")
        self.settings_file = join(self.base_folder, "settings.json")
        self.configurations_file = join(self.base_folder, "configurations.json")

        self.__gui_settings = {SettingsKey.ENABLE_PURGE: False}
        self.__configurations = {}

    def load_settings(self) -> None:
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
    def save_to_file(filename, data):
        with open(filename, "w") as sf:
            json.dump(data, sf, indent=4)

    @property
    def gui_settings(self):
        return self.__gui_settings

    @gui_settings.setter
    def gui_settings(self, settings):
        self.__gui_settings = settings

    @property
    def configurations(self):
        return self.__configurations

    @configurations.setter
    def configurations(self, configurations):
        self.__configurations = configurations

    def update_gui_setting(self, k: str, v: Any):
        self.gui_settings[k] = v
        self.save_to_file(self.settings_file, self.gui_settings)

    def update_configuration(self, k: str, kv_pairs: dict):
        self.configurations[k] = kv_pairs
        self.save_to_file(self.configurations_file, self.configurations)
