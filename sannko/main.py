import numpy as np
from copy import deepcopy
import argparse
import time

from ai import ai
from tool import *

parser = argparse.ArgumentParser(description=\
                  'reversi ai')
parser.add_argument('--visualize', '-v', default=False,
                    help='visualize reversi board')
parser.add_argument('--debug', '-db', default=False,
                    help='debug')
parser.add_argument('--time', '-t', default=False,
                    help='keep time')
parser.add_argument('--disc_num', '-dn', default=False,
                    help='number of discs on the current board')
args = parser.parse_args()


str2num = {'b':1, 'w':-1}
num2str = {1:'b', -1:'w'}

def input_action(game):
    turn, (alpha, num) = input().split(' ')
    (x, y) = notation2index(alpha, num)
    return game.update(x, y)

def ai_action(game, ai_name=0):
    if args.time:
        start = time.time()
    current_turn = game.turn
    (x, y) = ai(deepcopy(game), current_turn, ai_name)
    game = game.update(x, y)
    alpha, num = index2notation(x, y)
    print('%s %s%s' % (num2str[current_turn.value], alpha, num))
    if args.disc_num:
        print('(b, w) = (%s, %s)' % game.disc_count())
    if args.time:
        print('elapsed_time: %f' %\
              (time.time() - start))
    return game

if __name__ == '__main__':
    game = initialize_game()
    init_num = int(input())
    init_board = np.zeros((8, 8))
    for i in range(init_num):
        turn, (alpha, num) = input().split(' ')
        (x, y) = notation2index(alpha, num)
        init_board[y, x] = str2num[turn]
    game.board = init_board
    my_turn = Player(str2num[input()])
    if my_turn == Player['white']:
        if not args.debug:
            game = input_action(game)
        else:
            game = ai_action(game)
        if args.visualize:
            print(game.visualize(notations=True))
    while True:
        if not game.is_game_over():
            if not game.no_valid_moves():
                game = ai_action(game)
            else:
                game = game.skip_turn()
            if args.visualize:
                print(game.visualize(notations=True))
        if not game.is_game_over():
            if not game.no_valid_moves():
                if not args.debug:
                    game = input_action(game)
                else:
                    game = ai_action(game, ai_name=1)
            else:
                game = game.skip_turn()
            if args.visualize:
                print(game.visualize(notations=True))
        else:
            break
