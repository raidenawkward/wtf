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
        return len(res)

    def query(self, sql):
        print('querying: ' + sql)

        db = self.opendb()
        cur = db.execute(sql)
        res = WtfDatabase.cursorToArray(cur)
        db.commit()
        self.closedb()
        return res

    def cursorToArray(cursor):
        records = cursor.fetchall()
        field = [i[0] for i in cursor.description]
        records2 = [dict(zip(field,i)) for i in records]
        return records2




if __name__ == '__main__':
    db = WtfDatabase(dbfile='./testdb.db')
    #db.initdb()
    #res = db.execute('select * from keys;')
    #res = db.execute('insert into keys (key) values(\'wtf\') ;')
    #res = db.execute('delete from keys where id = 1 ;')
    print(res)
