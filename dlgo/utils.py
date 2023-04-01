from typing import List, Set, Tuple
from rich import print

from .gotypes import Player, Point
from .goboard import Board, Move, Pass, Resign

COLS = 'ABCDEFGHJKLMNOPQRST'
STONE_TO_CHAR = {
    None: ' [dim yellow]·[/dim yellow]',
    Player.black: ' [bold black]#[/bold black]',
    Player.white: ' [bold white]O[/bold white]',
}

def star_points(board_size: int) -> Set[Tuple[int, int]]:
    offset = 4 if board_size >= 13 else 3
    return {(offset, offset), (offset, board_size - offset + 1),
            (board_size - offset + 1, offset), (board_size - offset + 1, board_size - offset + 1), # corners
            (board_size // 2 + 1, board_size // 2 + 1), # center
            (offset, board_size // 2 + 1), (board_size - offset + 1, board_size // 2 + 1), # middle
            (board_size // 2 + 1, offset), (board_size // 2 + 1, board_size - offset + 1)} # middle

def point_from_coords(coords: str) -> Point:
    col = COLS.index(coords[0].upper()) + 1
    row = int(coords[1:])
    return Point(row=row, col=col)

def print_move(player: Player, move: Move) -> None:
    if isinstance(move, Pass):
        move_str = 'passes'
    elif isinstance(move, Resign):
        move_str = 'resigns'
    else:
        move_str = f'{COLS[move.point.col - 1]}{move.point.row}'
    print(f'{player} {move_str}')

def print_board(board: Board) -> None:
    star_points_set = star_points(board.num_rows)
    for row in range(board.num_rows, 0, -1):
        bump = " " if row <= 9 else ""
        line: List[str] = []
        for col in range(1, board.num_cols + 1):
            stone = board.get(Point(row=row, col=col))
            if stone is None and (row, col) in star_points_set:
                line.append(' [bold yellow]·[/bold yellow]')
            else:
                line.append(STONE_TO_CHAR[stone])
        print(f'{bump}{row} {"".join(line)}')
    print('    [bold cyan]' + ' '.join(COLS[:board.num_cols]) + '[/bold cyan]')
