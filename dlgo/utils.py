from typing import List

from .gotypes import Player, Point
from .goboard_slow import Board, Move, Pass, Resign

COLS = 'ABCDEFGHJKLMNOPQRST'
STONE_TO_CHAR = {
    None: ' ·',
    Player.black: ' #',
    Player.white: ' O'
}

def print_move(player: Player, move: Move) -> None:
    if isinstance(move, Pass):
        move_str = 'passes'
    elif isinstance(move, Resign):
        move_str = 'resigns'
    else:
        move_str = f'{COLS[move.point.col - 1]}{move.point.row}'
    print(f'{player} {move_str}')

def print_board(board: Board) -> None:
    for row in range(board.num_rows, 0, -1):
        bump = " " if row <= 9 else ""
        line: List[str] = []
        for col in range(1, board.num_cols + 1):
            stone = board.get(Point(row=row, col=col))
            line.append(STONE_TO_CHAR[stone])
        print(f'{bump}{row} {"".join(line)}')
    print('    ' + ' '.join(COLS[:board.num_cols]))
