from multiprocessing import Pool
import game as g
import random

def playout(state, player, coord):
  (cx, cy) = coord
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

def next_move(state, player):
  n = 100
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
  print(prob)
  return prob[-1][1]

import cProfile
if __name__ == '__main__':
#  cProfile.run('next_move(g.initialize_game(), g.Player.black)')
  print(next_move(g.initialize_game(), g.Player.black))

