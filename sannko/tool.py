import numpy as np
from scipy import ndimage
from enum import Enum
import sys

class Player(Enum):
  black = 1
  white = -1

def opponent(player):
  return Player(-player.value)

def empty_cells(board):
  return board == 0

def initial_board():
  b = Player.black.value
  w = Player.white.value
  board = np.zeros((8,8))
  board[3:5,3:5] = np.array([[w, b], [b, w]])
  return board

def bounds_check(x, y):
  return x >= 0 and x < 8 and y >= 0 and y < 8

surrounding_coords = [(i, j) for i in [-1, 0, 1] for j in [-1, 0, 1] if i != 0 or j != 0]

def place_disc(board, turn, x, y):
  if board[y,x] != 0:
    raise Exception('cell not empty', (x, y))

  bws = np.zeros((10,10))
  bws[1:9,1:9] = board.copy()
  (x, y) = (x+1, y+1)
  # board with sentinels

  opp = opponent(turn)

  for i, j in surrounding_coords:
    (xp, yp) = (x+i, y+j)
    cl = [(x,y)]
    while bws[yp,xp] == opp.value:
      cl.append((xp,yp))
      (xp, yp) = (xp+i, yp+j)
      if bws[yp,xp] == 0:
        break;
      if bws[yp,xp] == turn.value:
        for ux, uy in cl:
          bws[uy,ux] = turn.value
        break
  return bws[1:9,1:9]

def playable(board, turn):
  bws = np.zeros((10,10))
  bws[1:9,1:9] = board
  # board with sentinels

  opp = opponent(turn)

  res = np.zeros((8,8), dtype=bool)

  for x, y in [(x, y) for x in range(1,9) for y in range(1,9) if bws[y,x] == 0]:
    for i, j in surrounding_coords:
      if res[y-1,x-1]:
        break
      (xp, yp) = (x+i, y+j)
      while bws[yp,xp] == opp.value:
        (xp, yp) = (xp+i, yp+j)
        if bws[yp,xp] == 0:
          break
        if bws[yp,xp] == turn.value:
          res[y-1,x-1] = True
          break
  return res

def index2notation(x, y):
  return (chr(x + ord('a')), chr(y + ord('1')))

def notation2index(alpha, num):
  return (ord(alpha) - ord('a'), ord(num) - ord('1'))

def player_disc_total(board, turn):
  return np.sum(board == turn.value)

class GameState(object):
  """Represents the state of a game at a given point in time."""
  def __init__(self, board, turn):
    self.board = board
    self.__playable = None
    self.__playable_coords = None
    self.turn = turn

  def update(self, x, y):
    new_board = place_disc(self.board, self.turn, x, y)
    return GameState(new_board, opponent(self.turn))

  def skip_turn(self):
    return GameState(self.board, opponent(self.turn))

  def visualize(self, notations=False):
    res = self.turn.name + "'s turn\n"
    pl = self.valid_moves()
    if notations:
      res += "*abcdefgh*\n"
    for y in range(8):
      if notations:
        res += chr(ord('1') + y)
      for x in range(8):
        if self.board[y,x] == Player.black.value:
          res += "b"
        elif self.board[y,x] == Player.white.value:
          res += "w"
        elif pl[y,x]:
          res += "*"
        else:
          res += "_"
      if notations:
        res += chr(ord('1') + y)
      res += "\n"
    if notations:
      res += "*abcdefgh*\n"
    return res

  def is_game_over(self):
    return self.no_valid_moves() and self.skip_turn().no_valid_moves()

  def valid_moves(self):
    if self.__playable is None:
      self.__playable = playable(self.board, self.turn)
    return self.__playable

  def valid_moves_coords(self):
    if self.__playable_coords is None:
      self.__playable_coords = [(x, y) for x in range(8) for y in range(8) if self.is_valid_move(x, y)]
    return self.__playable_coords

  def is_valid_move(self, x, y):
    return self.valid_moves()[y,x]

  def valid_move_count(self):
    return np.sum(self.valid_moves())

  def no_valid_moves(self):
    return self.valid_move_count() == 0

  def is_cell_empty(self, x, y):
    return self.board[y, x] == 0

  def disc_owner(self, x, y):
    return Player(self.board[y, x])

  def disc_count(self):
    b = player_disc_total(self.board, Player.black)
    w = player_disc_total(self.board, Player.white)
    return (b, w)

  def game_outcome(self):
    (b, w) = self.disc_count()
    if b > w:
      return Player.black.name
    elif b < w:
      return Player.white.name
    else:
      return 'tie'

  def has_won(self, player):
    return self.is_game_over() and self.game_outcome() == player.name

def initialize_game():
  return GameState(initial_board(), Player.black)

if __name__ == '__main__':
  game = initialize_game()
  print(game.visualize(notations=True))
  while not game.is_game_over():
    (x, y) = (0, 0)
    while True:
      (alpha, num) = input("input: ")
      print((alpha, num))
      if num >= '1' and num <= '8' and alpha >= 'a' and alpha <= 'h':
        (x, y) = notation2index(alpha, num)
        break
    game = game.update(x, y)
    print()
    print(game.visualize(notations=True))
