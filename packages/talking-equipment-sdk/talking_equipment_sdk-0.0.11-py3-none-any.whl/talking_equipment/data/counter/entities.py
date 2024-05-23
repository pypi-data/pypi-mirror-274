from dataclasses import dataclass

from ..entities import Data


@dataclass
class CounterData(Data):
    value: int