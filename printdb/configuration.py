import os, json
from pathlib import Path
import printdb.utils as utils

SAVE_FOLDER = utils.path_join(os.path.expanduser("~"),"printdb")
class Configuration:
    def __init__(self, file="config.json"):
        self._loaded = False
        self._file = file
        self._data = {}

    def get_save(self):
        return utils.path_join(SAVE_FOLDER,f"{self._file}.json")

    def load_save(self):
        path = self.get_save()

        if utils.path_exists(path):
            with open(path, "r") as f:
                self._data = json.load(f)

        self._loaded = True

    def save_save(self):
        path = self.get_save()

        Path(SAVE_FOLDER).mkdir(parents=True, exist_ok=True)

        if utils.path_exists(path):
            utils.copy_file(path, path + ".bak")

        with open(path, "w") as f:
            json.dump(self._data, f, indent=4)

    def __setattr__(self, name, value):
        if name.startswith("_"):
            return object.__setattr__(self, name, value)

        if self._loaded:
            self._data[name] = value

        object.__setattr__(self, name, value)

    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]

        return None