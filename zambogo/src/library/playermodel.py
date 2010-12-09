import pygtk
import gtk
import zambogo.sgf.database

class PlayerModel(gtk.GenericTreeModel):
    column_types = (str,)
    column_names = ["Name"]
    
    def __init__(self):
        gtk.GenericTreeModel.__init__(self)
        self.database = zambogo.sgf.database.get_default()
        self.players = self.database.list_players()
        self.players = ["All %s players" % (len(self.players))] + self.players
        
    def get_column_names(self):
        return self.column_names[:]
    
    def on_get_flags(self):
        return gtk.TREE_MODEL_LIST_ONLY | gtk.TREE_MODEL_ITERS_PERSIST
    
    def on_get_n_columns(self):
        return len(self.column_types)
    
    def on_get_column_type(self, n):
        return self.column_types[n]
    
    def on_get_iter(self, path):
        return self.players[path[0]]
    
    def on_get_path(self, rowref):
        if not rowref:
            return 0
        return self.players.index(rowref)
    
    def on_get_value(self, rowref, column):
        if column is 0:
            return rowref
    def on_iter_next(self, rowref):
        try:
            i = self.players.index(rowref)+1
            return self.players[i]
        except IndexError:
            return None
    def on_iter_children(self, rowref):
        if rowref:
            return None
        return self.players[0]

    def on_iter_has_child(self, rowref):
        return False
    
    def on_iter_n_children(self, rowref):
        if rowref:
            return 0
        return len(self.players)
    
    def on_iter_nth_child(self, rowref, n):
        if rowref:
            return None
        try: 
            return self.players[n]
        except IndexError:
            return None

    def on_iter_parent(child):
        return None
    
