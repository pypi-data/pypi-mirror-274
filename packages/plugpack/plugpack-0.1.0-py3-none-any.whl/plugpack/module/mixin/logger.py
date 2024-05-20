# -*- coding: utf-8 -*-

from logging import Logger, getLogger
from typing import Final

from plugpack.module.errors import (
    ModuleAttributeInvalidValueError,
    ModuleAttributeNotFoundError,
)
from plugpack.module.mixin._base import ModuleBase

ATTR_LOGGER: Final[str] = "__logger__"


class ModuleLogger(ModuleBase):
    @property
    def has_logger(self) -> bool:
        return self.has(ATTR_LOGGER)

    def get_logger(self) -> Logger:
        if not self.has(ATTR_LOGGER):
            raise ModuleAttributeNotFoundError(self.module_name, ATTR_LOGGER)

        value = self.get(ATTR_LOGGER)

        if value is None:
            raise ModuleAttributeInvalidValueError(
                self.module_name,
                ATTR_LOGGER,
                "It must not be of `None`",
            )

        if isinstance(value, str):
            return getLogger(value)
        elif isinstance(value, Logger):
            return value
        else:
            raise ModuleAttributeInvalidValueError(
                self.module_name,
                ATTR_LOGGER,
                f"Unknown attribute type: {type(value).__name__}",
            )

    @property
    def logger(self) -> Logger:
        try:
            return self.get_logger()
        except:  # noqa
            return getLogger(self.module_name)
