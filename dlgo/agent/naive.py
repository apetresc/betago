import random

from .base import Agent
from .helpers import is_point_an_eye
from ..goboard import GameState, Move, Pass, Play


class RandomBot(Agent):
    def select_move(self, game_state: GameState) -> Move:
        """Choose a random valid move that preserves our own eyes."""
        candidates = [
            point
            for point in game_state.legal_moves()
            if not is_point_an_eye(game_state.board, point, game_state.next_player)
        ]
        if not candidates:
            return Pass()
        return Play(random.choice(candidates))
