import pygtk
import gtk
import playermodel
import zambogo.sgf.database

class PlayerTreeView(gtk.TreeView):
    
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
        self.__add_column("Name", 0)
    
    def __init__(self):
        gtk.TreeView.__init__(self)

        self.__guard = False
        self.database = zambogo.sgf.database.get_default()
        self.model = playermodel.PlayerModel()
        
        self.set_model(self.model)
        
        self.__add_columns()
        
        self.selection = self.get_selection()
        self.selection.set_mode(gtk.SELECTION_MULTIPLE)
        
        self.selection.set_select_function(self.__selected_function)
    
    def get_selected_players(self):
        players = []
        selection = self.get_selection()
        a = selection.get_selected_rows()
        paths = a[1]
        for path in paths:
            if (path[0] == 0): return None
            it = self.model.get_iter(path)
            players.append(self.model.get(it,0))
        return players
        
    
