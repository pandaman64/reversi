import game as g
import ai

def read_game():
  game = g.initialize_game()
  count = int(input())
  for i in range(count):
    push(game,input())
  game.turn = g.Player.black
  return game

def str2player(s):
  if s == "b":
    return g.Player.black
  elif s == "w":
    return g.Player.white
  else:
    raise Exception("? {0}".format(s))

def parse(line):
  p,pos = line.strip().split()
  p = str2player(p)
    
  if len(pos) < 2:
    raise Exception("ssosome wrong with {0}".format(line))

  x,y = g.notation2index(pos[0],pos[1])
  return (x,y,p)

def stringify(x,y,p):
  a,i = g.index2notation(x,y)
  if p == g.Player.black:
    return "b {0}{1}".format(a,i)
  elif p == g.Player.white:
    return "w {0}{1}".format(a,i)
  else:
    raise Exception("wakari")

def push(game,line):
  x,y,p = parse(line)
  game.push(x,y,p)


