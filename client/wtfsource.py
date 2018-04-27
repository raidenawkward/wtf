# base for data storage

class WtfRecord:
    FIELD_KEY = 'key'
    FIELD_ID = 'id'
    FIELD_VALUE = 'value'
    FIELD_DETAIL = 'detail'
    FIELD_USER = 'user'
    FIELD_TAGS = 'tags'
    FIELD_TIMESTAMP = 'timestamp'

    def __init__(self, path=None):
        self._dict = {}
        self._path = path

        if path is not None:
            self.loadFromFile(path)
        else:
            self.set(WtfRecord.FIELD_ID, self._generateId())

    def _generateId(self):
        stamp = self.getTimeStamp()
        import hashlib
        hash = hashlib.sha256(str(stamp).encode())
        return hash.hexdigest()

    def getTimeStamp(self):
        import time
        lt = time.localtime()
        t = time.mktime(lt)
        stamp = int(t)
        return stamp

    def updateTimeStamp(self):
        self.getDict()[WtfRecord.FIELD_TIMESTAMP] = self.getTimeStamp()

    def loadFromJsonBytes(self, jb):
        if jb is None:
            return False

        try:
            import json
            newdict = json.loads(jb)

            if newdict is None:
                self._dict = {}
            else:            
                self._dict = newdict
        except:
            return False

        return True

    def loadFromFile(self, path):
        import os, json
        self._path = path

        if not os.path.exists(path):
            return False

        try:
            fp = open(path)
            newdict = json.load(fp)
            fp.close()

            if newdict is None:
                self._dict = {}
            else:
                self._dict = newdict
        except:
            return False

        return True

    def saveToFile(self, path):
        self.updateTimeStamp()

        if path is None:
            return False

        self._path = path

        import os, json
        try:
            fp = open(path, 'w')
            json.dump(self._dict, fp)
            fp.close()
        except:
            return False

        return True

    def sync(self):
        return self.saveToFile(self.getPath())

    def getPath(self):
        return self._path

    def getDict(self):
        return self._dict

    def getKey(self):
        return self.getDict().get(WtfRecord.FIELD_KEY)

    def setKey(self, key):
        self.getDict()[WtfRecord.FIELD_KEY] = key

    def getId(self):
        return self.get(WtfRecord.FIELD_ID)

    def set(self, key, value):
        self.getDict()[key] = value

    def get(self, key):
        return self.getDict().get(key)

    def toString(self):
        content = '[' + str(type(self)) + '] ' + str(self) + '\n'
        keys = self.getDict().keys()
        keys = sorted(keys)
        for k in keys:
            content = content + '    ' + k + ' = ' + str(self.get(k)) + '\n'

        content = content + '\n'
        return str(content)

    def hash(self):
        return None


class WtfSource:
    '''
    this is base class for holding data
    '''

    def loadSource(self, path):
        pass

    def importSource(self, path, allowMerge=True):
        pass

    def exportSource(self, path):
        pass

    def syncSource(self):
        pass

    def add(self, wtfrecord, restrict=False):
        pass

    def retrieveByKey(self, key):
        return None

    def fetch(self, url):
        pass

    def merge(self, dst, allowDuplicate=True):
        pass

    def toString(self):
        return ''




if __name__ == '__main__':
    #r = WtfRecord()
    #r.setKey('testkey')
    #r.getDict()['value'] = 'vvv'
    #r.saveToFile('test.json')
    #r = WtfRecord(path='test.json')
    #print(r.getDict()['key'])
    #print(r.getDict()['value'])
    pass