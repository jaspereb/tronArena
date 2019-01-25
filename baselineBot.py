'''Sample bot, it will perform one step lookahead maximisation. Use this as a baseline'''

import numpy as np
import random
import copy

def getAction(game, playerNum):
    
    possibleActions = ['left','right','up','down']
    
    #Uncomment this line to avoid the snakes doing laps forever
#    random.shuffle(possibleActions)
    
    #Store the action values for each possible action
    V = np.ones((4,1))
    actionIndex = 0
    
    #For each possible action, we assign it a value based on the minimum reward
    # seen at that action for all possible opponent actions
    for playerAction in possibleActions:
        for opponentAction in possibleActions:
            gameCopy = copy.deepcopy(game)
            gameCopy.VERBOSE = 0    
            if(playerNum == 1):
                gameCopy.step(playerAction, opponentAction)
                if(gameCopy.winner == 'player2'): #A loss
                    V[actionIndex] = min(V[actionIndex],-1)
                elif(gameCopy.winner == 'draw'):
                    V[actionIndex] = min(V[actionIndex],-0.1)
                elif(gameCopy.winner == None): #Non terminal
                    V[actionIndex] = min(V[actionIndex],0)
                elif(gameCopy.winner == 'player1'): #A win
                    V[actionIndex] = min(V[actionIndex],1)
            elif(playerNum == 2):
                gameCopy.step(opponentAction, playerAction)
                if(gameCopy.winner == 'player1'): #A loss
                    V[actionIndex] = min(V[actionIndex],-1)
                elif(gameCopy.winner == 'draw'):
                    V[actionIndex] = min(V[actionIndex],-0.1)
                elif(gameCopy.winner == None): #Non terminal
                    V[actionIndex] = min(V[actionIndex],0)
                elif(gameCopy.winner == 'player2'): #A win
                    V[actionIndex] = min(V[actionIndex],1)                    

        actionIndex = actionIndex + 1

    bestAction = possibleActions[np.argmax(V)]
        
    print("Bot {} is choosing {} which should lead to a reward of {}".format(playerNum, bestAction, np.max(V)))
    return bestAction
