import pygtk
import gtk
import eventmodel
import zambogo.sgf.database

class EventTreeView(gtk.TreeView):
    
    def clear_filters(self):
        self.filter_events = None
        self.filter.refilter()
        
    def filter_player(self, player):
        events = set()
        
        d = zambogo.sgf.database.get_default()
        es = d.get_events_with_players([player])

        for event in es:
            events.add(event)
            
        if self.filter_events is None:
            self.filter_events = events
        else:
            self.filter_events = self.filter_events.intersection(filter_events)

        self.filter.refilter()
        
        
    def __filter_func(self,model,info):
        if self.filter_events is None:
            return True
        else:
            event = model.get(info, 0)[0].decode("utf-8")
            return event in self.filter_events
    
    def __selected_function(self, info):
        if self.__guard is True:
            return True
        self.__guard = True

        path = info[0]

        if path != 0:
            self.selection.unselect_path(0)
            return True

        self.selection.unselect_all()
        self.__guard = False
        
        return True

    def __add_column(self, name, mcolumn):
        cell = gtk.CellRendererText()
        column = gtk.TreeViewColumn(name, cell, text = mcolumn)
        self.append_column(column)
        
    def __add_columns(self):
        self.__add_column("Event", 0)
    
    def __init__(self):
        gtk.TreeView.__init__(self)

        self.__guard = False
        self.database = zambogo.sgf.database.get_default()
        self.model = eventmodel.EventModel()
        
        self.filter = self.model.filter_new()
        self.filter.set_visible_func(self.__filter_func)
        
        self.clear_filters()
        
        self.set_model(self.filter)
        
        self.__add_columns()
        
        self.selection = self.get_selection()
        self.selection.set_mode(gtk.SELECTION_MULTIPLE)
        
        self.selection.set_select_function(self.__selected_function)
    
    def get_selected_events(self):
        events = []
        selection = self.get_selection()
        a = selection.get_selected_rows()
        paths = a[1]
        for path in paths:
            if (path[0] == 0): return None
            it = self.filter.get_iter(path)
            events.append(self.filter.get(it,0))
        return events
        
    
