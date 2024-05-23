from dataclasses import dataclass

from ..entities import Data


@dataclass
class ControlData(Data):
    value: str
    key: str = 'RelayState1|RelayState2'

    @property
    def values(self) -> list:
        return self.value.split('|')

    @property
    def keys(self) -> list:
        return self.key.split('|')

    def as_dict(self) -> dict:
        return dict(zip(self.keys, self.values))