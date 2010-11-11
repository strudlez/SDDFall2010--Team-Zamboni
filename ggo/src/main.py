#!/usr/bin/env python
import clutter
import gobanactor
import engine.board
import pygtk
pygtk.require('2.0')
import gtk
import cluttergtk

last_color = "white"
game_mode = "local"
handicap = 0
time = 60
bytime = 10

def gnugo_played(vertex):
    global last_color
    global pass_count
    last_color == "white"

def button_press(stage, event, goban):
    print event.x
    print event.y
    global last_color
    global game_mode
    global pass_count
    pass_count = 0
    if game_mode == "local":
        if last_color != "gameOver":
            if last_color == "white":
                last_color = "black"
            else:
                last_color = "white"
            goban.place_stone_at_position(last_color,event.x,event.y)
    if game_mode == "ai":
        if last_color == "white":
            if goban.place_stone_at_position("black",event.x,event.y):
                last_color == "black"
                goban.place_stone_gnugo("white",gnugo_played)

def forfeit_game(stage,goban):
    global last_color
    last_color = "gameOver"
    score =  goban.estimate_score()
    if score[0] == "B":
        print "Black Wins!"
    if score[0] == "W":
        print "White Wins!"
    print score

def pass_turn(stage,goban):
    global last_color
    global pass_count
    global game_mode
    if game_mode == "local":
        if last_color != "gameOver":
            if pass_count == 1:
                forfeit_game(stage, goban)
            if pass_count == 0:
                if last_color == "white":
                    last_color = "black"
                else:
                    last_color = "white"
                pass_count = 1
    if game_mode == "ai":
        if pass_count == 1:
            forfeit_game(stage, goban)
        if pass_count == 0:
            if last_color == "white":
                last_color == "black"
                goban.place_stone_gnugo("white",gnugo_played)
                pass_count = 1

def estimate_score(stage, goban):
    score = goban.estimate_score()
    if score != None:
        print score
def set_handicap(stage, pieces, goban):
    global game_mode
    global last_color
    global handicap
    handicap = pieces

def set_time(stage, goban, tim, bytim):
    global time
    global bytime
    time = tim
    bytime = bytim
    initialize_time(stage, goban)
        
def initialize_handicap(stage, goban):
    global handicap
    x_pos = [135, 351, 568]
    y_pos = [126, 347, 564]
    if handicap == 2:
        goban.place_stone_at_position("black", x_pos[2], y_pos[0])
        goban.place_stone_at_position("black", x_pos[0], y_pos[2])
    if handicap == 4:
        goban.place_stone_at_position("black", x_pos[2], y_pos[0])
        goban.place_stone_at_position("black", x_pos[0], y_pos[2])
        goban.place_stone_at_position("black", x_pos[2], y_pos[2])
        goban.place_stone_at_position("black", x_pos[0], y_pos[0])
    if handicap == 6:
        goban.place_stone_at_position("black", x_pos[2], y_pos[0])
        goban.place_stone_at_position("black", x_pos[0], y_pos[0])
        goban.place_stone_at_position("black", x_pos[2], y_pos[1])
        goban.place_stone_at_position("black", x_pos[0], y_pos[1])
        goban.place_stone_at_position("black", x_pos[2], y_pos[2])
        goban.place_stone_at_position("black", x_pos[0], y_pos[2])
    if handicap >= 0:
        if game_mode == "ai":
            goban.place_stone_gnugo("white", gnugo_played)
        if game_mode == "local":
            last_color == "black"

def initialize_time(stage, goban):
    global time
    global bytime
    goban.set_time(time, bytime)
    print goban.get_time("white")
        
        
class main_window:
    def destroy(self,evt):
        gtk.main_quit()
	
    def delete_evt(self,widget,event, data=None):
        pass
    def new_game(self,w,data):
        global game_mode
        game_mode = "local"
    def set_handicap(self,w,data):
        pass
    def new_teach_game(self,w,data):
        global game_mode
        game_mode = "ai"
    def load_game(self,w,data):
        print "To be implemented"
    def save_game(self,w,data):
        print "To be implemented"
    def start_game(self, stage, goban):
        initialize_handicap(self.stage, goban)
        set_time(self.stage, goban, self.time_entry.get_text(), self.time_entry.get_text())
    def settings_window(self,w,data):
        dialog = gtk.Dialog(None, None, gtk.DIALOG_MODAL)
        dialog.set_title("Settings")
        self.time_entry = gtk.Entry()
        self.time_entry.set_text("60")
        self.label = gtk.Label("Time Allowance:")
        self.by_entry = gtk.Entry()
        self.by_entry.set_text("10")
        self.label1 = gtk.Label("Byo-Yomi time:")

        self.r1 = gtk.RadioButton(None, "No Handicap")
        self.r1.connect("toggled", set_handicap, 0, self.goban)
        self.r1.set_active(True)
        dialog.vbox.pack_start(self.r1)
        self.r1.show()
        self.r1 = gtk.RadioButton(self.r1, "2 Stones")
        self.r1.connect("toggled", set_handicap, 2, self.goban)
        dialog.vbox.pack_start(self.r1)
        self.r1.show()
        self.r1 = gtk.RadioButton(self.r1, "4 Stones")
        self.r1.connect("toggled", set_handicap, 4, self.goban)
        dialog.vbox.pack_start(self.r1)
        self.r1.show()
        self.r1 = gtk.RadioButton(self.r1, "6 Stones")
        self.r1.connect("toggled", self.start_game, self.goban)
        dialog.vbox.pack_start(self.r1)
        self.r1.show()
        dialog.vbox.pack_start(self.label)
        dialog.vbox.pack_start(self.time_entry)
        dialog.vbox.pack_start(self.label1)
        dialog.vbox.pack_start(self.by_entry)

        
        accept_b=gtk.Button("Accept")
        accept_b.connect("clicked", self.start_game, self.goban, self.r1)
        accept_b.set_size_request(60,40)
        accept_b.show()

        self.r1.set_flags(gtk.CAN_DEFAULT)
        self.r1.grab_default()

        self.label.show()
        self.label1.show()
        self.time_entry.show()
        self.by_entry.show()
        dialog.run()
        dialog.destroy()
       
       
    def create_menu_bar(self,window):
        accel_group=gtk.AccelGroup()
        item_factr = gtk.ItemFactory(gtk.MenuBar, "<main>", accel_group)
        item_factr.create_items(self.menu_items)
        window.add_accel_group(accel_group)
        self.item_factr=item_factr
        return item_factr.get_widget("<main>")
	
    def __init__(self):
        
        self.board = engine.board.Board()
        self.goban = gobanactor.GobanActor(self.board)
        self.menu_items = (( "/_File",         None,         None, 0, "<Branch>" ),
        ( "/File/_New Game","<control>N", self.new_game, 0, None ),
        ( "/File/_New Teaching Game","<control>T", self.new_teach_game, 0, None ),
        ( "/File/_Open","<control>O", self.load_game, 0, None ),
        ( "/File/_Save","<control>S", self.save_game, 0, None ),
        ( "/File/sep1", None,None, 0, "<Separator>" ),
        ( "/File/Quit","<control>Q", gtk.main_quit, 0, None ),
        ( "/_Options",None,None, 0, "<Branch>" ),
        ( "/Options/_Settings","<control>R", self.settings_window, 0, None),
        ( "/_Help",None,None, 0, "<LastBranch>" ),
        ( "/_Help/About",None,None, 0, None ),)

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_evt)
        self.window.connect("destroy",self.destroy)
        self.embed = cluttergtk.Embed()

        menubar=self.create_menu_bar(self.window)
        menubar.show()
        self.toolbar = gtk.Toolbar()
        self.toolbar2 = gtk.Toolbar()
        self.game_board_container=gtk.HandleBox()

        self.toolbar.set_style(gtk.TOOLBAR_BOTH)

        self.top_box = gtk.VBox(False,2)
        self.menu_box = gtk.HBox(False,2)
        horiz_align = gtk.Alignment(0,0,1,0)

        self.menu_box.pack_start(menubar,False,True,0)
        self.top_box.pack_start(self.menu_box,False,True,0)
        separator = gtk.HSeparator()
        self.top_box.pack_start(separator,False,True,5)

        horiz_align.add(self.top_box)
        horiz_align.show()
        self.menu_box.show()
        separator.show()


        self.embed.realize()
        self.window.set_size_request(900, 700)
        hpane = gtk.HPaned()


        s_win = gtk.ScrolledWindow()
        s_win.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        s_win.add_with_viewport(self.embed)
        s_win.set_size_request(700, 700)
        s_win.show()

        self.game_board_container.add(s_win)
        #self.game_board_container.connect('child-detached', self.wrap_window, self.game_board_container)
        hpane.pack1(self.game_board_container, resize=True)
        hpane.set_position(700)


        self.stage = self.embed.get_stage() 
        self.stage.set_size(700,700)

        self.stage.add(self.goban)

        self.forfeit_b=gtk.Button("Forfeit")
        self.forfeit_b.connect("clicked", forfeit_game, self.goban)
        self.forfeit_b.set_size_request(60,40)
        self.forfeit_b.show()
        self.pass_b = gtk.Button("Pass")
        self.pass_b.connect("clicked", pass_turn, self.goban)
        self.pass_b.set_size_request(60,40)
        self.pass_b.show()
        self.estimate_b=gtk.Button("Estimate\nScore")
        self.estimate_b.connect("clicked", estimate_score, self.goban)
        self.estimate_b.set_size_request(60,40)
        self.estimate_b.show()


        self.toolbar.append_widget(self.forfeit_b,"End Game","Private")
        self.toolbar.append_widget(self.pass_b,"Pass Turn","Private")
        self.toolbar.append_widget(self.estimate_b,"Show estimate of current score","Private")
        self.top_box.pack_start(self.toolbar,True,True,0)

        self.top_box.show()
        hpane.pack2(horiz_align,resize=True)

        self.window.add(hpane)

        self.embed.show_all()

        self.stage.connect("delete-event",quit)
        self.stage.connect("button-press-event",button_press,self.goban)

        self.game_board_container.show()
        hpane.show()
        self.toolbar.show()
        self.embed.show()
        self.window.show()
        self.settings = self.settings_window(0,None)

    def main(self):
        gtk.main()
	
if __name__=="__main__":
    win = main_window()
    win.main()
