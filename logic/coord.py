from dataclasses import dataclass


@dataclass
class Coord:
    r: int
    c: int

    def __str__(self):
        return f'{self.r};{self.c}'
