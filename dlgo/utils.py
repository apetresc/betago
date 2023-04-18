from typing import List, Set, Tuple
from rich import print

from .gotypes import Player, Point
from .goboard import Board, Move, Pass, Resign

COLS = 'ABCDEFGHJKLMNOPQRST'
STONE_TO_CHAR = {
    None: '·',
    Player.black: '#',
    Player.white: 'O',
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
            elif stone is None:
                line.append(' [dim yellow]·[/dim yellow]')
            else:
                line.append(f' [bold {stone}]{STONE_TO_CHAR[stone]}[/bold {stone}]')
        print(f'{bump}{row} {"".join(line)}')
    print('    [bold cyan]' + ' '.join(COLS[:board.num_cols]) + '[/bold cyan]')

def to_ascii(board: Board) -> str:
    star_points_set = star_points(board.num_rows)
    ascii_board: List[str] = []
    for row in range(board.num_rows, 0, -1):
        bump = " " if row <= 9 else ""
        line: List[str] = []
        for col in range(1, board.num_cols + 1):
            stone = board.get(Point(row=row, col=col))
            if stone is None and (row, col) in star_points_set:
                line.append(' ·')
            else:
                line.append(f' {STONE_TO_CHAR[stone]}')
        ascii_board.append(f'{bump}{row} {"".join(line)}')
    ascii_board.append('    ' + ' '.join(COLS[:board.num_cols]))
    return '\n'.join(ascii_board)

def from_ascii(ascii_board: str) -> Board:
    """Create a Board instance from an ASCII representation.
    
    :param str ascii_board: a multiline string equivalent to the output of print_board.
    :return: a Board instance.
    """
    lines = list(map(lambda s: s.strip(' 0123456789'), ascii_board.strip().splitlines()))
    if lines[-1].startswith('A'):
        lines = lines[:-1]
    h, w = len(lines), (len(lines[0]) + 1) // 2
    board = Board(w, h)
    for row, line in enumerate(lines):
        for col, char in enumerate(line.replace(' ', '')):
            if char == '#':
                board.place_stone(Player.black, Point(row=h - row, col=col + 1))
            elif char == 'O':
                board.place_stone(Player.white, Point(row=h - row, col=col + 1))
    return board
