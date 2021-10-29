import sqlite3
import threading

class SQLite3:
    def db_open(self,dbname):
        tid = threading.get_ident()
        if tid in self.db[dbname]:
            try:
                cur = self.db[dbname][tid].cursor()
                cur.close()
                return self.db[dbname][tid] # OK!
            except:
                del self.db[dbname][tid]
        self.db[dbname][tid] = sqlite3.connect(self.data.data_dir + "/dynamic/" + dbname + ".sqlite3")
        cur = self.db[dbname][tid].cursor()
        cur.execute("PRAGMA journal_mode = WAL")
        cur.execute("PRAGMA synchronous = NORMAL")
        cur.execute("PRAGMA busy_timeout = 3000")
        self.db[dbname][tid].commit()
        return self.db[dbname][tid]
    def db_close(self,dbname):
        tid = threading.get_ident()
        if tid in self.db[dbname]:
            try:
                cur = self.db[dbname][tid].cursor()
                cur.close()
                self.db[dbname][tid].close()
            except:
                pass
            del self.db[dbname][tid]


    def __init__(self,data):
        self.data = data
        self.sql = data.sql
        self.db = {}
        for dbname in self.sql['index'].keys():
            if dbname == "":
                continue
            self.db[dbname] = {}
        self.init_db()

    def try_int(self,s):
        try:
            return int(s)
        except ValueError:
            return None

    def _sql_execute_idx(self,dbname,conn,idx):
        if not idx in self.sql['index'][dbname]:
            return
        cur = conn.cursor()
        for sqlfile in self.sql['index'][dbname][idx]:
            if self.sql[sqlfile] == "":
                conn.rollback()
                conn.close()
                raise Exception("sql is empty db:"+dbname + " idx:"+str(idx))
            cur.execute(self.sql[sqlfile])
        cur.close()
        conn.commit()

    def init_db(self):
        for dbname in self.sql['index'].keys():
            if dbname == "":
                continue
            conn = self.db_open(dbname)
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='meta';")
            rows = cur.fetchall()
            cur.close()
            if len(rows) != 1:
                self._sql_execute_idx(dbname,conn,0)
                cur = conn.cursor()
                cur.execute("insert into meta(meta_key,meta_val) values('version','0');")
                cur.close()
                conn.commit()
            cur = conn.cursor()
            cur.execute("select meta_val from meta where meta_key = 'version';")
            rows = cur.fetchall()
            cur.close()
            if len(rows) != 1:
                self.db_close(dbname)
                raise Exception('meta.version not set on db:' + dbname)
            ver = self.try_int(rows[0][0])
            if ver is None:
                self.db_close(dbname)
                raise Exception('meta.version is broken on db:' + dbname)
            if ver < self.sql['index'][dbname]['']['max_index']:
                ver_val = ver
                while ver_val < self.sql['index'][dbname]['']['max_index']:
                    ver_val += 1
                    self._sql_execute_idx(dbname,conn,ver_val)
                cur = conn.cursor()
                cur.execute("update meta set meta_val = ? where meta_key = 'version';",(str(ver_val),))
                cur.close()
            conn.commit()
            self.db_close(dbname)

    def sql_execute(self,dbname,sql,sqlparam):
        conn = self.db_open(dbname)
        cur = conn.cursor()
        if sqlparam is None:
            cur.execute(sql)
        else:
            cur.execute(sql,sqlparam)
        rows = cur.fetchall()
        cur.close()
        return rows

    def sql_commit(self,dbname):
        self.db_open(dbname).commit()

    def sql_rollback(self,dbname):
        self.db_open(dbname).rollback()




            


       

