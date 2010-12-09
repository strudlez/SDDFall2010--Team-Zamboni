import pygtk
import gtk

import zambogo.sgf.database

class LibraryModel(gtk.GenericTreeModel):
    column_types = (str, str, int, str, str, str, str, str)
    column_names = ['White', 'Black', "ID", 'Event', 'Date', 'Komi', 'Handicap','Result']
    

    def __path_to_id(self, path):
            return path+1

    def __init__(self):
        gtk.GenericTreeModel.__init__(self)
        
        self.database = zambogo.sgf.database.get_default()
        
    def get_column_names(self):
        return self.column_names[:]
    
    def on_get_flags(self):
        return gtk.TREE_MODEL_LIST_ONLY|gtk.TREE_MODEL_ITERS_PERSIST
    
    def on_get_n_columns(self):
        return len(self.column_types)
    
    def on_get_column_type(self,n):
        return self.column_types[n]
    
    def on_get_iter(self, path):
        if path is None:
            return self.database.infos[self.__path_to_id(0)]
        try:
            return self.database.infos[self.__path_to_id(path[0]+1)]
        except KeyError:
            return None
    
    def on_get_path(self, rowref):
        return (rowref.id-1,)
    
    def on_get_value(self, rowref, column):
        game = rowref
        if column is 0:
            return game.props["PW"]
        elif column is 1:
            return game.props["PB"]
        elif column is 2:
            return game.id
        elif column is 3:
            return game.props["EV"]
        elif column is 4:
            return game.props["DT"]
        elif column is 5:
            return game.props["KM"]
        elif column is 6:
            return game.props["HA"]
        elif column is 7:
            return game.props["RE"]
    
    def on_iter_next(self, rowref):
        try:
            path = self.on_get_path(rowref)
            return self.database.infos[self.__path_to_id(path[0]+1)]
        except KeyError,IndexError:
            return None

    def on_iter_children(self,rowref):
        if rowref:
            return None
        return self.database.infos[self.__path_to_id(0)]
    
    def on_iter_has_child(self, rowref):
        return False
    
    def on_iter_n_children(self, rowref):
        if rowref:
            return 0
        return len(self.database.infos.keys())

    
    def on_iter_nth_child(self, rowref, n):
        if rowref:
            return None
        try:
#            info = self.database.infos[n+1]
            return n+1
        except KeyError:
            return None

    def on_iter_parent(self, child):
        return None
        


