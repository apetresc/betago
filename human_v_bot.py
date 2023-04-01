import argparse

from dlgo.agent import naive
from dlgo.goboard import GameState, Play
from dlgo import gotypes
from dlgo.utils import print_board, print_move, point_from_coords


def main(board_size: int = 19):
    game = GameState.new_game(board_size)
    bot = naive.RandomBot()
    while not game.is_over():
        print_board(game.board)
        if game.next_player == gotypes.Player.black:
            human_move = input('-- ')
            point = point_from_coords(human_move.strip())
            move = Play(point)
        else:
            move = bot.select_move(game)
        print_move(game.next_player, move)
        game = game.apply_move(move)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--board-size', '-n', type=int, default=19)
    args = argparser.parse_args()

    main(board_size=args.board_size)