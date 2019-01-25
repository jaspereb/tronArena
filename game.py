import numpy as np
from PIL import Image

class Game():
    #An arena for the tron game, turns are synchronous. Both 'tails' are stored
    #internally using counters but are returned as a binary map of occupied/unocc.
    
    #READ THIS:
    #The action space is left,right,up,down with respect to the board (not to the player)
    #The outer edge of the area is a wall, don't run into it
    #
    #as 
    def __init__(self):
        #Set up default game using parameters below
        self.VERBOSE = 1 #For debugging, 0 prints nothing, 1 prints end state, 2 prints all states

        self.arenaSize = (100,150) #19,25 is the default
        self.tailLength = 100000

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
        
        #Winner, is 'player1' or 'player2' or 'draw'
        self.winner = None

    def step(self, p1Action, p2Action):
        #Takes a single step in the environment, each action should be one of the following:
        # 'left'
        # 'right'
        # 'up'
        # 'down'
        #If none of these is input, the previous action is used (ie, go straight)
        # THIS IS WITH RESPECT TO THE BOARD NOT THE PLAYER

        #If you run into a wall or a tail you lose. Hitting the other player is a draw. 
        
        if(self.VERBOSE>1):
            print("Prior to move, the arena looks like:  ")
            print(self.getGameState())
                
        if(p1Action == None):
            p1Action = self.lastP1Action
            if(self.VERBOSE>0):
                print("No action specified, using previous action")
        if(p2Action == None):
            p2Action = self.lastP2Action
            if(self.VERBOSE>0):
                print("No action specified, using previous action")
            
        self.lastP1Action = p1Action
        self.lastP2Action = p2Action
        
        
        #Get current player positions
        p1Pos = self.getPlayerPosition(1)
        p2Pos = self.getPlayerPosition(2)
        
        #Update tail positions before moving players
        self.p1Tail[p1Pos[0], p1Pos[1]] = 1
        self.p2Tail[p2Pos[0], p2Pos[1]] = 1
        self.p1Tail[np.where(self.p1Tail != 0)] += 1
        self.p2Tail[np.where(self.p2Tail != 0)] += 1
        self.p1Tail[np.where(self.p1Tail > self.tailLength+1)] = 0
        self.p2Tail[np.where(self.p2Tail > self.tailLength+1)] = 0
        
        self.gameState[p1Pos[0], p1Pos[1]] = 0
        self.gameState[p2Pos[0], p2Pos[1]] = 0
        
        #First move both players to new positions
        if(p1Action == 'left'):
            p1Pos[1] = p1Pos[1]-1
        elif(p1Action == 'right'):
            p1Pos[1] = p1Pos[1]+1
        elif(p1Action == 'up'):
            p1Pos[0] = p1Pos[0]-1
        elif(p1Action == 'down'):
            p1Pos[0] = p1Pos[0]+1
        else:
            print("INVALID P1 ACTION")
            print(p1Action)
            return
            
        if(p2Action == 'left'):
            p2Pos[1] = p2Pos[1]-1
        elif(p2Action == 'right'):
            p2Pos[1] = p2Pos[1]+1
        elif(p2Action == 'up'):
            p2Pos[0] = p2Pos[0]-1
        elif(p2Action == 'down'):
            p2Pos[0] = p2Pos[0]+1
        else:
            print("INVALID P2 ACTION")
            print(p2Action)
            return
            
        self.gameState[p1Pos[0], p1Pos[1]] = 1
        self.gameState[p2Pos[0], p2Pos[1]] = 2
        
        if(self.VERBOSE>1):
            print("After the move, the arena looks like:  ")
            print(self.getGameState())
        
        #Check player-player collision
        if(np.array_equal(p1Pos,p2Pos)):
            if(self.VERBOSE>0):
                print("DRAW: Game ended with player to player collision")
            self.terminal = True
            self.winner = 'draw'
            return
        
        #Check player-wall collision
        collision = self.checkWallCollision(p1Pos, p2Pos)
        
        if(collision == 1):
            if(self.VERBOSE>0):
                print("P2 Wins: Game ended with player 1 hitting the wall")
            self.terminal = True
            self.winner = 'player2'
            return
        elif(collision == 2):
            if(self.VERBOSE>0):
                print("P1 Wins: Game ended with player 2 hitting the wall")
            self.terminal = True
            self.winner = 'player1'
            return
        elif(collision == 3):
            if(self.VERBOSE>0):
                print("DRAW: Game ended with both players hitting the wall")
            self.terminal = True
            self.winner = 'draw'   
            return

        #Check player-tail collision
        collision = self.checkTailCollision(p1Pos, p2Pos)
        
        if(collision == 1):
            if(self.VERBOSE>0):
                print("P2 Wins: Game ended with player 1 hitting a tail")
            self.terminal = True
            self.winner = 'player2'
            return
        elif(collision == 2):
            if(self.VERBOSE>0):
                print("P1 Wins: Game ended with player 2 hitting a tail")
            self.terminal = True
            self.winner = 'player1'
            return
        elif(collision == 3):
            if(self.VERBOSE>0):
                print("DRAW: Game ended with both players hitting a tail")
            self.terminal = True
            self.winner = 'draw' 
            return
        
    def checkWallCollision(self, p1Pos, p2Pos):
        #Returns 0 if no players in wall square, 1 if p1 is, 2 if p2 is, 3 if both
        collision = 0
        if(p1Pos[0] == 0 or p1Pos[0] == self.arenaSize[0]-1):
            collision += 1
        elif(p1Pos[1] == 0 or p1Pos[1] == self.arenaSize[1]-1):
            collision += 1
            
        if(p2Pos[0] == 0 or p2Pos[0] == self.arenaSize[0]-1):
            collision += 2
        elif(p2Pos[1] == 0 or p2Pos[1] == self.arenaSize[1]-1):
            collision += 2

        return collision
    
    def checkTailCollision(self, p1Pos, p2Pos):
        #Returns 0 if no players in tail square, 1 if p1 is, 2 if p2 is, 3 if both
        collision = 0
        tails = self.p1Tail + self.p2Tail
        if(tails[p1Pos[0], p1Pos[1]] != 0):
            collision += 1
        if(tails[p2Pos[0], p2Pos[1]] != 0):
            collision += 2    
        return collision
        
    def getPlayerPosition(self, playerNum):
        #Playernum is 1 or 2. Returns an array of (row, col)
        row = int(np.where(self.gameState == playerNum)[0])
        col = int(np.where(self.gameState == playerNum)[1])
        pos = np.asarray([row, col])
        return pos
        
    def getGameState(self):
        #Returns a copy of the game state as a numpy array of [boardsize,boardsize] where
        #player 1 is a a 1, player 2 is a 2, tails are 3 and the walls are 8.
        #You can use the getPlayerPosition to get the [row,col] position from the game board
        outputState = np.copy(self.gameState)
        outputState[np.where((self.p1Tail + self.p2Tail) != 0)] = 3
        
        #to overlay player positions above tails
        outputState[np.where(self.gameState == 1)] = 1
        outputState[np.where(self.gameState == 2)] = 2
        
        return outputState
        
    def getGameImg(self):
        #Formats the game state as a PIL image
        imgState = self.getGameState()
        #Adjust values for display
        imgState[np.where(imgState == 1)] = 15
        imgState[np.where(imgState == 2)] = 20
        imgState[np.where(imgState == 3)] = 10
        
        imgState = 12*imgState
        imgState = imgState.astype(np.uint8)
        img = Image.fromarray(imgState)
        
        basewidth = 300
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize))

        return img
    
if __name__ == "__main__":
    game = Game()
    print(game.gameState)
