import gtp.gtp
import goutil

class Board:
    def __clear_stones(self):
		#init the list of stones
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
            (x,y) = goutil.vertex_to_coords(vertex)
            (x,y) = (x-1,y-1)
            self.stones[x][y]=mark#keep track of the color of stone placed

    def __update_stones(self):
        self.__clear_stones()
        self.__parse_stones("white")
        self.__parse_stones("black")
    
    def __init__(self):
        #lol...
        self.gtp = gtp.gtp.gtp()

        self.gtp.set_boardsize("19")
        self.gtp.clear_board()
        self.__clear_stones()
        
    def undo(self):
        try:
            self.gtp.undo()
        except RuntimeError:
            return False
        self.__update_stones()
        return True
        
    def make_move(self, color, x, y):
        vertex = goutil.coords_to_vertex(x,y)
        try: 
            self.gtp.move(color, vertex)
        except RuntimeError:
            return False
        self.__update_stones()
        return True
        
