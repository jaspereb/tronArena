import numpy as np
import utils


class Game( ):
    #An arena for the tron game, turns are synchronous. Both 'tails' are stored
    #internally using counters but are returned as a binary map of occupied/unocc.
    
    #READ THIS:
    #The action space is left,right,up,down with respect to the board (not to the player)
    #The outer edge of the area is a wall, don't run into it
    #
    #as 
    def __init__( self):
        #Set up default game using parameters below

        self.arenaSize = (19,25)
        self.tailLength = 10

        #Blank Arena with walls
        self.gameState = np.zeros(self.arenaSize, np.int)
        self.gameState[0,:] = 8
        self.gameState[:,0] = 8
        self.gameState[:,-1] = 8
        self.gameState[-1,:] = 8
        
        #Set starting positions
        self.gameState[9,5] = 1
        self.gameState[9,19] = 2
        
        #The map of tail positions
        self.p1Tail = np.zeros(self.arenaSize, np.int)
        self.p2Tail = np.zeros(self.arenaSize, np.int)
        
        #Use this to set starting direction
        self.lastP1Action = 'right'
        self.lastP2Action = 'left'
        
        #If the game is in a terminal state
        self.terminal = False
        
        #The reward according to player 1. 1 for win, -1 for loss, 0.1 for draw
        self.p1Reward = None


    def step(self, p1Action, p2Action):
        #Takes a single step in the environment, each action should be one of the following:
        # 'left'
        # 'right'
        # 'up'
        # 'down'
        #If none of these is input, 'left' is assumed. 
        # THIS IS WITH RESPECT TO THE BOARD NOT THE PLAYER

        #If you run into a wall or a tail you lose. Hitting the other player is a draw. 
        
        #Get current player positions
        p1Pos = self.getPlayerPosition(self, 1)
        p2Pos = self.getPlayerPosition(self, 2)
        
        self.gameState[p1Pos] = 0
        self.gameState[p2Pos] = 0
        
        #First move both players to new positions
        if(p1Action == 'left'):
            p1Pos[1] = p1Pos[1]-1
        
        self.gameState[p1Pos] = 1
        self.gameState[p2Pos] = 2

    def check_for_win( self, playerID, target=4 ):
        # ---------------------------------------------------
        # inputs:
        #   player id ==> player to check. 1 or 2
        #   target ==> how many consecutive tokens to win. default=4
        # outputs:
        #   FLAG_win ==> 1-player wins, 0-no win
        # ---------------------------------------------------

        # identify playerID's tokens
        playerState = self.gameState == playerID

        FLAG_win = 0

        # check for horizontal win
        for i in range( self.boardSize[0] ):
            if np.sum( np.convolve( playerState[i,:] , np.ones((target))) >= target ):
                FLAG_win = 1

        # check for vertical win
        for i in range( self.boardSize[1] ):
            if np.sum( np.convolve( playerState[:,i] , np.ones((target))) >= target ):
                FLAG_win = 1

        # check for diagonal win
        diag1 = np.eye(target)
        diag2 = diag1[::-1,:]
        for i in range( self.boardSize[0] - target + 1 ):
            for j in range(self.boardSize[1] - target + 1):
                if (np.sum( diag1*playerState[i:i+target,j:j+target] ) == target) | (np.sum( diag2*playerState[i:i+target,j:j+target] ) == target):
                    FLAG_win = 1
                    break

        return FLAG_win


    def getPlayerPosition(self, playerNum):
        #Playernum is 1 or 2. Returns a tuple of (row, col)
        row = int(np.where(self.gameState == playerNum)[0])
        col = int(np.where(self.gameState == playerNum)[1])
        pos = [row, col]
        return pos
        
    def check_for_draw( self ):
        # ---------------------------------------------------
        # inputs:
        #   none
        #
        # outputs:
        #   ==> 1-draw, 0-no draw --------------------------------

        # draw if no free spaces on top row
        if np.sum( self.gameState[0,:] == 0 ) == 0:
            return 1
        else:
            return 0
        
if __name__ == "__main__":
    game = Game()
    print(game.gameState)