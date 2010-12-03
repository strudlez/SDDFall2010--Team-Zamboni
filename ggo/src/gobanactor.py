# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor Boston, MA 02110-1301,  USA

import clutter
import engine.board
import engine.goutil
from timer import Timer


#Stone is a class which stores a stone's color, it's location, and displays it on the screen
class Stone(clutter.Texture):
    def __init__(self,color,x,y):
        clutter.Texture.__init__(self)

        #Sets the location of the stone
        self.x = x  
        self.y = y

        if color == "black": 
            self.set_from_file("black.png") #Loads black stone image
        elif color == "black_c":
            self.set_from_file("black_c.png") #Loads black stone with 1 liberty image
        elif color == "white":
            self.set_from_file("white.png") #Loads white stone image
        else:
            self.set_from_file("white_c.png") #Loads white stone with 1 liberty image
        self.set_size(40,40)
        self.set_anchor_point_from_gravity(clutter.GRAVITY_CENTER)


#GobanActor is our high-level graphical board.  This class passes instructions from the user down to board, and takes the information from board to display stones properly
class GobanActor(clutter.Group):
    def __place_stone(self, stone):
        (cx, cy) = self.__intersection_to_position(stone.x,stone.y+1) #Gets the location of a stone on our board
        
        self.add(stone) 
        stone.set_position(cx,cy)
        stone.show() #Adds the stone to our stage
	
    def set_board(self,move):#sets the board to a specific state
		self.board.stones=self.history[int(move)-1]
		cur_move_num = len(self.history)
		num_moves_undo=int(cur_move_num)-int(move)
		self.board.gtp.undo(num_moves_undo)
		
		self.history = self.history[0:int(move)]#Set history back to the undo point
		
		return num_moves_undo
		
    def update_stones(self, alt_board=None):
        temp_stones=self.board.stones
        if(alt_board!=None):
            temp_stones=alt_board 
        old_stones = self.stones  #Keep a record of our previous stones
        self.stones = {}
        
        for p in old_stones: #Remove all stones currently on the board
            stone = old_stones[p]
            stone.get_parent().remove(stone)
            
        for x in range(20): #Cycle through all on-board locations
            for y in range(20):
                vertex = engine.goutil.coords_to_vertex(x,y) #Gets a location to place the stone at.
                vertex2 = engine.goutil.coords_to_vertex(x,y+1) #Gets a location for the purpose of checking number of liberties.
                if temp_stones[x][y] == 'w': #If the stone at the current board position is white
                    if(self.board.count_liberties(vertex2)=='1'): 
                        stone = Stone("white_c",x,y) #If the stone has one liberty, display the warning piece instead of the normal piece
                    else:
                        stone = Stone("white",x,y) #Display the normal stone
                    self.stones[vertex] = stone
                elif temp_stones[x][y] == 'b': #if the stone is black
                    if(self.board.count_liberties(vertex2)=='1'): #Follows as if the stone was white, see above.
                        stone = Stone("black_c",x,y)
                    else:
                        stone = Stone("black",x,y)
                    self.stones[vertex] = stone

        for stone in self.stones:
            self.__place_stone(self.stones[stone]) #Place all stones on the board
        if(alt_board==None):
			if(len(self.history)%2 == 0):
				self.current_color="white"
			else:
				self.current_color="black"
			self.history.append(self.board.stones) #Keep track of the history for review
			self.window.add_hist_button(len(self.history), 1, self.current_color)
        
                    
 

            
    def __intersection_from_position(self,cx,cy): #Convert the coordinates of the stone into a column and row number

        ratio = 700/2000.0
        border_width = 60*ratio
        line_width = 6*ratio
        space_height = 98*ratio
        space_width = 98*ratio

        x = round((cx-border_width)/(space_width+line_width))+1
        y = round((cy-border_width)/(space_height+line_width))+1
        return (int(x),int(y))

    def __intersection_to_position(self, x, y): #Convert the column and row number of a stone into a location on the board

        ratio = 700/2000.0
        border_width = 60*ratio
        line_width = 6.0*ratio
        space_height = 98*ratio
        space_width =  98*ratio

        cx = border_width+(line_width+space_width)*(x-1)
        cy = border_width+(line_width+space_height)*(y-1)
        
        return (cx,cy)
        
    def place_stone(self, color, x, y): #Attempts to place a stone at the requested vertex
        
        if self.board.make_move(color, x, y):
            self.update_stones()
            return True
        
        return False
        
    def place_stone_gnugo(self, color, callback): #Has the AI place a stone.
        other = "black" if color=="white" else "white"
        self.timers[color].start() #start ai's timer
        def stone_placed(vertex):
            self.timers[color].stop() #stop ai's timer
            self.timers[other].start() #start player's timer
            self.update_stones()
            callback(vertex)
        self.board.make_gnugo_move(color, stone_placed)
        return True
        
    def place_stone_at_position(self, Color, cx, cy): #When the user clicks the board
        (x,y) = self.__intersection_from_position(cx,cy)  #Convert the click coordinates to a vertex
        return self.place_stone(Color,x,y) #Place a stone at the vertex

    def estimate_score(self): #Returns GnuGo's estimate of the score
        return self.board.estimate_score()

    def final_score(self): #Returns the final score of the game
        return self.board.final_score()

    def get_time(self, color): #Gets the amount of time remaining for the player of the requested color
        return self.timers[color].get_time()
        #return self.board.get_time(color)

    def set_time(self, time, bytime):  #Sets the amount of time for each player
        for i in self.timers.values(): i.set_time(time,bytime)
        return self.board.set_time(time, bytime)

    def __init__(self, board, window): #Creates the visible board, sets up our array of stones, and creates an instance of the board class to work with
        clutter.Group.__init__(self)#,*args)
        
        self.current_color="black"
        
        self.stones = {}
        
        self.board = board
    
        self.window = window
        
        self.timers={"black":Timer(), "white": Timer()}
    
        self.history = []

        
        self.set_size(700,700) 
        self.background = clutter.Texture("goban.png") #Loads the image of a board
        self.background.set_size(700,700) #Sets the size of our board image
        self.background.set_position(0,0)  #Sets the position of the board image
        self.add(self.background)#Displays the board

        self.show_all()
