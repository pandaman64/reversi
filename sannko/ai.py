import numpy as np

from tool import *

from conv_monte import conv_monte
from new_monte import new_monte

def ai(game, my_turn, ai_name=0):
    board = game.board
    if my_turn == Player['white']:
        board = board[::-1]
        b_ind = np.where(board==1)
        w_ind = np.where(board==-1)
        board[b_ind] = -1
        board[w_ind] = 1
    ai_game = initialize_game()
    ai_game.board = board
    ai_exe = [new_monte, conv_monte][ai_name]
    x, y = ai_exe(ai_game, Player['black'])
    if my_turn == Player['white']:
        y = 7-y
    return x, y
