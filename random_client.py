import game as g
import ai
import util
import sys
import random

def main():
  # read are
  game = util.read_game()
  me = util.str2player(input())

  while(not game.is_game_over()):
    #sys.stderr.write(str(me) + '\n')
    #sys.stderr.write(game.visualize(notations=True))
    if(game.no_valid_moves()):
      game.skip_turn()
      continue
    
    if(game.turn == me):
      #x,y = ai.next_move(game,me)
      valid_moves = game.valid_moves_coords()
      x,y = random.choice(valid_moves)
      game = game.update(x,y)
      #sys.stderr.write(util.stringify(x,y,me) + '\n')
      print(util.stringify(x,y,me))
    elif(game.turn == g.opponent(me)):
      x,y,p = util.parse(input())
      game = game.update(x,y)
    else:
      raise Exception("wrongwrong")

if __name__ == "__main__":
  main()
