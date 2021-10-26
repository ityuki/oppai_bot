import glob
import os
import re

class Data:
    def file_read(self,fname):
        try:
            with open(fname + ".opp",encoding="utf-8") as f:
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


    def list_loader(self,fname):
        d = []
        for l in self.file_read(fname):
            if l == "":
                continue
            d.append(l)
        return d

    def dict_loader(self,fname):
        d = {}
        for l in self.file_read(fname):
            if l == "":
                continue
            sp = re.split(r'\s+',l,maxsplit=2)
            if len(sp) != 2:
                continue
            d[sp[0]] = sp[1]
        return d

    def __init__(self,data_dir,private_dir):
        self.data_dir = data_dir
        self.data_dir = private_dir
        self.dict = {}
        self.list = {}
        self.conf = {}
        target_dir = data_dir + "/static/dict"
        for fname in self.file_list(target_dir):
            self.dict[fname] = self.dict_loader(target_dir + "/" + fname)
        target_dir = data_dir + "/static/list"
        for fname in self.file_list(target_dir):
            self.list[fname] = self.list_loader(target_dir + "/" + fname)
        target_dir = private_dir + "/conf"
        for fname in self.file_list(target_dir):
            self.conf[fname] = self.dict_loader(target_dir + "/" + fname)


