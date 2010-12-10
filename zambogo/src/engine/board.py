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

import zambogo.engine.gtp.gtp
import zambogo.engine.goutil

class Board:
    def __clear_stones(self):
        self.stones = [[None for a in range(20)] for b in range(20)]
        
    def __parse_stones(self, color):
        if color == 'white':
            mark = 'w'
        else:
            mark = 'b'
        stone_list = self.gtp.list_stones(color)
        print stone_list
        for vertex in stone_list.split(' '):
            if len(vertex) < 2:
                continue
            (x,y) = zambogo.engine.goutil.coords_from_vertex(vertex)
            (x,y) = (x-1,y-1)
            self.stones[x][y]=mark

    def __update_stones(self):
        self.__clear_stones()
        self.__parse_stones("white")
        self.__parse_stones("black")
    
    def __init__(self):
        #lol...
        self.gtp = zambogo.engine.gtp.gtp.gtp()

        self.gtp.set_boardsize("19")
        self.gtp.clear_board()
        self.__clear_stones()

    def estimate_score(self):
        try:
            score = self.gtp.estimate_score()
        except RuntimeError:
            return False
        return score

    def final_score(self):
        try:
            score = self.gtp.final_score()
        except RuntimeError:
            return False
        return score

    def set_time(self, time, bytime):
        try:
            tim = self.gtp.time_settings(time, bytime, 30)
        except RuntimeError:
            return False
        return tim

    def get_time(self, color):
        try:
            timelft = self.gtp.time_left(color)
        except RuntimeError:
            return False
        return timelft
     
    def make_move(self, color, x, y):
        vertex = zambogo.engine.goutil.coords_to_vertex(x,y)
        try: 
            self.gtp.move(color, vertex)
        except RuntimeError:
            return False
        self.__update_stones()
        return True
            
    def make_gnugo_move(self, color, callback):
        def gnugo_done(response):
            self.__update_stones()
            callback(response)
        self.gtp.genmove(color, gnugo_done)
        return True
    
    def get_move_num(self):
        return len(self.gtp.move_history().split(" "))/2

    
    def set_move(self, move):
        self.gtp.undo(self.get_move_num()-move)
        return move
    
    def undo(self):
        self.set_move(self.get_move_num()-1)
    def redo(self):
        self.set_move(self.get_move_num()+1)
                       
                       
        
