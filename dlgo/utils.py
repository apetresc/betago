from .gotypes import Player, Point
from .goboard_slow import Board, Move

COLS = 'ABCDEFGHJKLMNOPQRST'
STONE_TO_CHAR = {
    None: ' .',
    Player.black: ' #',
    Player.white: ' O'
}

def print_move(player: Player, move: Move) -> None:
    if move.is_pass:
        move_str = 'passes'
    elif move.is_resign:
        move_str = 'resigns'
    else:
        assert move.point is not None # TODO fix the type of Move
        move_str = f'{COLS[move.point.col - 1]}{move.point.row}'
    print(f'{player} {move_str}')

def print_board(board: Board) -> None:
    for row in range(board.num_rows, 0, -1):
        bump = " " if row <= 9 else ""
        line = []
        for col in range(1, board.num_cols + 1):
            stone = board.get(Point(row=row, col=col))
            line.append(STONE_TO_CHAR[stone])
        print(f'{bump}{row} {"".join(line)}')
    print('    ' + ' '.join(COLS[:board.num_cols]))
