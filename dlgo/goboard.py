from __future__ import annotations
import copy
from typing import Optional, Dict, FrozenSet, Iterable, List, Tuple

from . import zobrist
from .gotypes import Player, Point


class Play():
    """A stone placement on the board."""
    
    def __init__(self, point: Point):
        self.point = point

class Resign():
    pass

class Pass():
    pass

Move = Play | Resign | Pass

class GoString():
    def __init__(self, color: Player, stones: Iterable[Point], liberties: Iterable[Point]):
        self.color = color
        self.stones = frozenset(stones)
        self.liberties = frozenset(liberties)

    def without_liberty(self, point: Point) -> GoString:
        new_liberties = self.liberties - {point}
        return GoString(self.color, self.stones, new_liberties)

    def with_liberty(self, point: Point) -> GoString:
        new_liberties = self.liberties | {point}
        return GoString(self.color, self.stones, new_liberties)

    def merged_with(self, go_string: GoString) -> GoString:
        assert go_string.color == self.color
        combined_stones = self.stones | go_string.stones
        return GoString(
            self.color,
            combined_stones,
            (self.liberties | go_string.liberties) - combined_stones
        )

    @property
    def num_liberties(self) -> int:
        return len(self.liberties)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, GoString) and \
            self.color == other.color and \
            self.stones == other.stones and \
            self.liberties == other.liberties


class Board():
    def __init__(self, num_rows: int, num_cols: int):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid: Dict[Point, Optional[GoString]] = {}
        self._hash = zobrist.EMPTY_BOARD

    def is_on_grid(self, point: Point) -> bool:
        return 1 <= point.row <= self.num_rows and \
            1 <= point.col <= self.num_cols

    def get(self, point: Point) -> Optional[Player]:
        string = self._grid.get(point)
        if string is None:
            return None
        return string.color

    def get_go_string(self, point: Point) -> Optional[GoString]:
        return self._grid.get(point)

    def _remove_string(self, string: GoString) -> None:
        for point in string.stones:
            for neighbor in point.neighbors():
                neighbor_string = self._grid.get(neighbor)
                if neighbor_string is None:
                    continue
                if neighbor_string is not string:
                    self._replace_string(neighbor_string.with_liberty(point))
            self._grid[point] = None
            self._hash ^= zobrist.HASH_CODE[point, string.color]
    
    def _replace_string(self, new_string: GoString) -> None:
        for point in new_string.stones:
            self._grid[point] = new_string

    def place_stone(self, player: Player, point: Point) -> GoString:
        assert self.is_on_grid(point)
        assert self._grid.get(point) is None  # Make sure point is unoccupied
        adjacent_same_color: List[GoString] = []
        adjacent_opposite_color: List[GoString] = []
        liberties: List[Point] = []

        for neighbor in point.neighbors():
            if not self.is_on_grid(neighbor):
                continue
            neighbor_string = self._grid.get(neighbor)
            if neighbor_string is None:
                liberties.append(neighbor)
            elif neighbor_string.color == player:
                if neighbor_string not in adjacent_same_color:
                    adjacent_same_color.append(neighbor_string)
            else:
                if neighbor_string not in adjacent_opposite_color:
                    adjacent_opposite_color.append(neighbor_string)
        new_string = GoString(player, [point], liberties)

        for same_color_string in adjacent_same_color:
            new_string = new_string.merged_with(same_color_string)
        for new_string_point in new_string.stones:
            self._grid[new_string_point] = new_string
        self._hash ^= zobrist.HASH_CODE[point, player]
        for other_color_string in adjacent_opposite_color:
            replacement = other_color_string.without_liberty(point)
            if replacement.num_liberties:
                self._replace_string(other_color_string.without_liberty(point))
            else:
                self._remove_string(other_color_string)
        for other_color_string in adjacent_opposite_color:
            if other_color_string.num_liberties == 0:
                self._remove_string(other_color_string)
        return new_string
    
    def zobrist_hash(self) -> int:
        return self._hash


class GameState():
    def __init__(self, board: Board, next_player: Player, previous: Optional[GameState], move: Optional[Move]):
        self.board = board
        self.next_player = next_player
        self.previous_state = previous
        if previous is None:
            self.previous_states: FrozenSet[Tuple[Player, int]] = frozenset()
        else:
            self.previous_states = frozenset(
                previous.previous_states | {(previous.next_player, previous.board.zobrist_hash())}
            )
        self.last_move = move

    @property
    def situation(self) -> Tuple[Player, Board]:
        return (self.next_player, self.board)

    def apply_move(self, move: Move) -> GameState:
        if isinstance(move, Play):
            next_board = copy.deepcopy(self.board)
            next_board.place_stone(self.next_player, move.point)
        else:
            next_board = self.board
        return GameState(next_board, self.next_player.other, self, move)

    @classmethod
    def new_game(cls, board_size: int) -> GameState:
        board = Board(board_size, board_size)
        return GameState(board, Player.black, None, None)

    def is_move_self_capture(self, player: Player, move: Move) -> bool:
        if not isinstance(move, Play):
            return False
        next_board = copy.deepcopy(self.board)
        return next_board.place_stone(player, move.point).num_liberties == 0

    def does_move_violate_ko(self, player: Player, move: Move) -> bool:
        if not isinstance(move, Play):
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        next_situation = (player.other, next_board.zobrist_hash())
        return next_situation in self.previous_states

    def is_valid_move(self, move: Move) -> bool:
        if self.is_over():
            return False
        if isinstance(move, Pass) or isinstance(move, Resign):
            return True
        return self.board.get(move.point) is None and \
            not self.is_move_self_capture(self.next_player, move) and \
            not self.does_move_violate_ko(self.next_player, move)

    def is_over(self) -> bool:
        if self.last_move is None or self.previous_state is None:
            return False
        if isinstance(self.last_move, Resign):
            return True
        second_last_move = self.previous_state.last_move
        if second_last_move is None:
            return False
        return isinstance(self.last_move, Pass) and isinstance(second_last_move, Pass)

