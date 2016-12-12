import game as g
import ai
import util
import subprocess
import argparse

def new_player(cmd,player):
  p = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
  p.stdin.write('4\n'.encode())
  p.stdin.write('w e4\n'.encode())
  p.stdin.write('b e5\n'.encode())
  p.stdin.write('w d5\n'.encode())
  p.stdin.write('b d4\n'.encode())
  
  if player == g.Player.black:
    p.stdin.write('b\n'.encode())
  elif player == g.Player.white:
    p.stdin.write('w\n'.encode())
  else:
    raise Exception("haH?")

  p.stdin.flush()
  return p

def main():
  parser = argparse.ArgumentParser('super ultra hyper miracle othello matcher')
  parser.add_argument('black',default='monte_client.py')
  parser.add_argument('white',default='monte_client.py')
  args = parser.parse_args()

  black = new_player('python ' + args.black,g.Player.black)
  white = new_player('python ' + args.white,g.Player.white)

  game = g.initialize_game()
  util.push(game,'w e4')
  util.push(game,'b e5')
  util.push(game,'w d5')
  util.push(game,'b d4')

  while(not game.is_game_over()):
    print(game.visualize(notations=True))
    #input()
    if(game.no_valid_moves()):
      game.skip_turn()
      continue
    
    if(game.turn == g.Player.black):
      player = black
      opp = white
    elif(game.turn == g.Player.white):
      player = white
      opp = black
    else:
      raise Exception("aaaaaaaaaa")

    line = player.stdout.readline().decode() # includes \n
    x,y,p = util.parse(line)
    game = game.update(x,y)
    print(line,end="")
    opp.stdin.write(line.encode())
    opp.stdin.flush()

  if game.has_won(g.Player.black):
    print(args.black + " win")
  elif game.has_won(g.Player.white):
    print(args.white + " win")
  else:
    print("tie")
  
if __name__ == "__main__":
  main()
