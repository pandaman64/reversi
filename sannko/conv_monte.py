import numpy as np
from multiprocessing import Pool
import random

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

def conv_monte(state, player, debug=False):
  n = 60
  if sum(state.disc_count()) >= 20:
      n = 100
  if sum(state.disc_count()) >= 30:
      n = 150
  if sum(state.disc_count()) >= 40:
      n = 200
  if sum(state.disc_count()) >= 50:
      n = 400
  if sum(state.disc_count()) >= 60:
      n = 800

  totals = {}
  wins = {}
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
  return prob[-1][1]
