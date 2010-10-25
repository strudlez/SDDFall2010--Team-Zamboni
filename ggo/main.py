#!/usr/bin/env python
import clutter
import gobanactor
import engine.board

last_color = "black"

def button_press(stage, event, goban):
    global last_color
    if goban.place_stone_at_position(last_color,event.x,event.y):
        if last_color == "white":
            last_color = "black"
        else:
            last_color = "white"


if __name__=="__main__":
    stage = clutter.Stage()
    stage.show()

    stage.set_minimum_size(700,700)


    board = engine.board.Board()
    goban = gobanactor.GobanActor(board)
    stage.add(goban)
    
    stage.show_all()
    
    
    stage.connect("delete-event",quit)
    stage.connect("button-press-event",button_press,goban)

    clutter.main()
