# -*- coding: utf-8 -*-

from typing import Final

from plugpack.module.errors import (
    ModuleAttributeInvalidValueError,
    ModuleAttributeNotFoundError,
)
from plugpack.module.mixin._base import ModuleBase

ATTR_DOC: Final[str] = "__doc__"


class ModuleDoc(ModuleBase):
    @property
    def has_doc(self) -> bool:
        return self.has(ATTR_DOC)

    def get_doc(self) -> str:
        if not self.has(ATTR_DOC):
            raise ModuleAttributeNotFoundError(self.module_name, ATTR_DOC)

        value = self.get(ATTR_DOC)

        if value is None:
            raise ModuleAttributeInvalidValueError(
                self.module_name,
                ATTR_DOC,
                "It must not be of `None`",
            )

        if not isinstance(value, str):
            raise ModuleAttributeInvalidValueError(
                self.module_name,
                ATTR_DOC,
                "The attribute must be of type `str`",
            )

        return value

    @property
    def doc(self) -> str:
        try:
            return self.get_doc()
        except:  # noqa
            return str()
