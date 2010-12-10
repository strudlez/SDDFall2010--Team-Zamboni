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

import os
import gobject
import glib
import shlex, subprocess

#GTP(Go Text Protocol), is the text protocol used to communicate with GnuGo. Our gtp class provides us with functions that will request actions of GnuGo and report the results.
class gtp:
    def __gnugo_write_callback (self, source, condition): #Returns the output GnuGo to a callback function
        if self.waiting == True:
            response = self.rx()
            self.callback(response)
            self.waiting = False
            
        return True

    def __init__(self): #Creates a new instance of gtp with which to interface with GnuGo
        args = shlex.split("/usr/games/gnugo --mode gtp")
        self.proc = subprocess.Popen(args, stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE)
        (self.infile, self.outfile) = (self.proc.stdin, self.proc.stdout)
        self.watch = glib.io_add_watch(self.outfile,glib.IO_IN, self.__gnugo_write_callback)
        self.waiting = False

    def tx(self, string): #Writes a command to GnuGo
        print string
        self.infile.write(string+'\n')
        self.infile.flush()

    def rx(self): #Reads the output GnuGo returns
        line = self.outfile.readline()
        print line
        if line[0] == '?':
            self.outfile.readline()
            raise RuntimeError(line[2:-1])
        line = line[2:-1]
        line2 = 'x'
        while not line2[0] == '\n':
            line2 = self.outfile.readline()
            if not line2[0] == '\n':
                line = line + ' ' + line2[:-1]
        return line

    def get_name(self): #Returns the name, version, and protocol version of GnuGo
        self.tx('name')
        prog = self.rx()
        self.tx('version')
        vers = self.rx()
        self.tx('protocol_version')
        pvers = self.rx()
        return (prog,vers,pvers)
    
    def set_boardsize(self,size): #Sets the size of the Go board
        self.tx('boardsize ' + str(size))
        self.rx()
        
    def clear_board(self): #Clears the board of all stones
        self.tx('clear_board')
        self.rx()
        
    def set_komi(self, komi): #Sets the komi, or the amount of points added to the white player as recompense for moving second
        self.tx('komi ' + str(komi))
        self.rx()
        
    def set_handicap(self, handicap): #Sets the number of handicap stones on the board
        if handicap < 2:
            return None
        self.tx('fixed_handicap ' + str(handicap))
        return self.rx()
    
    def move(self, color, vertex): #Attempts to play a stone of the given color at the requested vertex
        self.tx('play ' + color + ' ' + vertex)
        print self.rx()
        
    def pass_move(self, color): #Passes the turn
        self.tx('play ' + color + 'pass')
        self.rx()

    def final_score(self): #Returns a file of the final game
        self.tx('final_score')
        return self.rx
    
    def set_level(self, level): #Sets the AI level of GnuGo
        self.tx('level ' + str(level))
        return self.rx()
    
    def list_stones(self, color): #Lists all stones of the requested color on the board, seperated by spaces
        self.tx('list_stones ' + color)
        return self.rx()
    
    def get_captures(self, color): #Get the number of pieces captured by the player of the requested color
        self.tx('captures ' + color)
        return self.rx()
    
    def undo(self): #Undoes the last move
        self.tx('undo')
        return self.rx()
    
    def undo(self, num_moves): #Undoes the last n moves
        self.tx('gg-undo %d' % num_moves)
        return self.rx()
    
    def move_history(self): #Gives the best possible estimate of the score
        self.tx("move_history")
        return self.rx()
    

    def countlib(self, vertex): #Returns the number of liberties for the stone at the given vertex
        self.tx('countlib ' + vertex)
        return self.rx()

    def estimate_score(self): #Gives the best possible estimate of the score
        self.tx('estimate_score')
        return self.rx()

    def time_settings(self, time, bytime, bystones): #Sets the time for each player
        self.tx('time_settings ' + str(time) + ' ' + str(bytime) + ' ' + str(bystones))
        return self.rx()

    def time_left(self,color): #Returns the time left for the player of the requested color
        self.tx('time_left %s 11 3' % color)
        return self.rx()
     
    def genmove(self, color, callback): #Generates a move by the Ai
        self.waiting = True
        self.callback = callback
        self.tx('genmove ' + color)
        return True
    
    def count_liberties(self, vertex): #Returns the number of liberties for the stone at the given vertex
            self.tx('countlib ' + vertex)
            return self.rx()
            
    def level(self, lvl): #Sets the Ai level
            self.tx('level %d' % lvl)
            return self.rx()
              
          
        
 
