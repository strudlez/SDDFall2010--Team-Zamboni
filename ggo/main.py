#!/usr/bin/env python
import clutter
import gobanactor
import engine.board
import pygtk
pygtk.require('2.0')
import gtk
import cluttergtk

last_color = "black"

def button_press(stage, event, goban):
    global last_color
    if goban.place_stone_at_position(last_color,event.x,event.y):
        if last_color == "white":
            last_color = "black"
        else:
            last_color = "white"

class main_window:
	def destroy(self,evt):
		gtk.main_quit()
		
	def delete_evt(self,widget,event, data=None):
		pass
	def new_game(self):
		pass
	def load_game(self):
		pass
	def save_game(self):
		pass
	def settings_window(self):
		pass
	def create_menu_bar(self,window):
		accel_group=gtk.AccelGroup()
		item_factr = gtk.ItemFactory(gtk.MenuBar, "<main>", accel_group)
		item_factr.create_items(self.menu_items)
		window.add_accel_group(accel_group)
		self.item_factr=item_factr
		return item_factr.get_widget("<main>")
	
	def __init__(self):
		self.menu_items = (( "/_File",         None,         None, 0, "<Branch>" ),
		( "/File/_New","<control>N", self.new_game, 0, None ),
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
		hpane.pack1(self.game_board_container, resize=True)
		hpane.set_position(700)
		
		
		self.stage = self.embed.get_stage() 
		self.stage.set_size(700,700)
		
		board = engine.board.Board()
		goban = gobanactor.GobanActor(board)
		self.stage.add(goban)
		
		self.forfeit_b=gtk.Button("Forfeit")
		self.forfeit_b.set_size_request(60,40)
		self.forfeit_b.show()
		self.pass_b = gtk.Button("Pass")
		self.pass_b.set_size_request(60,40)
		self.pass_b.show()
		
		self.toolbar.append_widget(self.forfeit_b,"End Game","Private")
		self.toolbar.append_widget(self.pass_b,"Pass Turn","Private")
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
