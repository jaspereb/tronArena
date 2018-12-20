'''This script runs the game environment, it begins a blank game, gets actions from 2 bots,
evolves the state, checks for end conditions and assigns reward. Default game settings are in the
game.py file. A SARS' sequence is stored for RL'''

import game
import copy
import bot1
import bot2


def playGame():
    tronGame = game.Game()
    print(" === Starting a new game ===")
    
    #You can remove this if you don't need it for RL
    memory = []
    reward = 0
    
    while(True):
        print(tronGame.getGameState())
        
        #While nobody has won, get a move from each bot
        p1Action = bot1.getAction(copy.deepcopy(tronGame))
        p2Action = bot2.getAction(copy.deepcopy(tronGame))
        
        print('Player 1 goes ' + p1Action)
        print('Player 2 goes ' + p2Action)
        
        startState = tronGame.getGameState()
        
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

if __name__ == "__main__":
    gameMemories = []
    
    gameMemories.append(playGame())