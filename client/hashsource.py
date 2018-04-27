from wtfsource import WtfSource, WtfRecord

class HashHelper:
    def hashString(self, str):
        import hashlib
        if str is None:
            return None

        hash = hashlib.sha1(str.encode())
        return hash.hexdigest()



class HashRecord(WtfRecord):

    IGNORED_HASH_FEILDS = [
        WtfRecord.FIELD_TIMESTAMP,
        WtfRecord.FIELD_ID,
        ]

    def __init__(self, path=None, dictionary=None):
        WtfRecord.__init__(self, path, dictionary=dictionary)

    def _shouldIgnoredWhenHash(self, key):
        return HashRecord.IGNORED_HASH_FEILDS.count(key) > 0

    def hash(self):
        helper = HashHelper()
        key = self.getKey()
        if key is None:
            return None

        source = ''

        keys = self.getDict().keys()
        keys = sorted(keys)

        for k in keys:
            if not self._shouldIgnoredWhenHash(k):
                source = source + str(self.get(k))

        return helper.hashString(source)


class HashSource(WtfSource):
    import os

    HOME_DIR = os.path.expanduser('~/.wtf/wtfdict/')

    def __init__(self, homedir=HOME_DIR):
        self._homeDir = homedir
        self._hashHelper = HashHelper()

        self._prepare()

    def _prepare(self):
        import os, json
        if self._homeDir is None:
            return

        if os.path.exists(self._homeDir) is False:
            os.makedirs(self._homeDir)

    def _getHashHelper(self):
        return self._hashHelper

    def getHomeDir(self):
        return self._homeDir

    def _getTempDir(self):
        import os
        return os.path.join(self.getHomeDir(), 'temp')

    def _genKeyPath(self, key):
        import os

        hashstr = self._getHashHelper().hashString(key)
        recorddir = os.path.join(self.getHomeDir(), hashstr)

        return recorddir

    def loadSource(self, path):
        self._homeDir = path

    def importSource(self, path, allowMerge=True):
        '''
        DANGER: please be ware of allowMerge, it removes all existing records
        '''

        import zipfile
        import os
        total = 0
        succeed = 0
        failed = 0

        if not os.path.isfile(path):
            return False

        if not zipfile.is_zipfile(path):
            return False

        if not allowMerge:
            # DANGER: delete current records
            import shutil
            shutil.rmtree(self.getHomeDir())
            os.makedirs(self.getHomeDir())

        try:
            zf = zipfile.ZipFile(path)
            nameList = zf.namelist()
            total = len(nameList)

            for filename in zf.namelist():
                filename = filename.replace('\\', '/')

                if filename.endswith('/'):
                    continue

                zcontent = zf.read(filename)
                record = HashRecord()
                try:
                    record.loadFromJsonBytes(zcontent)
                except:
                    failed = failed + 1

                if self.add(record):
                    succeed = succeed + 1
        except:
            return False

        # print('' + str(succeed) + ', ' + str(failed) + ' ' + str(total))
        return True

    def exportSource(self, path):
        import zipfile
        import os
        fileList = []
        homeDir = self.getHomeDir()
        if not os.path.isdir(homeDir):
            return False

        fileList.append(homeDir)

        try:
            for root, dirs, files in os.walk(homeDir):
                for f in files:
                    fullpath = os.path.join(root, f)
                    fileList.append(fullpath)

            zf = zipfile.ZipFile(path, "w", zipfile.zlib.DEFLATED)
            for f in fileList:
                zf.write(f)
            zf.close()
        except:
            return False

        return True

    def syncSource(self):
        pass

    def add(self, wtfrecord=None, restrict=False, dictionary=None):
        if dictionary is not None:
            wtfrecord = HashRecord(dictionary=dictionary)

        if wtfrecord is None:
            return False

        key = wtfrecord.getKey()
        if key is None:
            return False

        dirpath = self._genKeyPath(key)
        filename = wtfrecord.hash()

        import os
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        path = os.path.join(dirpath, filename)

        return wtfrecord.saveToFile(path)

    def remove(self, key, id=None):
        if key is None:
            return False, 'key is None'

        import os

        dirpath = self._genKeyPath(key)
        if not os.path.isdir(dirpath):
            return False, 'no record exists'

        for root, dirs, files in os.walk(dirpath):
            if len(files) > 1:
                if id is None:
                    err = 'more than one record for key \'' + key + '\', specify one id of them:'
                    for f in files:
                        record = HashRecord(path=os.path.join(root, f))
                        err = err + '\n' + record.toString()
                    return False, err

            for f in files:
                record = HashRecord(path=os.path.join(root, f))
                if id is not None:
                    if record.getId() == id:
                        os.remove(record.getPath())
                        return True, ''
                else:
                    os.remove(record.getPath())
                    return True, ''

        return False, 'no record was found'

    def edit(self, key, id, wtfrecord=None, dictionary=None):
        import os

        if id is None or key is None:
            return False, 'need key and id for editing'

        # print('edit: ' + key + ', ' + id + ', ' + str(dictionary))
        d = dictionary.copy()

        wtfrecord = HashRecord(dictionary=d)
        wtfrecord.setKey(key)

        dirpath = self._genKeyPath(key)
        if not os.path.isdir(dirpath):
            return False, 'no record exists'

        for root, dirs, files in os.walk(dirpath):
            for f in files:
                r = HashRecord(os.path.join(root, f))
                if r.getId() == wtfrecord.getId():
                    r.load(wtfrecord)
                    r.sync()
                    return True, None

        return False, 'nothing updated'

    def retrieveByKey(self, key):
        l = []

        dirpath = self._genKeyPath(key)

        import os
        if not os.path.exists(dirpath):
            return l

        for root, dirs, files in os.walk(dirpath):
            for f in files:
                record = HashRecord(path=os.path.join(root, f))
                l.append(record)

        return l

    def fetch(self, url):
        pass

    def merge(self, dst, allowDuplicate=True):
        pass

    def toString(self):
        return str(self)

    def getRecordCount(self):
        count = 0
        import os

        for root, dirs, files in os.walk(self.getHomeDir()):
            for f in files:
                count = count + 1

        return count

    def getAllRecords(self):
        l = []

        import os

        for root, dirs, files in os.walk(self.getHomeDir()):
            for f in files:
                record = HashRecord(path=os.path.join(root, f))
                l.append(record)
        return l





def importFromDict(dictpath):
    import os, json

    hs = HashSource(homedir='./newhomedir')

    if os.path.exists(dictpath) is False:
        return

    fp = open(dictpath)
    jarray = json.load(fp)
    fp.close()

    count = 0;
    for d in jarray:
        record = HashRecord()

        record.setKey(d.get('key'))
        record.set(WtfRecord.FIELD_TAGS, d.get('tag'))
        record.set(WtfRecord.FIELD_VALUE, d.get('value'))
        record.set(WtfRecord.FIELD_USER, d.get('createdby'))

        hs.add(record)
        count = count + 1


if __name__ == '__main__':
    '''
    r = HashRecord()
    r.setKey('key1')
    r.set('name', 'tome')
    r.set('age', '18')

    r1 = HashRecord()
    r1.setKey('key2')
    r1.set('name', 'tome')
    r1.set('age', '19')

    r2 = HashRecord()
    r2.setKey('key2')
    r2.set('name', 'tome')
    r2.set('age', '17')

    #hs = HashSource(homedir='./testhomedir')
    #hs.add(r)
    #hs.add(r1)
    #hs.add(r2)

    #hs.exportSource('./testexport.zip')
    #hs.importSource('./testexport.zip')

    #res = hs.retrieveByKey('key2')
    #for record in res:
        #print(record.get('age'))
    '''
    #importFromDict('C:\\Users\\Administrator\\.wtf\\wtfdict')
    hs = HashSource(homedir='./newhomedir')
    # hs.exportSource('./olddict.wtfdict')
    res = hs.retrieveByKey('BCTC')
    for record in res:
        print(record.toString())