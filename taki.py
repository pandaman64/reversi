from multiprocessing import Pool
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
  taple = state.disc_count()
  n = 0
  if taple[0] + taple[1] >= 45:
      n = 600
  elif taple[0] + taple[1] >= 35:
      n = 300
  elif taple[0] + taple[1] >= 20:
      n = 200
  else:
      n = 100
  totals = {}
  wins = {}
  moves = state.valid_moves_coords()
  coords = [random.choice(moves) for i in range(n)]
  result = monte_carlo(state, player, coords)
  
  coordlist = [[0,0], [0,7], [7,0], [7,7]]
  _coordlist = [[1,0], [1,1], [0,1], [1,7], [1,6], [0,6], [6,0], [6,1], [7,1], [6,7], [6,6], [7,6]]
  num = len(coordlist)
  flag = 0
  for j in range(3):
      for i in range(num):
          if state.is_valid_move(coordlist[i][0],coordlist[i][1]):
              return coordlist[i]
      for i in range(n):
        totals[coords[i]] = totals.get(coords[i], 0) + 1
        wins[coords[i]] = wins.get(coords[i], 0) + result[i]
      prob = []
      for key in totals.keys():
        prob.append((wins.get(key, 0) /  totals[key], key))
      prob = sorted(prob)
      if debug:
        print(prob)
      for k in _coordlist:
          if prob[-1][1] == k:
              flag = 1
      if flag == 0:
          break
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
