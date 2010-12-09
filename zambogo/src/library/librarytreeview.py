import pygtk
import gtk
import librarymodel
import zambogo.sgf.database

class LibraryTreeView(gtk.TreeView):
    
    def clear_filters(self):
        self.player_ids = None
        self.event_ids = None
        self.filter.refilter()
    
    def clear_event_filters(self):
        self.event_ids = None
        self.filter.refilter()
        
    def clear_player_filters(self):
        self.player_ids = None
        self.filter.refilter()
        
    def __refilter(self):
        self.filter.refilter()
        
    def filter_event(self, event):
        ids = set()
        d = zambogo.sgf.database.get_default()
        games = d.get_games_with_event(event)
        
        for game in games:
            ids.add(game)
        
        if self.event_ids is None:
            self.event_ids = ids
        else:
            self.event_ids = self.event_ids.union(ids)
            
        self.__refilter()
            
    
    def filter_player(self, player):
        ids = set()
        d = zambogo.sgf.database.get_default()
        games = d.get_games_with_player(player)

        for game in games:
            ids.add(game)
            
        if self.player_ids is None:
            self.player_ids = ids
        else:
            self.player_ids = self.player_ids.intersection(ids)
        self.__refilter()

        
    def __filter_func(self,model,info):
        if self.player_ids is None and self.event_ids is None:
            return True
        else:
            id = model.get(info,2)
            ret = True
            if self.player_ids is not None:
                ret = ret and id[0] in self.player_ids
            if self.event_ids is not None:
                ret = ret and id[0] in self.event_ids
            return ret

    def __add_column(self, name, mcolumn):
        cell = gtk.CellRendererText()
        column = gtk.TreeViewColumn(name, cell, text = mcolumn)
        column.set_resizable(True)
        column.set_expand(False)
        self.append_column(column)
        
    def __add_columns(self):
        self.__add_column("White", 0)
        self.__add_column("Black", 1)
        self.__add_column("Event", 3)
        self.__add_column("Date", 4)
        self.__add_column("Komi", 5)
        self.__add_column("Handicap", 6)
        self.__add_column("Result", 7)
    
    
    def __init__(self):
        gtk.TreeView.__init__(self)
        
        self.do_filter = False


        self.database = zambogo.sgf.database.get_default()
        self.model = librarymodel.LibraryModel()

        self.filter = self.model.filter_new()
        self.filter.set_visible_func(self.__filter_func)

        self.clear_filters()
        
        self.set_model(self.filter)
        
        
        self.__add_columns()
        self.columns_autosize()
        self.set_rules_hint(True)
        
        self.selection = self.get_selection()
        self.selection.set_mode(gtk.SELECTION_SINGLE)

    def get_selected_game(self):
        selection = self.get_selection()
        a = selection.get_selected_rows()
        path = a[1][0]
        
        it = self.filter.get_iter(path)
        id = self.filter.get(it,2)
        return id[0]
        

        
    
