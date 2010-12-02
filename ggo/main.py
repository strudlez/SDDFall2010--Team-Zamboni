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
	def new_game(self,w,data):
		pass
	def set_handicap(self,w,data):
		pass
	def new_teach_game(self,w,data):
		pass
	def load_game(self,w,data):
		pass
	def save_game(self,w,data):
		pass
	def disp_history(self, widget, data):
		color,parent,move_num=data.split(' ')
		self.goban._update_stones(alt_board=self.goban.history[int(move_num)-1])
		
		print color
	def add_hist_button(self,move_num, parent, color):
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
		
		self.toolbar = gtk.Toolbar()
		self.toolbar2 = gtk.Toolbar()
		self.game_board_container=gtk.HandleBox()

		self.toolbar.set_style(gtk.TOOLBAR_BOTH)
		
		self.top_box = gtk.VBox(False,2)
		
		self.button_box = gtk.HBox(False,2)#for history buttons
		hist_buttons_align=gtk.Alignment(0,0,1,0)
		
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
		
		board = engine.board.Board()
		self.goban = gobanactor.GobanActor(board,self)
		self.stage.add(self.goban)
		
		self.forfeit_b=gtk.Button("Forfeit")
		self.forfeit_b.set_size_request(60,40)

		self.pass_b = gtk.Button("Pass")
		self.pass_b.set_size_request(60,40)

		self.estimate_b=gtk.Button("Estimate\nScore")
		self.estimate_b.set_size_request(60,40)
		
		self.toolbar.append_widget(self.forfeit_b,"End Game","Private")
		self.toolbar.append_widget(self.pass_b,"Pass Turn","Private")
		self.toolbar.append_widget(self.estimate_b,"Show estimate of current score","Private")
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

	def main(self):
		gtk.main()
		
if __name__=="__main__":
	win = main_window()
	win.main()
