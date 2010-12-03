#!/usr/bin/env python

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


import clutter
import gobanactor
import engine.board
import pygtk
pygtk.require('2.0')
import gtk
import gobject
import cluttergtk
import time
#This is our initialiazation, ui, and user input file.
last_color = "white"
game_mode = "local"
handicap = 0
difficulty = 1
time = 60
bytime = 10

def gnugo_played(vertex): #Called after GnuGo places a stone
    global last_color 
    last_color = "white" #The last color is set to white, GnuGo's color

def button_press(stage, event, goban):
    global last_color
    global game_mode
    global pass_count
    pass_count = 0
    if game_mode == "local": #If we are playing in local mode, alternate colors placed by player
        print last_color
        col=last_color
        if last_color != "gameOver":
            if last_color == "white":
                last_color = "black"
            else:
                last_color = "white"
            if goban.place_stone_at_position(last_color,event.x,event.y):
                if last_color!="gameOver":
                    goban.timers[last_color].stop() #stop last player's timer
                    goban.timers[col].start() #start current player's timer
    if game_mode == "ai": #If we are playing in AI mode, the player plays black, and then the AI plays white
        if last_color == "white":
            if goban.place_stone_at_position("black",event.x,event.y):
                goban.timers["black"].stop() #stop player's timer
                last_color == "black"
                goban.place_stone_gnugo("white",gnugo_played)

def forfeit_game(stage,goban): #Functionality for the forfeit button in the sidepane - if it is pressed, last_color becomes gameOver to ensure no more stones are placed
    global last_color
    last_color = "gameOver"
    score =  goban.estimate_score() #Score is estimated by gnuGo and the winner is printed below
    if score[0] == "B":
        print "Black Wins!" 
    if score[0] == "W":
        print "White Wins!"
    print score
    
    for i in ['black','white']:
        goban.timers[i].inited=0
def pass_turn(stage,goban): #Functionality for the pass button in the sidepane - if the pass button is pressed, the player forfeits their turn.  If the pass button is pressed twice in a row, the game ends.
    global last_color
    global pass_count
    global game_mode
    if game_mode == "local": #If game mode is local, skip the current color and set pass_count to 1 if pass_count is 0 - else, end the game
        if last_color != "gameOver":
            if pass_count == 1:
                forfeit_game(stage, goban)
                goban.timers["white"].stop()
                goban.timers["black"].stop()
                #Stop timers
            if pass_count == 0:
                goban.timers[last_color].start()
                if last_color == "white":
                    
                    last_color = "black"
                else:
                    last_color = "white"
                goban.timers[last_color].stop()
                
                pass_count = 1
    if game_mode == "ai": #If game mode is AI, let AI play and set pass_count to 1.  If the player passes again, then end the game.
        if pass_count == 1:
            forfeit_game(stage, goban)
        if pass_count == 0:
            if last_color == "white":
                last_color == "black"
                goban.place_stone_gnugo("white",gnugo_played)
                pass_count = 1

def estimate_score(stage, goban): #print the estimated score
    score = goban.estimate_score()
    if score != None:
        print score
def set_handicap(stage, pieces, goban): #Set the number of handicap pieces to place when the board is initialized
    global handicap
    handicap = pieces

def set_difficulty(stage, slider, goban): #Set the number of handicap pieces to place when the board is initialized
    global difficulty
    difficulty=int(slider.get_value())

def set_time(stage, goban, tim, bytim): #Sets the variables that store time to the desired settings
    global time
    global bytime
    time = tim
    bytime = bytim
    initialize_time(stage, goban)
        
def initialize_handicap(stage, goban, clear=1): #Place stones at the typical positions in case there is a handicap
    global handicap
    global last_color
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
    if handicap > 0:
        if game_mode == "ai": #If game mode is AI, the AI, being white, immediately plays
            print(handicap)
            goban.place_stone_gnugo("white", gnugo_played)
        if game_mode == "local": #If game mode is local, switch the next piece placed to white
            last_color = "black"

def initialize_time(stage, goban): #Initializes the game clock with the desired amount of time.
    global time
    global bytime
    goban.set_time(time, bytime)
        
class main_window:
    def destroy(self,evt):
        gtk.main_quit()
    def delete_evt(self,widget,event, data=None):
        pass
    def new_game(self,w,data): #Sets the game mode to local
        global game_mode
        game_mode = "local"
        self.settings = self.settings_window(0,None, clear=1)
        
    def new_teach_game(self,w,data): #Sets the game mode to AI
        global game_mode
        game_mode = "ai"
        self.settings = self.settings_window(0,None, clear=1)
        
    def load_game(self,w,data): #For viewing past games
        print "To be implemented"
    def save_game(self,w,data): #For recording games
        print "To be implemented"
        
        
    
    def update_timer(self,goban): #Gets the current timer for both players, and forfeits if one runs out.  Reruns itself every half-second
        if last_color!="gameOver" and goban.timers['white'].inited and goban.timers['black'].inited:
            for color in ["white","black"]:
                time=goban.timers[color].get_time_str()
                if goban.timers[color].get_time()<=0: forfeit_game(None,goban)
                if color=="white":self.time_white.set_text(time)
                elif color=="black":self.time_black.set_text(time)
            
        gobject.timeout_add(500,self.update_timer,goban)
        
    def set_history(self, widget, data):
		move=self.place_in_hist
		print "Move is..."
		print move
		hist_remove_btn=self.goban.set_board(move)#Set the board back to this move
		print "Buttons to remove..."
		print hist_remove_btn
		count=0
		while count!=hist_remove_btn:
			last_btn=self.button_box.get_children().pop()
			last_btn.destroy()
			count=count+1
		global last_color
		if(int(move)%2 == 0):
			last_color="white"
			self.goban.current_color="black"
		else:
			last_color="black"
			self.goban.current_color="white"
			
			
    def disp_history(self, widget, data):
        color,parent,move_num = data.split(' ')
        self.place_in_hist=move_num
        self.goban.update_stones(alt_board=self.goban.history[int(move_num)-1])
        print color
    def add_hist_button(self,move_num, parent, color):
        self.place_in_hist=int(self.place_in_hist)+1
        button = gtk.Button()
        label = gtk.Label("%d "%move_num)
        box = gtk.HBox(False, 0)
        button.connect("clicked", self.disp_history, "%s %s %s" % (color,parent,move_num))
        image = gtk.Image()
        if(color=="white"):
            pixbuf = gtk.gdk.pixbuf_new_from_file("white.png")
            scaled_buf = pixbuf.scale_simple(18,18,gtk.gdk.INTERP_BILINEAR)
            image.set_from_pixbuf(scaled_buf)
    
        else:
            pixbuf = gtk.gdk.pixbuf_new_from_file("black.png")
            scaled_buf = pixbuf.scale_simple(18,18,gtk.gdk.INTERP_BILINEAR)
            image.set_from_pixbuf(scaled_buf)
        image.show()
        label.show()
        box.pack_start(image, False, False, 3)
        box.pack_start(label, False, False, 1)
        button.add(box)
        box.show()
        button.set_size_request(28,24)
        button.show()
        self.button_box.pack_start(button, False, False, 5)
    def start_game(self, stage, goban,dialog,clear=1): #Places handicap stones and initializes the game clock based on the choices made in the settings window.
        #clear the board
        if clear:
            goban.board.__init__()
            goban.update_stones()
            for i in self.button_box.get_children(): i.destroy()
            goban.history=[]
            global last_color
            if last_color == "gameOver":
                last_color = "white"
            
        goban.board.gtp.level(difficulty)
        initialize_handicap(self.stage, goban)
        
        
        
        set_time(self.stage, goban, self.time_entry.get_text(), self.by_entry.get_text())
        
        #start the current player's timer
        goban.timers["white" if last_color=="black" else "black"].start()
        
        dialog.destroy()
        
    def main_menu(self, w, data): #Initializes the main menu of game modes
        dialog = gtk.Dialog(None, None, gtk.DIALOG_MODAL)
        dialog.set_size_request(150,90)
        dialog.set_title("Main Menu")
        local_b=gtk.Button("Local Play") #Button for local play
        local_b.connect("clicked", self.start_local, self.goban, dialog)

        local_b.set_size_request(70,40)
        local_b.show()
        dialog.vbox.pack_start(local_b)
        ai_b=gtk.Button("AI Play") #Button for AI play
        ai_b.connect("clicked", self.start_ai, self.goban, dialog)

        ai_b.set_size_request(70,40)
        ai_b.show()
        dialog.vbox.pack_start(ai_b)
        dialog.run()
        dialog.destroy()
    def start_local(self, stage, goban, dialog): #Starts a game in local mode
        global game_mode
        game_mode = "local"
        dialog.destroy()
        self.settings = self.settings_window(0,None)
    def start_ai(self, stage, goban, dialog): #Starts a game in AI mode
        global game_mode
        game_mode = "ai"
        dialog.destroy()
        self.settings = self.settings_window(0,None)
    def settings_window(self,w,data, clear=0): #Creates a window with radio buttons for handicap stone number and text entry fields to desired amount of time and byo-yomi time
        dialog = gtk.Dialog(None, None, gtk.DIALOG_MODAL)
        dialog.set_title("Settings")
        self.time_entry = gtk.Entry() #Prepares the text entry fields
        self.time_entry.set_text("60")
        self.label = gtk.Label("Time Allowance:")
        self.by_entry = gtk.Entry()
        self.by_entry.set_text("10")
        self.label1 = gtk.Label("Byo-Yomi time:")

        self.r1 = gtk.RadioButton(None, "No Handicap") #Sets up the radio buttons
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
        self.r1.connect("toggled", set_handicap, 6, self.goban)
        dialog.vbox.pack_start(self.r1)
        self.r1.show()
        if game_mode == "ai":
            self.label2 = gtk.Label("Difficulty:")
            self.label2.show()
            self.difficult_scale=gtk.HScale()
            self.difficult_scale.set_digits(0);
            self.difficult_scale.set_range(1,10);
            self.difficult_scale.connect("value_changed", set_difficulty, self.difficult_scale, self.goban)
            self.difficult_scale.show();
        
        dialog.vbox.pack_start(self.label)
        dialog.vbox.pack_start(self.time_entry)
        dialog.vbox.pack_start(self.label1)
        dialog.vbox.pack_start(self.by_entry)
        
        if game_mode == "ai":
            dialog.vbox.pack_start(self.label2)
            dialog.vbox.pack_start(self.difficult_scale)

        
        accept_b=gtk.Button("Accept") #Accept button to finalize setting choices
        accept_b.connect("clicked", self.start_game, self.goban, dialog, clear)
        accept_b.set_size_request(60,40)
        accept_b.show()
        dialog.vbox.pack_start(accept_b)

        self.r1.set_flags(gtk.CAN_DEFAULT)
        self.r1.grab_default()
        
        self.label.show()
        self.label1.show()
        self.time_entry.show()
        self.by_entry.show()
        dialog.run()
        dialog.destroy()
       
       
    def create_menu_bar(self,window): #Create all the File, Options, and Help drop down menus at the top of the screen
        accel_group=gtk.AccelGroup()
        item_factr = gtk.ItemFactory(gtk.MenuBar, "<main>", accel_group)
        item_factr.create_items(self.menu_items)
        window.add_accel_group(accel_group)
        self.item_factr=item_factr
        return item_factr.get_widget("<main>")
    
    def __init__(self):
        self.place_in_hist=0
        self.menu_items = (( "/_File",         None,         None, 0, "<Branch>" ), #Sets up the menu items for future use
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

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)  #Initializes a window
        self.window.connect("delete_event", self.delete_evt)
        self.window.connect("destroy",self.destroy)
        self.embed = cluttergtk.Embed()

        menubar=self.create_menu_bar(self.window) #Creates the menubar and makes it viewable
        menubar.show()
        self.toolbar = gtk.Toolbar() #Creates two toolbars for use in storing UI widgets, and a game_board_container to handle the actual game display
        self.toolbar2 = gtk.Toolbar()
        self.game_board_container=gtk.HandleBox()

        self.toolbar.set_style(gtk.TOOLBAR_BOTH)

        self.top_box = gtk.VBox(False,2)
        self.button_box = gtk.HBox(False,2)#for history buttons
        hist_buttons_align=gtk.Alignment(0,0,1,0)
        hist_buttons_align.add(self.button_box)
        self.menu_box = gtk.HBox(False,2)
        horiz_align = gtk.Alignment(0,0,1,0)

        self.menu_box.pack_start(menubar,False,True,0)
        self.top_box.pack_start(self.menu_box,False,True,0)
        separator = gtk.HSeparator()
        self.top_box.pack_start(separator,False,True,5)

        horiz_align.add(self.top_box)
        hist_buttons_align.add(self.button_box)


		
        self.embed.realize()
        self.window.set_size_request(1200, 700)
        hpane = gtk.HPaned()
        self.vpane = gtk.VPaned()

		#Undo History Button
        global game_mode
        if(game_mode!="ai"):
			undo = gtk.Button("Undo")
			undo.connect("clicked", self.set_history, self.place_in_hist)
			self.button_box.pack_start(undo, False, False, 5)
		
        s_win = gtk.ScrolledWindow()
        s_win.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        s_win.add_with_viewport(self.embed)
        s_win.set_size_request(700, 700)


        hs_win = gtk.ScrolledWindow()
        hs_win.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        hs_win.add_with_viewport(hist_buttons_align)
        hs_win.set_size_request(700, 700)

        self.game_board_container.add(s_win)
        #self.game_board_container.connect('child-detached', self.wrap_window, self.game_board_container)
        hpane.pack1(self.game_board_container, resize=True)
        hpane.set_position(700)


        self.stage = self.embed.get_stage() 
        self.stage.set_size(700,700)

        self.board = engine.board.Board()
        self.goban = gobanactor.GobanActor(self.board, self)
        self.stage.add(self.goban)

        self.forfeit_b=gtk.Button("Forfeit")  #Sets up a Forfeit, Pass, and Estimate Score button for the sidepane
        self.forfeit_b.connect("clicked", forfeit_game, self.goban)
        self.forfeit_b.set_size_request(80,50)
        self.pass_b = gtk.Button("Pass")
        self.pass_b.connect("clicked", pass_turn, self.goban)
        self.pass_b.set_size_request(80,50)
        self.estimate_b=gtk.Button("Estimate\nScore")
        self.estimate_b.connect("clicked", estimate_score, self.goban)
        self.estimate_b.set_size_request(80,50)
        
        
        #Timer labels
        self.time_white_label = gtk.Label("White: ")
        self.time_black_label = gtk.Label("Black: ")
        self.time_white_label.show()
        self.time_black_label.show()
        
        self.time_white = gtk.Entry()
        self.time_black = gtk.Entry()
        
        #Timers
        self.time_white.set_editable(False)
        self.time_black.set_editable(False)
        
        self.time_white.set_width_chars(8)
        self.time_black.set_width_chars(8)
        
        self.time_white.show()
        self.time_black.show()


        self.toolbar.append_widget(self.forfeit_b,"End Game","Private") #Appens all the widgets to the toolbar and packs the toolbar into a Vbox
        self.toolbar.append_widget(self.pass_b,"Pass Turn","Private")
        self.toolbar.append_widget(self.estimate_b,"Show estimate of current score","Private")
        self.toolbar.append_widget(self.time_white_label, "Show time remaining","Private")
        self.toolbar.append_widget(self.time_white, "Show time remaining","Private")
        self.toolbar.append_widget(self.time_black_label, "Show time remaining","Private")
        self.toolbar.append_widget(self.time_black, "Show time remaining","Private")
        self.top_box.pack_start(self.toolbar,True,True,0)
        hpane.pack2(self.vpane,resize=True)
        self.vpane.pack1(horiz_align,resize=True)
        self.vpane.pack2(hs_win,resize=True)
        self.vpane.set_position(300)

        self.window.add(hpane)

        self.embed.show_all()

        self.stage.connect("delete-event",quit)
        self.stage.connect("button-press-event",button_press,self.goban)

        self.game_board_container.show()
        self.toolbar.show()
        self.embed.show()
        self.window.show_all()
        self.mm = self.main_menu(0,None)
        
        self.update_timer(self.goban)
        
    def main(self):
        gtk.main()
    
if __name__=="__main__":
    win = main_window()
    win.main()
