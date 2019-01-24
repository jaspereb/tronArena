'''Sample bot, will choose the first non losing move assuming the opponent always
    goes left (if p1) or right (if p2)'''

import numpy as np
import random
import copy

def getAction(game, playerNum):
    possibleActions = ['left','right','up','down']
    random.shuffle(possibleActions)
    
    #One step single-player lookahead. Take the first non-losing move
    for action in possibleActions:
        gameCopy = copy.deepcopy(game)
        gameCopy.VERBOSE = 0
        if(playerNum == 1):
            gameCopy.step(action, 'left')
            if(gameCopy.winner == 'player2' or gameCopy.winner == 'draw'): #A losing move
                print("bot 1 skipping " + action)
                continue
        elif(playerNum == 2):
            gameCopy.step('right', action)
            if(gameCopy.winner == 'player1' or gameCopy.winner == 'draw'):
                continue
        else:
            print("ERROR: Invalid player num")
            
        return action
        
    print("Bot {} found no non-losing moves".format(playerNum))
    return 'left'
