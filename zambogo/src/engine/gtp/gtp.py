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

class gtp:
    def __gnugo_write_callback (self, source, condition):
        if self.waiting == True:
            response = self.rx()
            self.callback(response)
            self.waiting = False
            
        return True

    def __init__(self):
        args = shlex.split("/usr/games/gnugo --mode gtp")
        self.proc = subprocess.Popen(args, stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE)
        (self.infile, self.outfile) = (self.proc.stdin, self.proc.stdout)
        self.watch = glib.io_add_watch(self.outfile,glib.IO_IN, self.__gnugo_write_callback)
        self.waiting = False

    def tx(self, string):
        print string
        self.infile.write(string+'\n')
        self.infile.flush()

    def rx(self):
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

    def get_name(self):
        self.tx('name')
        prog = self.rx()
        self.tx('version')
        vers = self.rx()
        self.tx('protocol_version')
        pvers = self.rx()
        return (prog,vers,pvers)
    
    def set_boardsize(self,size):
        self.tx('boardsize ' + str(size))
        self.rx()
        
    def clear_board(self):
        self.tx('clear_board')
        self.rx()
        
    def set_komi(self, komi):
        self.tx('komi ' + str(komi))
        self.rx()
        
    def set_handicap(self, handicap):
        if handicap < 2:
            return None
        self.tx('fixed_handicap ' + str(handicap))
        return self.rx()
    
    def move(self, color, vertex):
        self.tx('play ' + color + ' ' + vertex)
        print self.rx()
        
    def pass_move(self, color):
        self.tx('play ' + color + 'pass')
        self.rx()

    def final_score(self):
        self.tx('final_score')
        return self.rx
    
    def set_level(self, level):
        self.tx('level ' + str(level))
        return self.rx()
    
    def list_stones(self, color):
        self.tx('list_stones ' + color)
        return self.rx()
    
    def get_captures(self, color):
        self.tx('captures ' + color)
        return self.rx()
    
    def undo(self):
        self.tx('undo')
        return self.rx()

    def countlib(self, vertex):
        self.tx('countlib ' + vertex)
        return self.rx()

    def estimate_score(self):
        self.tx('estimate_score')
        return self.rx()

    def time_settings(self, time, bytime, bystones):
        self.tx('time_settings ' + str(time) + ' ' + str(bytime) + ' ' + str(bystones))
        return self.rx()

    def time_left(self,color):
        self.tx('time_left ' + color + ' 11 3')
        return self.rx()
     
    def genmove(self, color, callback):
        self.waiting = True
        self.callback = callback
        self.tx('genmove ' + color)
        return True
              
          
        
 
