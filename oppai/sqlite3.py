import sqlite3

class SQLite3:
    def __init__(self,data):
        self.data = data
        self.sql = data.sql
        self.db = {}
        for dbname in self.sql['index'].keys():
            if dbname == "":
                continue
            self.db[dbname] = sqlite3.connect(self.data.data_dir + "/dynamic/" + dbname + ".sqlite3")
            cur = self.db[dbname].cursor()
            cur.execute("PRAGMA journal_mode = WAL")
            cur.execute("PRAGMA synchronous = NORMAL")
            cur.execute("PRAGMA busy_timeout = 3000")
            self.db[dbname].commit()
        self.init_db()

    def try_int(self,s):
        try:
            return int(s)
        except ValueError:
            return None

    def __sql_execute_idx(self,dbname,idx):
        if not idx in self.sql['index'][dbname]:
            return
        cur = self.db[dbname].cursor()
        for sqlfile in self.sql['index'][dbname][idx]:
            if self.sql[sqlfile] == "":
                self.db[dbname].rollback()
                raise Exception("sql is empty db:"+dbname + " idx:"+str(idx))
            cur.execute(self.sql[sqlfile])
        cur.close()
        self.db[dbname].commit()

    def init_db(self):
        for dbname in self.sql['index'].keys():
            if dbname == "":
                continue
            cur = self.db[dbname].cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='meta';")
            rows = cur.fetchall()
            cur.close()
            if len(rows) != 1:
                self.__sql_execute_idx(dbname,0)
                cur = self.db[dbname].cursor()
                cur.execute("insert into meta(meta_key,meta_val) values('version','0');")
                cur.close()
                self.db[dbname].commit()
            cur = self.db[dbname].cursor()
            cur.execute("select meta_val from meta where meta_key = 'version';")
            rows = cur.fetchall()
            cur.close()
            if len(rows) != 1:
                raise Exception('meta.version not set on db:' + dbname)
            ver = self.try_int(rows[0][0])
            if ver is None:
                raise Exception('meta.version is broken on db:' + dbname)
            if ver < self.sql['index'][dbname]['']['max_index']:
                ver_val = ver
                while ver_val < self.sql['index'][dbname]['']['max_index']:
                    ver_val += 1
                    self.__sql_execute_idx(dbname,ver_val)
                cur = self.db[dbname].cursor()
                cur.execute("update meta set meta_val = ? where meta_key = 'version';",(str(ver_val),))
                cur.close()
            self.db[dbname].commit()

    def sql_execute(self,dbname,sql,sqlparam):
        cur = self.db[dbname].cursor()
        cur.execute(sql,sqlparam)
        rows = cur.fetchall()
        cur.close()
        return rows

    def sql_commit(self,dbname):
        self.db[dbname].commit()

    def sql_rollback(self,dbname):
        self.db[dbname].rollback()




            


       

