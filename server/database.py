# -*- coding: utf-8 -*-

import sqlite3

class WtfDatabase:

    def __init__(self, dbfile='wtf.db'):
        self._dbfile = dbfile
        self._db = None


    def initdb(self, schemafile='schema.sql'):
        db = self.opendb()
        with open(schemafile, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        self.closedb()

    def opendb(self):
        self._db = sqlite3.connect(self._dbfile)
        return self._db

    def closedb(self):
        if self._db is not None:
            self._db.close()

    def execute(self, sql):
        print('executing: ' + sql)

        db = self.opendb()
        cur = db.execute(sql)
        res = cur.fetchall()
        db.commit()
        self.closedb()
        return res

    def query(self, sql):
        print('querying: ' + sql)

        db = self.opendb()
        cur = db.execute(sql)
        res = cur.fetchall()
        db.commit()
        self.closedb()
        return res






if __name__ == '__main__':
    db = WtfDatabase(dbfile='./testdb.db')
    #db.initdb()
    #res = db.execute('select * from keys;')
    #res = db.execute('insert into keys (key) values(\'wtf\') ;')
    #res = db.execute('delete from keys where id = 1 ;')
    print(res)
