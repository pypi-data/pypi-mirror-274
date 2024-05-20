# -*- coding: utf-8 -*-

from typing import Final

from plugpack.module.errors import (
    ModuleAttributeInvalidValueError,
    ModuleAttributeNotFoundError,
)
from plugpack.module.mixin._base import ModuleBase

ATTR_VERSION: Final[str] = "__version__"


class ModuleVersion(ModuleBase):
    @property
    def has_version(self) -> bool:
        return self.has(ATTR_VERSION)

    def get_version(self) -> str:
        if not self.has(ATTR_VERSION):
            raise ModuleAttributeNotFoundError(self.module_name, ATTR_VERSION)

        value = self.get(ATTR_VERSION)

        if value is None:
            raise ModuleAttributeInvalidValueError(
                self.module_name, ATTR_VERSION, "It must not be of `None`"
            )

        if not isinstance(value, str):
            raise ModuleAttributeInvalidValueError(
                self.module_name, ATTR_VERSION, "The attribute must be of type 'str'"
            )

        return value

    @property
    def version(self) -> str:
        try:
            return self.get_version()
        except:  # noqa
            return str()
