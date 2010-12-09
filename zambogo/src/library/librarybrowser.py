import pygtk
import gtk
import librarytreeview
import playertreeview
import eventtreeview

class LibraryBrowser(gtk.Alignment):
    
    def __event_selection_changed(self, view):

        events = self.event_view.get_selected_events()
        
        self.library_view.clear_event_filters()
        
        if events is None:
            return
        
        for event in events:
            self.library_view.filter_event(event[0])
    
    def __player_selection_changed(self, view):
        players = self.player_view.get_selected_players()
        
        self.library_view.clear_player_filters()
        self.event_view.clear_filters()
        
        if players is None:
            return
        
        for player in players:
            self.event_view.filter_player(player[0])
            self.library_view.filter_player(player[0])
    
    def __sw(self, wid):
        sw = gtk.ScrolledWindow()
        sw.add(wid)
        return sw
    
    def __make_event_view(self):
        self.event_view = eventtreeview.EventTreeView()
        self.event_view.get_selection().connect("changed", self.__event_selection_changed)
        return self.__sw(self.event_view)
    
    def __make_library_view(self):
        self.library_view = librarytreeview.LibraryTreeView()
        return self.__sw(self.library_view)

    def __make_player_view(self):
        self.player_view = playertreeview.PlayerTreeView()
        
        self.player_view.get_selection().connect("changed", self.__player_selection_changed)
        return self.__sw(self.player_view)
    
    def __pack_widgets(self):
        vbox = gtk.VBox()
        hbox = gtk.HBox()
        
        lv = self.__make_library_view()
        pv = self.__make_player_view()
        ev = self.__make_event_view()
        
        hbox.pack_start(pv,True)
        hbox.pack_start(ev,True)
        
        vbox.pack_start(hbox,True)
        vbox.pack_start(lv,True)
        
        self.add(vbox)

    def __init__(self):
        gtk.Alignment.__init__(self)
        self.__pack_widgets()
        self.set(0,0,1,1)
        
    def get_selected_game (self):
        return self.library_view.get_selected_game()
