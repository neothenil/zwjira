import json
import copy
from pathlib import Path


class Config:
    # TODO: fill default vernums
    __default_vernums = {
        "ZWCAD2020 SP2": "2020.01.07(53615)_x64",
        "ZWCAD2021 SP2": "2021.03.18(63143)_x64",
        "ZWCAD2022 SP2": "22.20_2021.12.16(2dc3d9e9b39)_x64",
        "ZWCAD2023 Official": "23.00_2022.08.03(#7913-2ebd8186234)_x64",
        "ZWCAD2023 SP1": "23.10_2022.08.18(#8525-0d832381e57)_x64",
        "ZWCAD2023 SP2": "23.20_2022.11.17(#4989-3118d17423f)_x64",
    }

    __allowed_attributes = ["server", "username", "password", "vernums"]
    __first_time_message = """This is the first time you run zwjira. Please setup your authentication configuration with following commands:

    zwjira config username <your_username>
    zwjira config password <your_password>

    """

    def __init__(self):
        self._path = Path.home() / ".zwjira"
        if not self._path.exists():
            self._make_default_config_file()
            print(self.__first_time_message)
            exit(0)
        if not self._path.is_file():
            print(
                "Error occurs while reading configuration file: {} is not a file.".format(
                    self._path
                )
            )
            exit(1)
        text = self._path.read_text()
        self._data = json.loads(text)

    def __getattr__(self, attr):
        if attr not in self.__allowed_attributes:
            raise AttributeError(
                "{!r} is not a configuration item.".format(attr)
            )
        return self._data[attr]

    def __setattr__(self, attr, value):
        if attr in self.__allowed_attributes:
            self._data[attr] = value
        else:
            super().__setattr__(attr, value)

    def is_allowed(self, attr):
        return attr in self.__allowed_attributes

    def _make_default_config_file(self):
        self._data = {
            "server": "https://jira.zwcad.com",
            "username": "xxx",
            "password": "xxx",
            "vernums": self.__default_vernums,
        }
        self.save()

    def save(self):
        text = json.dumps(self._data)
        self._path.write_text(text)


config = Config()


def _set_config(attr, value):
    if not config.is_allowed(attr):
        print("Error: {!r} is not a configuration item.".format(attr))
        exit(1)
    setattr(config, attr, value)
    config.save()


def command_config(attr, value):
    if attr != "vernums":
        _set_config(attr, value)
        return 0
    fix_version = value.split(":")[0]
    vernum = value.split(":")[1]
    vernums = copy.deepcopy(config.vernums)
    vernums[fix_version] = vernum
    _set_config(attr, vernums)
    return 0


def command_reset_config():
    config._make_default_config_file()
    return 0
