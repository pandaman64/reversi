import numpy as np
from multiprocessing import Pool
import random
import time
from copy import deepcopy

score = np.array([[120, -20, 20, 5, 5, 20, -20, 120],
                  [-20, -40, -5, -5, -5, -5, -40, -20],
                  [20, -5, 15, 3, 3, 15, -5, 5],
                  [5, -5, 3, 3, 3, 3, -5, 5],
                  [5, -5, 3, 3, 3, 3, -5, 5],
                  [20, -5, 15, 3, 3, 15, -5, 5],
                  [-20, -40, -5, -5, -5, -5, -40, -20],
                  [120, -20, 20, 5, 5, 20, -20, 120]])

def playout(state, player, coord):
  (cx, cy) = coord
  state = state.update(cx, cy)
  while True:
    if state.no_valid_moves():
      state = state.skip_turn()
      if state.no_valid_moves():
        break
    else:
      (cx, cy) = random.choice(state.valid_moves_coords())
      state = state.update(cx, cy)
  if state.has_won(player):
    return 1
  else:
    return 0

def monte_carlo(state, player, coords):
  pool = Pool()
  results = [pool.apply_async(playout, [state, player, c]) for c in coords]
  pool.close()
  pool.join()
  return [r.get() for r in results]

def score_check(game):
  max_score = -10000
  max_index = []
  for x, y in game.valid_moves_coords():
      if score[x, y] > max_score:
          max_score = score[x, y]
          max_index = [(x, y)]
      elif score[x, y] == max_score:
          max_index.append((x, y))
  min_score = 10000
  min_index = []
  for xm, ym in max_index:
      local_max = -10000
      trygame = deepcopy(game)
      trygame = trygame.update(xm, ym)
      for x, y in trygame.valid_moves_coords():
          if score[x, y] > local_max:
              local_max = score[x, y]
      if local_max < min_score:
          min_index = [(xm, ym)]
      elif local_max == min_score:
          min_index.append((xm, ym))
  return min_index

before_time = 0
before_n = 0

def new_monte(state, player, debug=False):
  global before_time, before_n
  start = time.time()
  n = 55
  if sum(state.disc_count()) >= 20:
      n = int(before_n * 0.9 / before_time)

  totals = {}
  wins = {}
  if sum(state.disc_count()) < 10:
      moves = score_check(deepcopy(state))
  else:
      moves = state.valid_moves_coords()
  coords = [random.choice(moves) for i in range(n)]

  result = monte_carlo(state, player, coords)

  for i in range(n):
    totals[coords[i]] = totals.get(coords[i], 0) + 1
    wins[coords[i]] = wins.get(coords[i], 0) + result[i]
  prob = []
  for key in totals.keys():
    prob.append((wins.get(key, 0) /  totals[key], key))
  prob = sorted(prob)
  if debug:
    print(prob)
  before_time = time.time() - start
  before_n = n
  return prob[-1][1]
