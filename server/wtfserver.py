# -*- coding: utf-8 -*-

import wtf
import wtf.server
import wtf.server.database
from wtf.server.database import *

class WtfServer:

    def __init__(self, rootdir='.', dbfile='./wtf.db'):
        self._rootdir = rootdir
        self._db = WtfDatabase(dbfile=dbfile)

    def requestInitDb(self):
        self._db.initdb()

    def queryAll(self):
        sql = 'select * from valuesofkey;'
        res = self._db.query(sql)
        return res

    def query(self, key):
        if self.isKeyExist(key) is False:
            return

        sql = 'select * from valuesofkey where key = \'%s\';' % key
        res = self._db.query(sql)
        return res

    def isKeyExist(self, key):
        sql = 'select * from keys where key = \'%s\';' % key
        res = self._db.query(sql)
        return len(res) > 0

    def add(self, key, value, tag='', createdby=''):
        if self.isKeyExist(key) is False:
            sql = 'insert into keys (key) values (\'%s\')' % key
            self._db.execute(sql)

        sql = 'insert into valuesofkey (key, value, tag, createdby) values (\'%s\', \'%s\', \'%s\', \'%s\');' % (key, value, tag, createdby)
        self._db.execute(sql)

    def delete(self, key):
        if key is None:
            return
        sql = 'delete from valuesofkey where key = \'%s\';' % key
        self._db.execute(sql)
        sql = 'delete from keys where key = \'%s\';' % key
        res = self._db.execute(sql)

        return res





if __name__ == '__main__':
    server = WtfServer()
    #server.requestInitDb()
    res = server.add('key1', 'value1', 'test', 'tome')
    print(res)
    res = server.query('key1')
    res = server.delete('key1')
    print(res)

