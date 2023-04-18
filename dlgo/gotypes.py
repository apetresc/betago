from __future__ import annotations
import enum
from typing import List, NamedTuple


class Player(enum.Enum):
    black = 1
    white = 2

    @property
    def other(self):
        return Player.black if self == Player.white else Player.white

    def __str__(self):
        return self.name


class Point(NamedTuple):
    row: int
    col: int

    def neighbors(self) -> List[Point]:
        return [
                Point(self.row - 1, self.col),
                Point(self.row + 1, self.col),
                Point(self.row, self.col - 1),
                Point(self.row, self.col + 1),
        ]
