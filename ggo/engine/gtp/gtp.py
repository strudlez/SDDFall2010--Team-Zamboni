import os
import gobject

class gtp:
    def __init__(self):
        (self.infile, self.outfile) = os.popen2("/usr/bin/gnugo --mode gtp")

    def tx(self, string):
        self.infile.write(string+'\n')
        self.infile.flush()

    def rx(self):
        line = self.outfile.readline()
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
        self.rx()
        
    def pass_move(self, color):
        self.tx('play ' + color + 'pass')
        self.rx()

    def end_score(self):
        self.tx('end_score')
        return self.rx()
    
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
        self.rx()
        

