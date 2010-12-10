# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor Boston, MA 02110-1301, USA

import zambogo.engine.gtp.gtp
import zambogo.engine.goutil
#Board serves as our low-level board, which is a two-dimensional array. Board accepts requests from gobanactor and interfaces with GnuGo to complete the requested function.
class Board:
    def __clear_stones(self): #Wipes our array of stones
        self.stones = [[None for a in range(20)] for b in range(20)]
        
    def __parse_stones(self, color): #Fills our array of stones for us in gobanactor
        if color == 'white': #If we are parsing stone for white, sets our mark to w
            mark = 'w'
        else: #Else, sets our mark to b
            mark = 'b'
        stone_list = self.gtp.list_stones(color) #Requests a string that contains all vertexes which contain stones of the desired color from GnuGo
        for vertex in stone_list.split(' '): #For each vertex in stone_list
            if len(vertex) < 2:
                continue
            (x,y) = zambogo.engine.goutil.coords_from_vertex(vertex) #Find the coordinates of the stone given a vertex on the board
            (x,y) = (x-1,y-1) #Decrement the coordinates, as arrays start at 0, not 1
            self.stones[x][y]=mark #Records that there is a stone of the color we are parsing at this vertex

    def __update_stones(self): #Updates our array with the positions of all stones
        self.__clear_stones() #Wipes the array of stones
        self.__parse_stones("white") #Parse the board for all white and black stones
        self.__parse_stones("black")
    
    def __init__(self): #Create a new board
        #lol...
        self.gtp = zambogo.engine.gtp.gtp.gtp() #Creates an instance of gtp to interface with

        self.gtp.set_boardsize("19") #Tells gtp to set our board size to the standard 19x19
        self.gtp.clear_board() #Tells gtp to clear our board of all objects
        self.__clear_stones() #Clears the array of stones

    def estimate_score(self): #Estimates the current score with GnuGo
        try:
            score = self.gtp.estimate_score()
        except RuntimeError:
            return False
        return score

    def final_score(self): #Gets the final game file from GnuGo
        try:
            score = self.gtp.final_score()
        except RuntimeError:
            return False
        return score

    def set_time(self, time, bytime): #Sets the time allocation for each player
        try:
            tim = self.gtp.time_settings(time, bytime, 30)
        except RuntimeError:
            return False
        return tim

    def get_time(self, color): #Gets the time for the player of the requested color
        try:
            timelft = self.gtp.time_left(color)
        except RuntimeError:
            return False
        return timelft
     
    def make_move(self, color, x, y): #Attempt to make a move at the given coordinates with a stone of the given color
        vertex = zambogo.engine.goutil.coords_to_vertex(x,y) #Convert the coordinates to a board vertex
        try:
            self.gtp.move(color, vertex)
        except RuntimeError:
            return False
        self.__update_stones()
        return True
            
    def make_gnugo_move(self, color, callback): #Have the AI place a stone on the board
        def gnugo_done(response): #This is a function that will be called when a stone has been placed by GnuGo
            self.__update_stones()
            callback(response)
        self.gtp.genmove(color, gnugo_done)
        return True
    
    def get_move_num(self):
        return len(self.gtp.move_history().split(" "))/2

    def count_liberties(self, vertex): #Returns the number of liberties at the given vertex
        return self.gtp.count_liberties(vertex)
    
    def set_move(self, move):
        self.gtp.undo(self.get_move_num()-move)
        self.__update_stones()
        return move
    
    def undo(self):
        self.set_move(self.get_move_num()-1)
    def redo(self):
        self.set_move(self.get_move_num()+1)
        
    def count_liberties(self, vertex):
        return int(self.gtp.count_liberties(vertex))
