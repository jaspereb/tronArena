# TRONArena
This program is a tron (or 2 player snake) game arena. It defines a game class (similar to the connect4 game) along with some helper methods. 

Clone or download the code from [here](https://github.com/jaspereb/tronArena/releases/latest) then run the main.py file.

The GUI should behave properly if you run it in an environment that stops pop up windows (eg a notebook or the Spyder IDE), otherwise you have to manually close each GUI frame. 

Seeing as we're roboticists, for the actual contest this game class will be running in a ROS node which you can read the board state from and send your moves to.  

This [link](https://www.a1k0n.net/2010/03/04/google-ai-postmortem.html) is a good place to start for a non-learning based approach.  

Check out [this](http://karpathy.github.io/2016/05/31/rl/) for a policy gradient implementation.  

The initial challenge will be an empty board of 25x19 squares, there will also be a slightly more difficult challenge where random walls are introduced to the area for each game, code for this will be added shortly.  

There is a discussion blog [on confluence](https://confluence.acfr.usyd.edu.au/pages/viewrecentblogposts.action?key=SOCL&src=sidebar)

## Game Rules & Implementation Details
-The board is stored as a numpy array with default size (19,25)  
-Player 1 position is stored as a 1, player 2 is a 2  
-The outer edge of the board is a wall, stored as 8's  
-The tails are stored internally as a counter but are exposed in the getGameState() function as all 3's  
-You can use the getGameState() function to get a copy of the board with the walls, players and tails on it. Tails are both stored as 3's  
-During each move you are teleported one square either up,down,left,right. If you end up on the same square as your opponent it counts as a draw.  
-The square you were previously on becomes a tail, the final square of your tail is erased  
-If you hit a wall at the same move your opponent hits a tail, you are the loser  
-If your bot tries to move back on itself you will hit your own tail and lose, implement your own don't-make-a-U-turn code  
-2 sample bots are provided, an optimal one step lookahead bot called baselineBot.py and a simplified lookahead bot called bot1.py  

## Dependencies
-matplotlib  
-numpy  
-PIL  
-For some reason the GUI is grayscale in python3, use python2 if you need the colours

## ToDo
-Write ROS node wrapper for competition  
-Write code to add random walls for hard mode

