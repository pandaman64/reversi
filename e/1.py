import rev.game as g
import numpy as np

def initial_board():
    b = g.Player.black.value
    w = g.Player.white.value
    board = np.zeros((8,8))
    board[3:5,3:5] = np.array([[w, b], [b, w]])
    return board

def initialize_game():
  return g.GameState(initial_board(), g.Player.black)
  
def initial_zero_board():
    b = g.Player.black.value
    w = g.Player.white.value
    board = np.zeros((8,8))
    return board

def initialize_zero_game():
  return g.GameState(initial_zero_board(), g.Player.black)
  
   

def randomGO(game): #return WIN or LOSE
    sk = 0
    for i in range(0,1000):
        #print(game.visualize(notations=True))
        vms = game.valid_moves_coords()
        vmcount = len(vms)
        #print ("vms",vmcount)
        if vmcount == 0 :
            sk = sk + 1
            game = game.skip_turn()
            if sk == 2:
                break
            continue
        sk = 0
        vmi = vms[np.random.randint(vmcount)]
        game = game.update(vmi[0],vmi[1])
    return game.disc_count()

def montecarlo(game,player):
    prob = 0
    res = randomGO(game)
    if player == g.Player.black:
        if res[0] > res[1]:
            prob += 1
        elif res[1]> res[0]:
            prob -= 1
    if player == g.Player.white:
        if res[0] > res[1]:
            prob -= 1
        elif res[1]> res[0]:
            prob += 1
    return prob

def MC_(game):
    player = game.turn
    vms = game.valid_moves_coords()
    vmcount = len(vms)
    SCORE = np.zeros(vmcount)
    if vmcount == 0:
        return None
    for p in range(100):
        for i in range(vmcount):
            vmi = vms[i]
            game_i = game.update(vmi[0],vmi[1])
            SCORE[i] += montecarlo(game_i,player)
    j = np.argmax(SCORE)
    return vms[j]

if __name__ == "__main__":
    b = g.Player.black.value
    w = g.Player.white.value
    initcount = int(input())
    #print (initcount)
    board = np.zeros((8,8))
    for i in range(initcount):
        bcol , bpos = input().split(' ')
        bwp = g.notation2index(bpos[0],bpos[1])
        #print (bcol,bwp)
        board[bwp[0],bwp[1]] = b if bcol == "b" else w
    bcol = input()
    player = g.Player.black if bcol == 'b' else g.Player.white
    game = g.GameState(board, g.Player.black)
    
    
    "black is first"
    
    while(True):
        #print(game.turn)    
        #print(game.visualize(notations=True)) 
        
        if game.turn == player:
            mc_ = MC_(game)
            #print ("SELECTED :: ",mc_)
            if mc_ == None:
                game = game.skip_turn()
            else:
                game = game.update(mc_[0], mc_[1])
                outstr = g.index2notation(mc_[0], mc_[1])
                print ( 'b' if player == g.Player.black else 'w' , outstr[0]+outstr[1] )
                if len(game.valid_moves_coords()) == 0:
                    game = game.skip_turn()
        else:
            bcol , bpos = input().split(' ')
            bwp = g.notation2index(bpos[0],bpos[1])
            game = game.update(bwp[0],bwp[1])

if __name__ == "__main_1_":
    
    game = g.initialize_game()

    while not game.is_game_over():
        print(game.visualize(notations=True))        
        mc_ = MC_(game)
        print ("SELECTED :: ",mc_)
        if mc_ == None:
            game = game.skip_turn()
        else:
            game = game.update(mc_[0], mc_[1])
        
            
