import clutter

class GobanActor(clutter.Group):
    def __init__(self):
        self.background = clutter.Texture.new_from_file("goban.png")
        self.add_actor(background)
        self.show_all()
