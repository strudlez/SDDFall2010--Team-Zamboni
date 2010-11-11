import gio
import glib


USERNAME="racarr"
PASSWORD="zaq12wsx"

class IGSClient:
    def write(self,string):
        self.output.write(string)

    def read_pending(self):
        read = ""
        while self.socket.condition_check(glib.IO_IN):
            read += self.input.read(1)
        return read
    
    def automatch(self, opponent):
        if not self.logged_in:
            return False
        self.output.write("automatch " + opponent + "\n")
        return True
    
    def login(self):
        if not self.connected:
            return False
        self.output.write(USERNAME+"\n"+PASSWORD+"\n")
        self.logged_in = True

        return True

    def connect(self):
        self.connection = self.client.connect_to_host("igs.joyjoy.net:7777",
                                                      7777, None)
        self.input = self.connection.get_input_stream()
        self.output = self.connection.get_output_stream()
        
        self.socket = self.connection.get_socket()
        
        self.connected = True
        
        return True
        
    def disconnect(self):
        self.connection.close()
    
    def __init__(self):
        self.connected = False
        self.logged_in = False

        self.client = gio.SocketClient()
