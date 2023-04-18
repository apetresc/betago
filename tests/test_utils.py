import dlgo.utils as utils

def test_from_ascii():
    ascii_board = '''
19  # # # # # # O O O O O O O O O · O O O
18  · # · # # # O O O # O O O · O O O # #
17  # # # # · # # # # # O O O O · O O # #
16  # # # # # # # # · # # # O O O O # # #
15  # O # O O # # # # # # # # # O # # # #
14  # O O O O O # # · # O O O O O # # # #
13  # # O O · O O # # # # O O O O # # · #
12  # · # O O # O O # # # # # # O # # # #
11  # # # O O # # O O O # # O # O # # # ·
10  # # O O · O # # # # O O O O # # # # #
 9  · # O O O O O # · # O O · O # # # # #
 8  # # O # # # O # # # # # O O # # # · #
 7  # # O # # O O # # # # # # # # # # # #
 6  # # # # O O O O # # O # # # # · # # #
 5  O # # O O · O O O # O O O O # # # # #
 4  O O # O O O O O # # # # O # # # # # #
 3  O O O · O O # # # # # # O # # # O # ·
 2  O O O O O O O O O O O O O O O O O # #
 1  O O O · O O O O · O O O O O O O # # #
    A B C D E F G H J K L M N O P Q R S T
    '''.strip()
    board = utils.from_ascii(ascii_board)
    assert board.num_rows == 19
    assert board.num_cols == 19
    assert utils.to_ascii(board) == ascii_board