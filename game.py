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

def place_disc(board, turn, x, y):
  if board[y,x] != 0:
    raise Exception('cell not empty', (x, y))

  bws = np.zeros((10,10))
  bws[1:9,1:9] = board.copy()
  (x, y) = (x+1, y+1)
  # board with sentinels

  opp = opponent(turn)

  for i in [-1, 0, 1]:
    for j in [-1, 0, 1]:
      if i == 0 and j == 0:
        continue
      (xp, yp) = (x+i, y+j)
      cl = [(x,y)]
      while bws[yp,xp] == opp.value:
        cl.append((xp,yp))
        (xp, yp) = (xp+i, yp+j)
        if bws[yp,xp] == 0:
          break;
        if bws[yp,xp] == turn.value:
          print(cl)
          for ux, uy in cl:
            bws[uy,ux] = turn.value
          break
  return bws[1:9,1:9]

def playable(board, turn):
  bws = np.zeros((10,10))
  bws[1:9,1:9] = board
  # board with sentinels

  opp = opponent(turn)

  f = np.array([[1,1,1],[1,0,1],[1,1,1]])
  cd = ndimage.convolve(bws == opp.value, f, mode='constant', cval=0)
  cs = np.logical_and(cd > 0, empty_cells(bws))

  res = np.zeros((8,8), dtype=bool)

  for x in range(1,9):
    for y in range(1,9):
      if not cs[y,x]:
        continue
      for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
          if i == 0 and j == 0:
            continue
          (xp, yp) = (x+i, y+j)
          while bws[yp,xp] == opp.value:
            (xp, yp) = (xp+i, yp+j)
            if bws[yp,xp] != opp.value: # either empty(0) or player's color
              res[y-1,x-1] |= bws[yp,xp] == turn.value
              break
  return res

def index2notation(x, y):
  return (chr(x + ord('a')), chr(y + ord('1')))

def notation2index(alpha, num):
  return (ord(alpha) - ord('a'), ord(num) - ord('1'))

class GameState(object):
  """Represents the state of a game at a given point in time."""
  def __init__(self, board, turn):
    self.board = board
    self.turn = turn

  def update(self, x, y):
    self.board = place_disc(self.board, self.turn, x, y)
    self.turn = opponent(self.turn)

  def visualize(self, notations=False):
    res = self.turn.name + "'s turn\n"
    pl = playable(self.board, self.turn)
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
    w = np.sum(playable(self.board, Player.white)) == 0
    b = np.sum(playable(self.board, Player.black)) == 0
    return w and b

  def is_valid_move(self, x, y):
    return playable(self.board, self.turn)[y,x]

  def game_outcome(self):
    w = np.sum(self.board == Player.white.value)
    b = np.sum(self.board == Player.black.value)
    if w > b:
      return Player.white.name
    elif w < b:
      return Player.black.name
    else:
      return 'tie'

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
    game.update(x, y)
    print()
    print(game.visualize(notations=True))

