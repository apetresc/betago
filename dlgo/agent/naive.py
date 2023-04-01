import random
from typing import List

from .base import Agent
from .helpers import is_point_an_eye
from ..goboard import GameState, Move, Pass, Play
from ..gotypes import Point


class RandomBot(Agent):
    def select_move(self, game_state: GameState) -> Move:
        """Choose a random valid move that preserves our own eyes."""
        candidates: List[Point] = []
        for r in range(1, game_state.board.num_rows + 1):
            for c in range(1, game_state.board.num_cols + 1):
                candidate = Point(row=r, col=c)
                if game_state.is_valid_move(Play(candidate)) and \
                        not is_point_an_eye(game_state.board, candidate, game_state.next_player):
                    candidates.append(candidate)
        if not candidates:
            return Pass()
        return Play(random.choice(candidates))
