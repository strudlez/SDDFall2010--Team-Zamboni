#!/usr/bin/python
#
# main.py
# Copyright (C) racarr 2010 <racarr@gnome.org>
# 
# ggo is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# ggo is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.


#!/usr/bin/env python
import clutter
import gobanactor
import engine.board

playerMove = True

def gnugo_played(vertex):
    global playerMove
    playerMove = True
    

def button_press(stage, event, goban):
    global playerMove
    
    if playerMove == True:
        if goban.place_stone_at_position("black",event.x,event.y):
            playerMove = False
            goban.place_stone_gnugo("white",gnugo_played)

def quit_callback(*args):
    quit()

if __name__=="__main__":
    stage = clutter.Stage()
    stage.show()

    stage.set_minimum_size(700,700)


    board = engine.board.Board()
    goban = gobanactor.GobanActor(board)
    stage.add(goban)
    
    stage.show_all()
    
    
    stage.connect("delete-event",quit_callback)
    stage.connect("button-press-event",button_press,goban)

    clutter.main()
