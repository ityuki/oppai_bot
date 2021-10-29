from random import choice
import oppai.cmd as Cmd

import re
import time

class Bot:
    def __init__(self,data):
        self.data = data
        self.cmd = Cmd.Cmd(data)
    
    def incomming_message(self,channel,user,message):
        res = None

        # oppai count検索
        if re.match(r'^oppai\s+[a-z]+.*$',message) is None:
            count = len(re.split(r'お.*?っ.*?ぱ.*?い',message)) - 1
            self.cmd.add_oppai(channel,count)

        # log save
        rows = self.data.db.sql_execute("log","select max(id) from log",None)
        id = 0
        if not rows is None and not rows[0] is None and not rows[0][0] is None:
            id = int(rows[0][0]) + 1
        self.data.db.sql_execute("log","insert into log(id,channnel,userid,msg,create_at) values(?,?,?,?,?)",(id,channel,user,message,int(time.time())))
        self.data.db.sql_commit("log")

        # 出力メッセージ構築
        if not re.match(r'^oppai\s+[a-z]+.*$',message) is None:
            # oppai command
            cmds = re.split(r'\s+',message,maxsplit=3)
            if len(cmds) >= 2 and cmds[0] == 'oppai':
                if len(cmds) == 3 and cmds[2] == "":
                    cmds.pop()
                cmd = cmds[1]
                if cmd == "control":
                    pass
                else:
                    if self.cmd.has_cmd(cmd):
                        res = self.cmd.run_cmd(channel,cmd)
                    else:
                        res = "しらないおっぱいです"

        return res

