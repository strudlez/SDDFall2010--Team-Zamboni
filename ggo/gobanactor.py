import clutter
import engine.board
import engine.goutil

class Stone(clutter.Texture):
    def __init__(self,color):
        clutter.Texture.__init__(self)
        if color == "black":
            self.set_from_file("black.png")
        else:
            self.set_from_file("white.png")
        self.set_size(40,40)
        self.set_anchor_point_from_gravity(clutter.GRAVITY_CENTER)

class GobanActor(clutter.Group):
    def __update_stones(self):
        old_stones = self.stones
        self.stones = {}
        
        for stone in old_stones:
            stone.get_parent().remove(stone)
            
        for x in range(20):
            for y in range(20):
                vertex = goutil.coords_to_vertex(x,y)
                if vertex in old_stones.keys():
                    self.stones[vertex] = self.old_stones[vertex]
                

            
    def __intersection_from_position(self,cx,cy):
        ratio = 700/2000.0
        border_width = 60*ratio
        line_width = 7*ratio
        space_height = 100*ratio
        space_width = 100*ratio

        x = round((cx-border_width)/(space_width+line_width))+1
        y = round((cy-border_width)/(space_height+line_width))+1
        print (cx,cy)
        print (x,y)
        return (int(x),int(y))

    def __intersection_to_position(self, x, y):
        ratio = 700/2000.0
        border_width = 60*ratio
        line_width = 7*ratio
        space_height = 98*ratio
        space_width = 98*ratio

        cx = border_width+(line_width+space_width)*(x-1)
        cy = border_width+(line_width+space_height)*(y-1)
        
        return (cx,cy)
    def place_stone(self, color, x, y):
        
        if self.board.make_move(color, x, y):
            self.__update_stones()
            return True
        
        return False
        
    def place_stone_at_position(self, Color, cx, cy):
        (x,y) = self.__intersection_from_position(cx,cy)
        return self.place_stone(Color,x,y)

    def __init__(self, board):
        clutter.Group.__init__(self)#,*args)
        
        self.stones = {}
        
        self.board = board

        
        self.set_size(700,700)
        self.background = clutter.Texture("goban.png")
        self.background.set_size(700,700)
        self.background.set_position(0,0)
        self.add(self.background)

        self.show_all()
