import inspect
import re
import random

class Cmd:
    def __init__(self,data):
        self.data = data

    def get_method(self,name):
        try:
            f = getattr(self,name)
            if not inspect.ismethod(f):
                return None
            return f
        except AttributeError:
            return None

    def has_cmd(self,cmd):
        if not cmd in self.data.dict_keys(self.data.dict['help']):
            return False
        return True
    
    def run_cmd(self,channel,cmd):
        f = self.get_method(cmd)
        if f is None:
            return cmd + "はまだ知らないコマンドですね"
        return f(channel)
    
    def add_oppai(self,channel,count):
        if not 'sum' in self.data.dynamic_dict:
            self.data.dynamic_dict['sum'] = {}
        if not channel in self.data.dynamic_dict['sum']:
            self.data.dynamic_dict['sum'][channel] = "0"
        self.data.dynamic_dict['sum'][channel] = str(int(self.data.dynamic_dict['sum'][channel]) + count)
        self.data.dynamic_dict_writer("sum")

        if not 'count' in self.data.dynamic_dict:
            self.data.dynamic_dict['count'] = {}
        if not channel in self.data.dynamic_dict['count']:
            self.data.dynamic_dict['count'][channel] = ""
        d = re.split(r'\s+',self.data.dynamic_dict['count'][channel])
        if len(d) > 30:
            d.pop(0)
        d.append(str(count))
        self.data.dynamic_dict['count'][channel] = " ".join(d)
        self.data.dynamic_dict_writer("count")
    
    # 以下、実行関数

    # おっぱい数を返す
    def count(self,channel):
        if not channel in self.data.dynamic_dict['sum']:
            self.data.dynamic_dict['sum'] = "0"
        return "現在 " + self.data.dynamic_dict['sum'][channel] + "おっぱいです"

    # おっぱい宣教師語録+α
    def word(self,channel):
        scnt = len(self.data.list['word'])
        dcnt = int(self.data.db.sql_execute("word","select count(*) from word where is_deleted = 0",None)[0][0])
        r = random.randint(0,scnt+dcnt-1)
        if r < scnt:
            self.data.db.sql_commit("word")
            return self.data.list['word'][r]
        r -= scnt
        msg = self.data.db.sql_execute("word","select msg from word where is_deleted = 0 order by id limit ?,1",(r,))[0][0]
        self.data.db.sql_commit("word")
        return msg
    
    # おっぱいフラグ
    def flag(self,channel):
        scnt = len(self.data.list['flag'])
        dcnt = int(self.data.db.sql_execute("flag","select count(*) from flag where is_deleted = 0",None)[0][0])
        r = random.randint(0,scnt+dcnt-1)
        if r < scnt:
            self.data.db.sql_commit("flag")
            return self.data.list['flag'][r]
        r -= scnt
        msg = self.data.db.sql_execute("flag","select msg from flag where is_deleted = 0 order by id limit ?,1",(r,))[0][0]
        self.data.db.sql_commit("flag")
        return msg
    
    # helloおっぱい
    def hello(self,channel):
        return random.choice(self.data.list['hello'])
    
    def random(self,channel):
        cmd = random.choice(self.data.dict_keys(self.data.dict['help']))
        if cmd == "random":
            return "あぶないぱい。自分で `oppai random` しそうになったぱい"
        if cmd == "control":
            return "自分で `oppai control` することはできないぱい。あぶないぱい"
        return self.run_cmd(channel,cmd)

    def per(self,channel):
        if not channel in self.data.dynamic_dict['count']:
            return "おっぱわーが足りません"
        if self.data.dynamic_dict['count'][channel] is None:
            return "おっぱわーが足りません"
        d = re.split(r'\s+',self.data.dynamic_dict['count'][channel])
        if len(d) < 1:
            return "おっぱわーが足りません"
        opper = sum([int(x) for x in d])
        if opper == 0:
            return "おっぱわーが足りません"
        per = int(100 * opper / len(d))
        return "現在のおっぱい濃度は " + str(per) + " %です"
    
    def ping(self,channel):
        return 'oppai pong!'
    
    def help(self,channel):
        max_length_command = max([len(x) for x in self.data.dict_keys(self.data.dict['help'])])
        help_text = '```\n'
        help_text += "Usage: oppai <subcommand>\n"
        for cmd in self.data.dict_keys(self.data.dict['help']):
            help_text += ("\toppai {:<" + str(max_length_command) + "}: {:}\n").format(cmd,self.data.dict['help'][cmd])
        help_text += '```\n'
        return help_text
    
    def version(self,channel):
        return "oppai_bot version 0.0.20211029"
        






