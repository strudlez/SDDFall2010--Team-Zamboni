import clutter
import zambogo.engine.board
import zambogo.engine.goutil
import zambogo.util

class Stone(clutter.Texture):
    def __init__(self,color,x,y):
        clutter.Texture.__init__(self)

        self.x = x
        self.y = y
        self.color = color
		
        if color == "black":
            self.set_from_file(zambogo.util.get_image("black.png"))
        elif color == "white_c":
            self.set_from_file(zambogo.util.get_image("white.png"))
        elif color == "black_c":
            self.set_from_file(zambogo.util.get_image("black.png"))
        else:
            self.set_from_file(zambogo.util.get_image("white.png"))
        self.set_size(40,40)
        self.set_anchor_point_from_gravity(clutter.GRAVITY_CENTER)



class GobanActor(clutter.Group):
    def __place_stone(self, stone):
        (cx, cy) = self.__intersection_to_position(stone.x,stone.y+1)
        self.add(stone)
        stone.set_position(cx,cy)
        stone.show()

    def _update_stones(self, alt_board=None):
        stones=self.board.stones
        if(alt_board!=None):
			stones=alt_board
        
        old_stones = self.stone_actors
        self.stone_actors = {}
        
        for p in old_stones:
            stone = old_stones[p]
            stone.get_parent().remove(stone)
            
        for x in range(20):
            for y in range(20):
                vertex = zambogo.engine.goutil.coords_to_vertex(x,y)
                vertex2 = zambogo.engine.goutil.coords_to_vertex(x,y+1)
                if stones[x][y] == 'w':
					if((self.stone_actors.has_key(vertex))==False):
						color="white"
						try:
							if(self.board.gtp.count_liberties(vertex2)=='1'):
								color="white_c"
						except:
							pass
						stone = Stone(color,x,y)
						self.stone_actors[vertex] = stone
                elif stones[x][y] == 'b':
					if((self.stone_actors.has_key(vertex))==False):
						color="black"
						try:
							if(self.board.gtp.count_liberties(vertex2)=='1'):
								color="black"
						except:
							pass
						stone = Stone(color,x,y)
						self.stone_actors[vertex] = stone
						
        for stone in self.stone_actors:
            self.__place_stone(self.stone_actors[stone])
        if(alt_board==None):
			self.history.append(self.board.stones)#keep track of the history for review
#			self.window.add_hist_button(len(self.history), 1, self.current_color)
        
        if(self.current_color=="black"):
			self.current_color="white"
        else:
			self.current_color="black"
            
    def __intersection_from_position(self,cx,cy):

        ratio = 700/2000.0
        border_width = 60*ratio
        line_width = 6*ratio
        space_height = 98*ratio
        space_width = 98*ratio

        x = round((cx-border_width)/(space_width+line_width))+1
        y = round((cy-border_width)/(space_height+line_width))+1
        return (int(x),int(y))

    def __intersection_to_position(self, x, y):

        ratio = 700/2000.0
        border_width = 60*ratio
        line_width = 6.0*ratio
        space_height = 98*ratio
        space_width =  98*ratio

        cx = border_width+(line_width+space_width)*(x-1)
        cy = border_width+(line_width+space_height)*(y-1)
        return (cx,cy)
    
    def undo(self):
        self.board.undo()
        self._update_stones()

    def place_stone(self, color, x, y):
        
        if self.board.make_move(color, x, y):
            self._update_stones()
            return True
        
        return False
        
    def place_stone_at_position(self, Color, cx, cy):
        (x,y) = self.__intersection_from_position(cx,cy)
        return self.place_stone(Color,x,y)

    def __init__(self, board, window):
        clutter.Group.__init__(self)#,*args)
        
        self.current_color="black"
        
        self.stone_actors = {}
        
        self.board = board
        
        self.window=window
		
        self.history = []
        
        self.set_size(700,700)
        self.background = clutter.Texture(zambogo.util.get_image("goban.png"))
        self.background.set_size(700,700)
        self.background.set_position(0,0)
        self.add(self.background)

        self.show_all()
