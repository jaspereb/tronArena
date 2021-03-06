'''This script runs the game environment, it begins a blank game, gets actions from 2 bots,
evolves the state, checks for end conditions and assigns reward. Default game settings are in the
game.py file. A SARS' sequence is stored for RL'''

import game
import copy
import baselineBot
from matplotlib import pyplot as plt


def playGame():
    GUI = True #This is super inefficient
    
    tronGame = game.Game()
    print(" === Starting a new game ===")
    
    #You can remove this if you don't need it for RL
    memory = []
    reward = 0
    
    while(True):
        print(tronGame.getGameState())
        
        #While nobody has won, get a move from each bot
        p1Action = baselineBot.getAction(copy.deepcopy(tronGame), 1)
        p2Action = baselineBot.getAction(copy.deepcopy(tronGame), 2)

        startState = tronGame.getGameState()
        
        if(GUI):        
            img = tronGame.getGameImg()
            plt.figure()
            plt.imshow(img)
            plt.show()
            
        #Note, if it is grayscale (as in python3), player 1 is the darker one
        print('Player 1 (yellow) goes ' + p1Action)
        print('Player 2 (red) goes ' + p2Action)
        
        #Evolve the game state        
        tronGame.step(p1Action,p2Action)
           
        #Assign Rewards
        if(tronGame.terminal == True):
            if(tronGame.winner == 'player1'):
                reward = 1
            elif(tronGame.winner == 'player2'):
                reward = -1
            elif(tronGame.winner == 'draw'):
                reward = 0.1
            else:
                print("ERROR")
                
        memory.append([startState, p1Action, p2Action, reward, tronGame.getGameState()])    
        if(tronGame.terminal == True):
            break

    return memory
    
if __name__ == "__main__":
    gameMemories = []
    
    gameMemories.append(playGame())