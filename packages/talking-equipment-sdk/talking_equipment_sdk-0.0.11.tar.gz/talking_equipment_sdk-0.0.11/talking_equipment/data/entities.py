from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Union


@dataclass
class Data(ABC):
    value: Union[int, float, str]

    @classmethod
    @property
    def value_type(cls) -> Union[int, float, str]:
        return cls.__annotations__['value']

    @classmethod
    @property
    def value_type_str(cls) -> str:
        return cls.value_type.__name__

    @property
    def is_int(self) -> bool:
        return isinstance(self.value, int)

    @property
    def is_float(self) -> bool:
        return isinstance(self.value, float)

    @property
    def is_str(self) -> bool:
        return isinstance(self.value, str)

    @classmethod
    @property
    def name(cls) -> str:
        return cls.__name__
