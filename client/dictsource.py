from wtfsource import WtfSource

class DictSource (WtfSource):
    '''
    this class holds ABBRs as a dict
    '''

    HOME_DIR = os.path.expanduser('~/.wtf')
    DATABASE_PATH = 'wtfdict'

    def __init__(self, homedir=HOME_DIR, path=DATABASE_PATH):
        self._homeDir = homedir
        self._path = path
        self._dict = {}

    def importSource(self, srcdir=HOME_DIR, srcpath=DATABASE_PATH):
        import os, json

        self._path = distpath
        self._homeDir = dstdir

        path = None
        if srcdir is None:
            path = srcpath
        else:
            path = os.path.join(srcdir, srcpath)

        if os.path.exists(path) is False:
            return False

        fp = open(path)
        newdict = json.load(fp)
        fp.close()

        if newdict is None:
            return False

        self._dict = newdict

        return True

    def exportSource(self, dstdir=HOME_DIR, dstpath=DATABASE_PATH):
        '''
        save current Wtf dict into home dir
        '''
        import os, json

        self._path = distpath
        self._homeDir = dstdir

        path = None

        if dstdir is not None:
            if os.path.exists(dstdir) is False:
                os.makedirs(dstdir)
            path = os.path.join(dstdir, dstpath)
        else:
            path = distpath

        fp = open(path, 'w')
        json.dump(self._dict, fp)
        fp.close()

        return True

    def syncSource(self):
        return self.exportSource(self._homeDir, self._path)

    def fetch(self, url):
        pass

    def merge(self, dst, allowDup=True):
        self._mergeDictItem(dst)

    def _mergeDictItem(self, newdict):
        '''
        1. not exist, add it
        2. existed, and totally same with one of the existed item, skip it
        3. existed, but do not same with any of existed item, add it as a new record
        '''
        # print('_mergeDictItem')

        for d in newdict:
            key = d.get('key')
            value = d.get('value')
            tag = d.get('tag')
            createdby = d.get('createdby')

            if key is None:
                continue

            existedList = self.get(key)
            if existedList is None:
                # print('_mergeDictItem existList is None ' + key)
                self.add(key=key, value=value, tag=tag, createdby=createdby)
            else:
                # print('_mergeDictItem existList is not None ' + key)
                hit = False
                for dd in existedList:
                    ddvalue = dd.get('value')
                    ddtag = dd.get('tag')
                    ddcreatedby = dd.get('createdby')

                    if ddvalue == value and ddtag == tag and ddcreatedby == createdby:
                        hit = True
                        break
                    elif ddvalue == value and ddtag == tag:
                        hit = True
                        break
                    else:
                        continue

                if not hit:
                    #print('_mergeDictItem not hit: ' + key + ', ' + value)
                    self.add(key=key, value=value, tag=tag, createdby=createdby)

    def add(self, key, value):
        if key is None or value is None:
            return False

        if createdby is None:
            createdby = self.getSettings().get(Wtf.KEY_SETTINGS_USER_NAME)

        d = {}
        d['key'] = key
        d['value'] = value
        d['tag'] = tag
        d['createdby'] = createdby
        self.getWtfDict().append(d)
        self.syncSource()

        return True

    def retrieve(self, key):
        res = []
        if key is None:
            return None
        table = self.getWtfDict()

        for d in table:
            if d['key'].upper() == key.upper():
                res.append(d)

        return res

    def toString(self):
        return ''