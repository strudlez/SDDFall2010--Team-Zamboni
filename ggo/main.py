#!/usr/bin/env python
import clutter
import gobanactor
import engine.board
import pygtk
pygtk.require('2.0')
import gtk


last_color = "black"

def button_press(stage, event, goban):
    global last_color
    if goban.place_stone_at_position(last_color,event.x,event.y):
        if last_color == "white":
            last_color = "black"
        else:
            last_color = "white"

class main_window:
	def destroy(self):
		gtk.main_quit()
		
	def delete_evt(self,widget,event, data=None):
		pass
	
	
	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("delete_event", self.delete_evt)
		self.window.connect("destroy",self.destroy)
		self.embed = clutter.cluttergtk.Embed()
		self.window.add(self.embed)
		self.embed.show()


		self.embed.realize()
		windowSize = self.window.get_size()
		self.embed.set_size_request(windowSize[0],windowSize[1])
		stage = self.embed.get_stage() 
		stage.set_minimum_size(700,700)

		board = engine.board.Board()
		goban = gobanactor.GobanActor(board)
		stage.add(goban)
		
		stage.show_all()
		stage.show()
		
		stage.connect("delete-event",quit)
		stage.connect("button-press-event",button_press,goban)

		clutter.main()
		self.window.show()

	def main(self):
		gtk.main()
		
if __name__=="__main__":
	win = main_window()
	win.main()
