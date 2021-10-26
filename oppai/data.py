import glob
import os
import re

from oppai.sqlite3 import SQLite3

class Data:
    def file_read(self,fname):
        try:
            with open(fname,encoding="utf-8") as f:
                return f.read().split("\n")
        except OSError:
            return []
    
    def file_list(self,dir):
        try:
            d = []
            for fn in glob.glob(dir + "/*.opp"):
                if os.path.isfile(fn):
                    d.append(os.path.splitext(os.path.basename(fn))[0])
            return d
        except OSError:
            return []

    def try_int(self,s):
        try:
            return int(s)
        except ValueError:
            return None

    def list_loader(self,fname):
        d = []
        for l in self.file_read(fname + ".opp"):
            if l == "":
                continue
            d.append(l)
        return d

    def dict_loader(self,fname):
        d = {}
        d[''] = {}
        d['']['index'] = []
        for l in self.file_read(fname + ".opp"):
            if l == "":
                continue
            sp = re.split(r'\s+',l,maxsplit=2)
            if len(sp) != 2:
                continue
            if sp[0] == "" or sp[1] == "":
                continue
            d[sp[0]] = sp[1]
            d['']['index'].append(sp[0])
        return d
    
    def index_loader(self,fname):
        d = {}
        d[''] = {}
        d['']['index'] = []
        d['']['vals'] = {}
        for l in self.file_read(fname + ".opp"):
            if l == "":
                continue
            sp = re.split(r'\s+',l,maxsplit=3)
            if len(sp) != 3:
                continue
            if sp[0] == "" or sp[1] == "" or sp[2] == "":
                continue
            key = sp[0]
            idx = self.try_int(sp[1])
            val = sp[2]
            if idx is None:
                continue
            if not key in d:
                d[key] = {}
                d[key][''] = {}
                d[key]['']['index'] = []
                d[key]['']['max_index'] = -1
            if not idx in d[key]:
                d[key][idx] = []
            ary_size = len(d[key][idx])
            if not val in d['']['vals']:
                d['']['vals'][val] = []
            d['']['vals'][val].append( len(d['']['index']) )
            d['']['index'].append( (key,idx,ary_size) )
            d[key]['']['index'].append( (idx,ary_size) )
            d[key][idx].append( val )
            if d[key]['']['max_index'] < idx:
                d[key]['']['max_index'] = idx
        return d

    def __init__(self,data_dir,private_dir):
        self.data_dir = data_dir
        self.private_dir = private_dir
        self.dict = {}
        self.list = {}
        self.sql = {}
        self.conf = {}
        target_dir = data_dir + "/static/dict"
        for fname in self.file_list(target_dir):
            self.dict[fname] = self.dict_loader(target_dir + "/" + fname)
        target_dir = data_dir + "/static/list"
        for fname in self.file_list(target_dir):
            self.list[fname] = self.list_loader(target_dir + "/" + fname)
        target_dir = data_dir + "/static/sql"
        self.sql['index'] = self.index_loader(target_dir + "/index")
        for fname in self.sql['index']['']['vals'].keys():
            self.sql[fname] = "\n".join(self.file_read(target_dir + "/" + fname))
        target_dir = private_dir + "/conf"
        for fname in self.file_list(target_dir):
            self.conf[fname] = self.dict_loader(target_dir + "/" + fname)
        
        self.db = SQLite3(self)
        


