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

def gnugo_played(vertex):
    global last_color
    last_color == "white"

def button_press(stage, event, goban):
    global last_color
    global game_mode
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

def pass_turn(stage):
    global last_color
    if last_color != "gameOver":
        if last_color == "white":
            last_color = "black"
        else:
            last_color = "white"

def estimate_score(stage, goban):
    score = goban.estimate_score()
    if score != None:
        print score

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
    def settings_window(self,w,data):
        dialog = gtk.Dialog(None, None, gtk.DIALOG_MODAL)
        dialog.set_title("Settings")
        time_entry = gtk.Entry()
        label = gtk.Label("Time Allowance:")

        r1 = gtk.RadioButton(None, "No Handycap")
        r1.connect("toggled", self.set_handicap, "No Handycap")
        r1.set_active(True)
        dialog.vbox.pack_start(r1)
        r1.show()
        r1 = gtk.RadioButton(r1, "2 Stones")
        r1.connect("toggled", self.set_handicap, "2 Stones")
        dialog.vbox.pack_start(r1)
        r1.show()
        r1 = gtk.RadioButton(r1, "4 Stones")
        r1.connect("toggled", self.set_handicap, "4 Stones")
        dialog.vbox.pack_start(r1)
        r1.show()
        r1 = gtk.RadioButton(r1, "6 Stones")
        r1.connect("toggled", self.set_handicap, "6 Stones")
        dialog.vbox.pack_start(r1)
        r1.show()
        dialog.vbox.pack_start(label)
        dialog.vbox.pack_start(time_entry)


        r1.set_flags(gtk.CAN_DEFAULT)
        r1.grab_default()

        label.show()
        time_entry.show()
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
        self.menu_items = (( "/_File",         None,         None, 0, "<Branch>" ),
        ( "/File/_New Game","<control>N", self.new_game, 0, None ),
        ( "/File/_New Teaching Game","<control>T", self.new_teach_game, 0, None ),
        ( "/File/_Open","<control>O", self.load_game, 0, None ),
        ( "/File/_Save","<control>S", self.save_game, 0, None ),
        ( "/File/sep1", None,None, 0, "<Separator>" ),
        ( "/File/Quit","<control>Q", gtk.main_quit, 0, None ),
        ( "/_Options",None,None, 0, "<Branch>" ),
        ( "/Options/_Settings","<control>R", self.settings_window, 0, None ),
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

        board = engine.board.Board()
        goban = gobanactor.GobanActor(board)
        self.stage.add(goban)

        self.forfeit_b=gtk.Button("Forfeit")
        self.forfeit_b.connect("clicked", forfeit_game, goban)
        self.forfeit_b.set_size_request(60,40)
        self.forfeit_b.show()
        self.pass_b = gtk.Button("Pass")
        self.pass_b.connect("clicked", pass_turn)
        self.pass_b.set_size_request(60,40)
        self.pass_b.show()
        self.estimate_b=gtk.Button("Estimate\nScore")
        self.estimate_b.connect("clicked", estimate_score, goban)
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
        self.stage.connect("button-press-event",button_press,goban)

        self.game_board_container.show()
        hpane.show()
        self.toolbar.show()
        self.embed.show()
        self.window.show()

    def main(self):
        gtk.main()
	
if __name__=="__main__":
    win = main_window()
    win.main()
