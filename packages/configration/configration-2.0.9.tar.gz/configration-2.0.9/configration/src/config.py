"""Base class for config object for the application."""

from termcolor import cprint
import colorama

from .constants import (ERROR_COLOUR, CORRUPT_FILE_MSG, MISSING_ATTR_MSG,
                        NOT_OF_TYPE_MSG, FIELD, NOT_IN_DICT)

colorama.init()

MODULE_COLOUR = 'red'


class Config():
    """
    The class takes a path to a json file and if valid, returns a config dict.

    Attributes
    ----------

    path: str
        The path to the config file

    attrs: dict[str, list[type]
        The dict keys are the fields that are expected in the config json
        The dict item holds a list of allowed types for each files

        If there are attrs, then the config is validated.

    create: bool
        Whether or not the config should be created if missing.
        Defaults to False.
        (The individual sub-classes implement the function.)
    """

    def __init__(
            self,
            path: str,
            defaults: dict[str, str] = {},
            attrs: dict[str, list[type]] = {},
            create: bool = False
            ):
        self.path = path
        self.defaults = defaults
        self.attrs = attrs
        self.create = create
        self.config = self._get_config()
        for key, item in self.config.items():
            self.__dict__[key] = item

    def __repr__(self):
        if not self.attrs:
            return str(self.__dict__)
        output = ['Config:']
        for key, item in self.attrs.items():
            output .append(f'{key}, {self.__dict__[key]}')
        return '\n'.join(output)

    def _get_config(self) -> dict[str, object]:
        # Return config, if contents are valid.
        config = self._read_config()

        if config and not self.attrs:
            return config

        if config and self._validate_config(config):
            return config

        if self.defaults:
            return self.defaults
        return {}

    def _validate_config(self, config: dict[str, type]) -> bool:
        # Return True if structure and values in config are valid.
        for name, item_types in self.attrs.items():
            if name not in config:
                cprint(f'{CORRUPT_FILE_MSG} {MISSING_ATTR_MSG} {name}',
                       ERROR_COLOUR)
                return False
            if type(config[name]) not in item_types:
                cprint(
                    (f'{CORRUPT_FILE_MSG} {name} {NOT_OF_TYPE_MSG} '
                     f'{item_types}'),
                    ERROR_COLOUR)
                return False
        return True

    def update(self, field: str, value: object, force: bool = False) -> None:
        """Update the value of an attribute in config."""
        if not force and field not in self.__dict__['config']:
            cprint(f'{FIELD} {field} {NOT_IN_DICT}', ERROR_COLOUR)
            return

        self.__dict__['config'][field] = value
