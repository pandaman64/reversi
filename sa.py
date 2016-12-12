from multiprocessing import Pool
import numpy as np
import game as g
import random
import util

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

def next_move(state, player, debug=False):
  totalDisc = g.player_disc_total(state.board, g.Player.black) + g.player_disc_total(state.board, g.Player.white)
  n = int(25  * (1 + np.exp(totalDisc / 16)))
  #print(n)  
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

#import cProfile
#cProfile.run('next_move(g.initialize_game(), g.Player.black)')
if __name__ == '__main__':
  game = util.read_game()
  me = util.str2player(input())
  while(not game.is_game_over()):
    if(game.no_valid_moves()):
      game.skip_turn()
      continue

    if(game.turn == me):
      x,y = next_move(game,me)
      game = game.update(x,y)
      print(util.stringify(x,y,me))
    elif(game.turn == g.opponent(me)):
      x,y,p = util.parse(input())
      game = game.update(x,y)
    else:
      raise Exception("rejsf")
#  print(next_move(g.initialize_game(), g.Player.black))

