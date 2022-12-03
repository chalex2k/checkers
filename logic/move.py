from dataclasses import dataclass

from .coord import Coord
from .figures import Figure


@dataclass
class Move:
    checker: Figure
    from_: Coord
    to: Coord

