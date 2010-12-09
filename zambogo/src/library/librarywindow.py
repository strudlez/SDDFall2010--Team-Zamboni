import gtk
import pygtk
import librarybrowser
import zambogo.sgf.database
import zambogo.review.reviewwindow

class LibraryWindow(gtk.Window):
    
    def __play_clicked(self, pb):
        db = zambogo.sgf.database.get_default()
        game = self.browser.get_selected_game()
        rw = zambogo.review.reviewwindow.ReviewWindow()
        print "game: " + str(db.infos[game])
        rw.load_sgf(db.infos[game].props["filename"])
        print game
        
    def __open_response(self, dialog, response):
        if response == gtk.RESPONSE_ACCEPT:
            folder = dialog.get_filename()
            print folder + " folder"
            d = zambogo.sgf.database.get_default()
            d.add_folder(folder)
            
        dialog.destroy()
        
    def __open_clicked(self, pb):
        d = gtk.FileChooserDialog("Import files", self, gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_ACCEPT))
        d.run()
        d.show_all()
        
        d.connect("response", self.__open_response)
    
    def __setup_toolbar(self):
        pb = gtk.ToolButton(gtk.STOCK_MEDIA_PLAY)
        pb.connect("clicked", self.__play_clicked)
        
        ib = gtk.ToolButton(gtk.STOCK_OPEN)
        ib.connect("clicked", self.__open_clicked)
        
        self.toolbar.insert(ib,0)
        self.toolbar.insert(pb,1)
    
    def __make_browser(self):
        self.browser = librarybrowser.LibraryBrowser()
        
    def __make_toolbar(self):
        self.toolbar = gtk.Toolbar()
        self.__setup_toolbar()
    
    def __setup_ui(self):
        self.vbox = gtk.VBox()
        
        self.__make_browser()
        self.__make_toolbar()
        
        self.vbox.pack_start(self.toolbar, False, False)
        self.vbox.pack_start(self.browser)

        self.add(self.vbox)
    
    def __init__(self):
        gtk.Window.__init__(self)
        
        self.connect("delete-event", gtk.Widget.hide_on_delete)
        
        self.__setup_ui()

        self.set_default_size(800,700)
        
