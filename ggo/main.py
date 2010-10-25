#!/usr/bin/env python


import clutter
import gobanactor

last_color = gobanactor.Black

def button_press(stage, event, goban):
    global last_color
    if goban.place_stone_at_position(last_color,event.x,event.y):
        if last_color == gobanactor.White:
            last_color = gobanactor.Black
        else:
            last_color = gobanactor.White


if __name__=="__main__":
    stage = clutter.Stage()
    stage.show()

    stage.set_minimum_size(700,700)


    goban = gobanactor.GobanActor()
    stage.add(goban)
    
    stage.show_all()
    
    
    stage.connect("delete-event",quit)
    stage.connect("button-press-event",button_press,goban)

    clutter.main()
