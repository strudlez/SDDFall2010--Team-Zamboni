#ximport clutter

import gtk
import pygtk

import cluttergtk
import clutter

import zambogo.actors.gobanactor
import zambogo.engine.board

import zambogo.sgf.sgflib


class ReviewWindow(gtk.Window):
    
    def __make_label(self):
        self.label = gtk.Label()
    
    def __make_board(self):
        self.board = zambogo.engine.board.Board()
        self.goban = zambogo.actors.gobanactor.GobanActor(self.board,self)
        self.stage.add(self.goban)
        self.stage.show()

    def __setup_stage(self):
        self.stage = self.embed.get_stage()
        self.stage.set_size(700,700)
        
        self.__make_board()
        
        self.stage.show_all()
    
    def __make_embed(self):
        self.embed = cluttergtk.Embed()
        self.embed.set_size_request(700,700)
        
    def __make_button(self, stock_id):
        b = gtk.Button()
        image = gtk.Image()
        
        image.set_from_stock(stock_id, gtk.ICON_SIZE_BUTTON)
        b.set_image(image)
        
        return b
    
    def __parse_node(self, node):
        color = ""
        move = ""

        if node.has_key("B"):
            color = "black"
            move = node.get("B").data[0]
        elif node.has_key("W"):
            color = "white"
            move = node.get("W").data[0]
            
        coords = list(move)
        x = ord(coords[0])-ord('a')+1
        y = ord(coords[1])-ord('a')+1
        
        return (color,x,y)
    
    def __update_sensitivity(self):
        self.nextb.set_sensitive(True)
        self.prevb.set_sensitive(True)
        self.startb.set_sensitive(True)
        self.endb.set_sensitive(True)
        
        if (self.move_num == len(self.game_tree)-1):
            self.nextb.set_sensitive(False)
            self.endb.set_sensitive(False)
        if (self.move_num == 0):
            self.prevb.set_sensitive(False)
            self.startb.set_sensitive(False)
        
    
    def __update_label(self):
        self.label.set_text("(%s of %s)" % (self.move_num,
                                            len(self.game_tree)-1))
    
    def __next_clicked(self, nextb):
        node = self.cursor.node
        (color,x,y) = self.__parse_node(node)
        
        self.goban.place_stone(color,x,y)
        
        self.move_num += 1
        self.__update_label()
        self.__update_sensitivity()
        self.cursor.next()
        
    def __end_clicked(self, endb):
        while self.move_num < len(self.game_tree)-1:
            print self.move_num
            self.__next_clicked(endb)
        
    def __prev_clicked(self, prevb):
        self.goban.undo()
        self.cursor.previous()
        self.move_num -= 1
        self.__update_label()
        self.__update_sensitivity()
        
    def __start_clicked(self, startb):
        while self.move_num > 0:
            self.__prev_clicked(startb)
        
    def __make_button_box(self):
        self.hbox = gtk.HBox()
        self.startb = self.__make_button(gtk.STOCK_MEDIA_REWIND)
        self.prevb = self.__make_button(gtk.STOCK_MEDIA_PREVIOUS)
        self.nextb = self.__make_button(gtk.STOCK_MEDIA_NEXT)
        self.endb = self.__make_button(gtk.STOCK_MEDIA_FORWARD)

        self.startb.set_sensitive(False)
        self.prevb.set_sensitive(False)
        self.nextb.set_sensitive(False)
        self.endb.set_sensitive(False)
        
        self.nextb.connect("clicked", self.__next_clicked)
        self.endb.connect("clicked", self.__end_clicked)
        self.startb.connect("clicked", self.__start_clicked)
        self.prevb.connect("clicked", self.__prev_clicked)


        self.__make_label()
        self.hbox.pack_start(self.startb)
        self.hbox.pack_start(self.prevb)
        self.hbox.pack_start(self.label)
        self.hbox.pack_start(self.nextb)
        self.hbox.pack_start(self.endb)
        
        
    def __setup_window(self):
        
        self.vbox = gtk.VBox()

        self.__make_embed()
        self.__make_button_box()
        
        self.vbox.pack_start(self.embed)
        self.vbox.pack_start(self.hbox)

        self.add(self.vbox)

        self.__setup_stage()
        
        
    def __parse_sgf(self,path):
        f = open(path, 'r')
        data = f.read()
        
        self.game_tree = zambogo.sgf.sgflib.SGFParser(data).parseOneGame()
        self.game_tree = self.game_tree.mainline()
        self.label.set_text("(0 of %s)" % (len(self.game_tree)-1,))
        self.cursor = self.game_tree.cursor()
        self.cursor.next()
        
        self.move_num = 0
        self.__update_sensitivity()
        
    def load_sgf(self,path):
        self.__parse_sgf(path)        

    def __init__(self):
        gtk.Window.__init__(self)
        
        self.__setup_window()
        self.show_all()
    
    
