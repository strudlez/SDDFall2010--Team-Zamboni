import sqlite3
import sgflib
import string
import os
import os.path
import zambogo.util

database = None

def get_default():
    global database
    if database is None:
        database = SGFDatabase()
    return database



class SGFInfo:
    def __init__(self, data=None):
        self.__resetProperties()
        
        if data != None:
            self.__parseData(data)

        
    def load_file(self, path):
        f = open(path, 'r')
        data = f.read()
        
        self.props["filename"] = path

        self._game = sgflib.SGFParser(data).parseOneGame()
        self.__parseProperties()
        
    def __parseData(self,data):
        props = ["WR","BR","GN","DT","HA","SZ","EV","PW","PC","KM","filename","PB","RE","TM"]
        self.id = data[0]

        data = data[1:]
        for i in range(0,14):
            self.props[props[i]] = data[i]

    def __parseProperties(self):
        root = self._game[0]
        for p in root:
            if self.props.has_key(p.id):
                self.props[p.id] = string.join(map(string.strip, p), "::")

    def __resetProperties(self):
        self.props = {'DT' : '',# DaTe
                      'RE' : '',# REsult
                      'PB' : '',# Black Player's name
                      'BR' : '',# Black Rank
                      'PW' : '',# White Player's name
                      'WR' : '',# White Rank
                      'KM' : '',# KoMi
                      'HA' : '',# HAndicap
                      'SZ' : '',# board SiZe
                      'TM' : '',# TiMe limit
                      'filename' : None,
                      'GN' : '',# Game Name
                      'PC' : '',# PlaCe where game held
                      'EV' : '',}# EVent name

class SGFQuery:
    
    def __init__(self):
        self.fields = {}
        
    def player_black(self, player):
        self.fields["pb"] = player
        
    def player_white(self, player):
        self.fields["pw"] = player
        
    def build_query(self):
        query = "select * from games where "
        f = ""
        
        for k in self.fields.keys():
            f += "%s = '%s' and" % (k,self.fields[k])
        f = f[:-4]
        
        return query+f


class SGFDatabase:
    
    def __create_database(self):
        database_path = os.path.join(zambogo.util.get_sgf_dir(),"sgfbase")
        conn = sqlite3.connect(database_path)
        c = conn.cursor()
        c.execute('''create table games (id integer primary key, wr text, br text, gn text, dt text, ha text, sz text, ev text, pw test, pc text, km text, filename text, pb text, re text, tm text)''')
        conn.commit()
        return conn


    def __open_database(self):
        database_path = os.path.join(zambogo.util.get_sgf_dir(),"sgfbase")
        if (os.path.isfile(database_path)):
            conn = sqlite3.connect(database_path)
            return conn
        else:
            return self.__create_database()
        
    def __load_database(self):
        c = self.conn.cursor()
        c.execute("select * from games")
        for row in c:
            self.infos[row[0]] = SGFInfo(row)

    def __init__(self):
        self.conn = self.__open_database()
        self.infos = {}
        
        self.__load_database()
        
    def __run_insert_query(self, info):
        props = ["WR","BR","GN","DT","HA","SZ","EV","PW","PC","KM","filename","PB","RE","TM"]
        plist = "("
        values = []
        for prop in props:
            values.append(info.props[prop].decode("utf8"))
            plist = plist + prop.lower() + ","
        plist = plist.rstrip(",")
        plist = plist + ")"
        query = "insert into games %s values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)" % (plist,)
        c = self.conn.cursor()
        c.execute(query,values)
        self.infos[c.lastrowid] = info
        info.id = c.lastrowid

        self.conn.commit()

    def __check_for_game(self, info):
        c = self.conn.cursor()
        c.execute ("select * from games where filename = ?", (info.props["filename"],))
        if c.fetchall() != []:
            return True
        return False
        
        
    def __add_to_database(self, info):
        
        if self.__check_for_game(info):
            return

        self.__run_insert_query(info)

    def list_sgfs(self):
        c = self.conn.cursor()
        c.execute("select * from games")
        
    def add_sgf(self, path):
        info = SGFInfo()
        info.load_file(path)
        self.__add_to_database(info)
    
    def add_folder(self, folder):
        it = os.walk(folder)
        for root,dirs,files in it:
            for f in files:
                if f[-4:] == ".sgf":
                    self.add_sgf(os.path.join(root,f))
                    
    def run_search_query(self, query):
        c = self.conn.cursor()
        c.execute(query.build_query())
        return c.fetchall()
    
    def list_players(self):
        c = self.conn.cursor()
        c.execute("select distinct pw from games union select distinct pb from games")
        players = []
        for row in c:
            players.append(row[0])
        return players
    def list_events(self):
        c = self.conn.cursor()
        c.execute("select distinct ev from games")
        events = []
        for row in c:
            if row[0] is not None:
                events.append(row[0])
        return events
    
    def get_games_with_player(self, player):
        games = []
        c = self.conn.cursor()
        c.execute("select id from games where pw=? or pb=?", (player,player))
        for row in c:
            games.append(row[0])
        return games
    
    def get_games_with_event(self, event):
        games = []
        c = self.conn.cursor()
        c.execute("select id from games where ev=?",(event,))
        for row in c:
            games.append(row[0])
        return games
    
    def get_events_with_players(self, players):
        events = set()
        for player in players:
            query = "select distinct ev from games where pb=? or pw=?"
            c = self.conn.cursor()
            c.execute(query,(player,player))
            for row in c:
                events.add(row[0])
        return events

                    



