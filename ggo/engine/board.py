import gtp.gtp
import goutil

class Board:
    def __clear_stones(self):
        self.stones = [[None for a in range(19)] for b in range(19)]
        
    def __parse_stones(self, color):
        if color == 'White':
            mark = 'w'
        else:
            mark = 'b'
        stone_list = self.gtp.list_stones(color)
        for vertex in stone_list.split(' '):
            (x,y) = goutil.vertex_to_coords(vertex)
            (x,y) = (x-1,y-1)
            self.stones[x][y]=mark

    def __update_stones(self):
        self.__clear_stones()
        self.__parse_stones(self,White)
        self.__parse_stones(self,Black)
    
    def __init__(self):
        self.gtp = gtp.gtp()

        gtp.boardsize("19")
        gtp.clear_board()
        self.__clear_stones()
        
    def make_move(self, color, x, y):
        vertex = goutil.coords_to_vertex(x,y)
        self.gtp.move(color, vertex)
        self.__update_stones()
        
