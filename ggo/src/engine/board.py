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

import gtp
import goutil

class Board:
    def __clear_stones(self):
        self.stones = [[None for a in range(20)] for b in range(20)]
        
    def __parse_stones(self, color):
        if color == 'white':
            mark = 'w'
        else:
            mark = 'b'
        stone_list = self.gtp.list_stones(color)
        for vertex in stone_list.split(' '):
            if len(vertex) < 2:
                continue
            (x,y) = goutil.coords_from_vertex(vertex)
            (x,y) = (x-1,y-1)
            self.stones[x][y]=mark

    def __update_stones(self):
        self.__clear_stones()
        self.__parse_stones("white")
        self.__parse_stones("black")
    
    def __init__(self):
        #lol...
        self.gtp = gtp.gtp()

        self.gtp.set_boardsize("19")
        self.gtp.clear_board()
        self.__clear_stones()
        
    def make_move(self, color, x, y):
        vertex = goutil.coords_to_vertex(x,y)
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
        
