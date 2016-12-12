# -*- coding: utf-8 -*-
import numpy as np
import game as g
import ai


black = 1
white = -1


def getInput():
    color,num = input().split()
    x = ord(num[0]) - ord('a')
    y = ord(num[1]) - ord('1')
    if color == 'b':
        color = black
    else:
        color = white
    return (x,y,color)

def setOutput(x,y,Player):
    playerChar = 'b'
    if Player==-1:
        playerChar = 'w'
    x = chr(x+ord('a'))
    y = chr(y+ord('1'))
    print(playerChar+' '+x+y)
    
val = np.array([[ 30,-12,  0, -1, -1,-10,-12, 30],
               [-12,-15, -3, -3, -3, -3,-15,-12],
               [  0, -3,  0, -1, -1,  0, -3,  0],
               [ -1, -3, -1, -1, -1, -1, -3, -1],
               [ -1, -3, -1, -1, -1, -1, -3, -1],
               [  0, -3,  0, -1, -1,  0, -3,  0],
               [-12,-15, -3, -3, -3, -3,-15,-12],
               [ 30,-12,  0, -1, -1,-10,-12, 30]])
       
def evaluation(mygame, Player):
    return (val*(mygame.board==Player) * Player).sum()

def myAI(mygame, Player,turn):
    (x, y) = (0, 0)
    maxVal = -999999
    if turn <= 32:
        #print("use eva")
        for i in mygame.valid_moves_coords():
            tmpGame = mygame.update(i[0],i[1])
            tmpval = evaluation(tmpGame, Player)
            #print("tmpval = {}, (x,y)=({},{})".format(tmpval,i[0],i[1]))
            if maxVal < tmpval:
                maxVal = tmpval
                x = i[0]
                y = i[1]
    else:
        #print("use monte")
        x,y = ai.next_move(mygame, g.Player.black if turn%2==1 else g.Player.white)
    return x,y
'''
if __name__ == '__main__':
    
    firstDisc = input()
    firstDisc = ord(firstDisc) - ord('0')
    board = np.zeros([8,8])
    for i in range(4):
        x,y,color = getInput()
        board[x][y] = color
    game = g.GameState(board, color)
        
    
    myColor = input()
    if color == 'b':
        color = black
    else:
        color = white
    
    
    turn = 1
    Player = black
    mygame = g.initialize_game()
    print("hello")
    while not mygame.is_game_over():
        #print("hello")
        if turn%2==1:
            x,y = myAI(mygame,Player,turn)
        else:
            x,y = ai.next_move(mygame, g.Player.white)
        mygame = mygame.update(x, y)
        print()
        print(mygame.visualize(notations=True))
        turn+=1
    print("winner is {}".format(mygame.game_outcome()))
'''

if __name__ == '__main__':
    firstDisc = input()
    firstDisc = ord(firstDisc) - ord('0')
    board = np.zeros([8,8])
    for i in range(4):
        x,y,color = getInput()
        board[x][y] = color
    game = g.GameState(board, color)
        
    
    myColor = input().strip()
    if color == 'b':
        color = black
    else:
        color = white
    
    
    turn = 1
    Player = black
    mygame = g.initialize_game()
    turnPlayer = 1 if Player==black else -1
    while not mygame.is_game_over():
        #print("hello")
        (x,y,color) = (0,0,0)
        if turn%2==turnPlayer:
            x,y = myAI(mygame,Player,turn)
            setOutput(x,y,Player)
        else:
            x,y,color = getInput()#ai.next_move(mygame, g.Player.white)
        mygame = mygame.update(x, y)
        #print()
        #print(mygame.visualize(notations=True))
        turn+=1
    #print("winner is {}".format(mygame.game_outcome()))
        
    
    
    
