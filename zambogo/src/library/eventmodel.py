import pygtk
import gtk
import zambogo.sgf.database

class EventModel(gtk.GenericTreeModel):
    column_types = (str,)
    column_names = ["Name"]
    
    def __init__(self):
        gtk.GenericTreeModel.__init__(self)
        self.database = zambogo.sgf.database.get_default()
        self.events = self.database.list_events()
        self.events = ["All %s events" % (len(self.events))] + self.events
        
    def get_column_names(self):
        return self.column_names[:]
    
    def on_get_flags(self):
        return gtk.TREE_MODEL_LIST_ONLY | gtk.TREE_MODEL_ITERS_PERSIST
    
    def on_get_n_columns(self):
        return len(self.column_types)
    
    def on_get_column_type(self, n):
        return self.column_types[n]
    
    def on_get_iter(self, path):
        if path is None:
            return self.events[0]
        try:
            return self.events[path[0]]
        except KeyError:
            return None
    
    def on_get_path(self, rowref):
#        if not rowref:
 #           return 0
        return self.events.index(rowref)
    
    def on_get_value(self, rowref, column):
        if column is 0:
            return rowref
    def on_iter_next(self, rowref):
        try:
            i = self.events.index(rowref)+1
            return self.events[i]
        except IndexError:
            return None
    def on_iter_children(self, rowref):
        if rowref is not None:
            return None
        return self.events[0]

    def on_iter_has_child(self, rowref):
        return False
    
    def on_iter_n_children(self, rowref):
        if rowref:
            return 0
        return len(self.events)
    
    def on_iter_nth_child(self, rowref, n):
        if rowref:
            return None
        try: 
            event = self.events[n]
            return n
        except IndexError:
            return None

    def on_iter_parent(child):
        return None

    
