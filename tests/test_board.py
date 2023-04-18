from dlgo.goboard import GameState, Play
from dlgo.gotypes import Player, Point
from dlgo.utils import from_ascii

def test_self_capture_small():
    game = GameState(from_ascii("""
    5 . . O # .
    4 . . O # #
    3 O O . O O
    2 # # O . .
    1 . # . . .
      A B C D E
    """), next_player=Player.black, previous=None, move=None)
    assert game.is_move_self_capture(Player.black, Play(Point(row=5, col=5)))
    assert not game.is_valid_move(Play(Point(row=5, col=5)))
    assert not game.is_move_self_capture(Player.black, Play(Point(row=1, col=1)))
    assert game.is_valid_move(Play(Point(row=1, col=1)))

def test_self_capture_big():
    game = GameState(from_ascii("""
        19  O O · O · O O · O O O # # · # # · # #
        18  O O O O O O O O O O # # # # # # # # #
        17  O O O O O O O O O # # · # # # O # O O
        16  O O # O O # # O # # · # # # # O O O O
        15  O # # # # # # # # # # # # # O O O O O
        14  # # # · # # # # # · # # # # O · O O ·
        13  # # # # # · # · # # # # · # O O O O O
        12  # # # # # # # # # # # · # # # # O O O
        11  # # · # # # O O O # # # # O O O O O ·
        10  # # # · # O O · O # # # O O O # # O O
         9  # # # # # # O O O O O O O O O # # # #
         8  # · # # · # O · O O O O · O O # # · O
         7  # # # # # # # O O O O O O O O # O O O
         6  # # O # # · # O · O O O O · O O # O O
         5  O O O O # # # # O O O · O O O # # O O
         4  · O # # # · # O O O O O O # O O # # #
         3  # O O O # # # # O O · O O # # # # O O
         2  O O O O # # # # # O O # # # # # O O O
         1  O O # # # · # · # # O # # # · # O O ·
            A B C D E F G H J K L M N O P Q R S T"""),
           next_player=Player.black,
           previous=None,
           move=None)
    assert not game.is_move_self_capture(Player.black, Play(Point(row=1, col=19)))
    assert game.is_valid_move(Play(Point(row=1, col=19)))