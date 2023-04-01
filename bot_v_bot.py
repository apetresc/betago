from dlgo.agent import naive
from dlgo.goboard_slow import GameState
from dlgo.gotypes import Player
from dlgo.utils import print_board, print_move


def main():
    board_size = 19
    game = GameState.new_game(board_size)
    bots = {
            Player.black: naive.RandomBot(),
            Player.white: naive.RandomBot()
    }

    while not game.is_over():
        print_board(game.board)
        bot_move = bots[game.next_player].select_move(game)
        print_move(game.next_player, bot_move)
        game = game.apply_move(bot_move)


if __name__ == '__main__':
    main()
