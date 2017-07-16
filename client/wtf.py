# for checking abbrs that i have already known
# by tome.huang@samsung.com

import sys
import wtfserverrequester


class Wtf:
    import os

    WTF_IDENTITY = '201707162123'
    VERSION = '2.01'
    DATABASE_NAME = 'wtfdict'
    SERVER_URL = 'http://35.162.208.187:1235/'
    SYNC_URL = 'http://35.162.208.187/wtf/wtfdict'
    HOME_DIR = os.path.expanduser('~/.wtf')


    def __init__(self, serverurl=SERVER_URL):
        self._requester = wtfserverrequester.WtfServerRequester(serverurl=serverurl)
        self._dict = {}
        self.load()

    def getDict(self):
        return self._dict

    def getWtfDict(self):
        return self.getDict()

    def getVersion(self):
        return Wtf.VERSION

    def getDatabaseVersion(self):
        return ''

    def fetch(self, url=SYNC_URL, dirname=HOME_DIR, filename=DATABASE_NAME):
        import urllib, urllib.request, os, shutil, json

        newfilename = filename + '.new'
        oldpath = os.path.join(dirname, filename)
        newpath = os.path.join(dirname, newfilename)

        content = None

        if os.path.exists(dirname) is False:
            os.makedirs(dirname)

        content = self._requester.fetchAll()

        if content is None:
            return False

        if content['err'] != 0:
            return False

        try:
            wfp = open(newpath, 'w')
            if wfp is None:
                return False

            json.dump(content['data'], wfp)
            #wfp.write(str(content['data']))
            wfp.close()
        except:
            print(e)
            return False

        try:
            shutil.copyfile(oldpath, oldpath + '.old')
        except FileNotFoundError:
            pass

        try:
            shutil.move(newpath, oldpath)
        except:
            return False

        return self.load()


    def load(self, dirname=HOME_DIR, filename=DATABASE_NAME):
        import os, json

        path = os.path.join(dirname, filename)
        if os.path.exists(path) is False:
            return False

        fp = open(path)
        newdict = json.load(fp)
        fp.close()

        if newdict is None:
            return False

        self._dict = newdict
        
        return True

    def save(self, dirname=HOME_DIR, filename=DATABASE_NAME):
        import os, json

        if os.path.exists(dirname) is False:
            os.makedirs(dirname)

        path = os.path.join(dirname, filename)
        fp = open(path, 'w')
        json.dump(self._dict, fp)
        fp.close()


    def add(self, key, value, tag='', createdby=WTF_IDENTITY):
        if key is None or value is None:
            return False

        d = {}
        d['key'] = key
        d['value'] = value
        d['tag'] = tag
        d['createdby'] = createdby
        self.getWtfDict().append(d)
        self.save()

        try:
            self._requester.add(key, value, tag, createdby)
        except:
            print('something wrong occured when uploading it to server')

        return True

    def edit(self, key, value):
        if key is None or value is None:
            return False

        oldvalue = self.getWtfDict().get(key)
        if oldvalue is None:
            return False

        self.getWtfDict()[key] = value

        self.save()
        return True

    def remove(self, key):
        if key is None:
            return False

        d = self.getWtfDict()[:]
        for item in d:
            if item['key'] == key:
                self.getWtfDict().remove(item)

        self.save()

        try:
            self._requester.delete(key)
        except:
             print('something wrong occured when uploading it to server')

        return True


    def get(self, key):
        res = []
        if key is None:
            return None
        table = self.getWtfDict()

        for d in table:
            if d['key'].upper() == key.upper():
                res.append(d)

        return res

    def upload(self, url):
        pass






def usage(value=None, args=None):
    print('wtf - retrieve the abbrs')

    for d in PARAM_LIST:
        line = '-' + d[0]
        line = line + ', ' + '--' + d[2]
        line = line + '\t\t' + d[3]
        print(line)

def version(value=None, args=None):
    wtf = Wtf()

    content = 'exe version: ' + wtf.getVersion()
    content = content + '\n' + 'database version: ' + wtf.getDatabaseVersion()
    print(content)

def add(value, args):
    key = value
    arglen = len(args)
    if arglen <= 0:
        usage()
        return

    val = args[0]
    tag = ''
    createdby = Wtf.WTF_IDENTITY
    if arglen > 1:
        tag = args[1]
    if arglen > 2:
        createdby = args[2]

    wtf = Wtf()
    wtf.add(key, val, tag, createdby)

def delete(value, args):
    key = value

    wtf = Wtf()
    wtf.remove(key)

def edit(value, args):
    key = value
    if len(args) <= 0:
        usage()
        return
    val = args[0]

    wtf = Wtf()
    wtf.edit(key, val)

def get(value, args):
    key = None
    if value is not None:
        key = value
    else:
        key = args[0]

    wtf = Wtf()
    arr = wtf.get(key)

    if arr is None:
        print('nothing found for \'' + key + '\'')
    else:
        if len(arr) == 0:
            print('nothing found for \'' + key + '\'')
        else:
            print('[' + key + ']')
            for d in arr:
                value = d['value']
                tag = d['tag']
                createdby = d['createdby']
                item = value
                if tag != '':
                    item = item + '\ntag: ' + tag
                if createdby != '':
                    item = item + '\ncreated by:' + createdby

                item = item + '\n==== '
                print(item)

def fetch(value, args):
    wtf = Wtf()
    res = wtf.fetch()
    if res:
        print('fetch succeed')
    else:
        print('fetch failed')




'''
    [opt, contains_param, longopt, explain, entrance]
'''
PARAM_LIST = [
    ['h', False, 'help', 'display help information', usage],
    ['v', False, 'version', 'display version', version],
    ['a', True, 'add', 'add new record: wtf -a key value', add],
    ['d', True, 'delete', 'delete value by key: wtf -d key', delete],
    #['e', True, 'edit', 'edit and restore old record: wtf -e key value', edit],
    ['g', True, 'get', 'get record by key: wtf key or wtf -g key', get],
    ['f', False, 'fetch', 'fetch the latest wtf database(network required)', fetch],
]


def generateOptParams(paramList=PARAM_LIST):
    opts = ''
    longopts = []

    for d in paramList:
        opts = opts + d[0]
        l = d[2]

        if d[1] is True:
            opts = opts + ':'
            l = l + '='

        longopts.append(l)

    return opts, longopts

def getEntrance(opt, paramList=PARAM_LIST):
    if opt is None:
        return None, False

    for d in paramList:
        if opt == '-' + d[0] or opt == '--' + d[2]:
            withParam = d[1]
            return d[4], withParam

    return None, False

def appendFromFile(path, spliter=' '):
    '''
    append data from file into current wtf database
    '''

    fp = open(path, 'r')
    if fp is None:
        return

    wtf = Wtf()

    while True:
        line = fp.readline()
        if line is None or len(line) == 0:
            break;

        
        words = line.split(spliter)
        if len(words) <= 0:
            break;
        key = words[0]
        value = line[len(key) + 1:]
        print('line: ' + line)
        print('adding ' + key + ', value = ' + value)
        wtf.add(key, value)

    fp.close()


def convert(olddict):
    import json
    fp = open(olddict, 'r')
    d = json.load(fp)
    fp.close()

    database = d['database']

    wtf = Wtf()

    keys = database.keys()
    for key in keys:
        value = database[key]
        tag = 'spay'
        wtf.add(key, value, tag)
        print('added: ' + key)

def clearAllOnServer():
    wtf = Wtf()
    d = wtf.getWtfDict()
    keys = []
    for item in d:
        keys.append(item['key'])

    for key in keys:
        wtf.remove(key)
        print('removed: ' + key)


def main(argv):
    import getopt

    opts, longopts = generateOptParams()

    try:
        opts, args = getopt.getopt(argv, opts, longopts)
        if len(opts) == 0 and len(args) > 0:
            get(None, args)
            return
        elif len(opts) > 0:
            for opt, value in opts:
                entrance, withParam = getEntrance(opt)
                if entrance is None:
                    usage()
                    return

                entrance(value, args)
        else:
            usage()

    except getopt.GetoptError:
        usage()


if __name__ == '__main__':
    main(sys.argv[1:])
    #path = 'C:\\Users\\Administrator\\Desktop\\attrs.txt'
    #appendFromFile(path)
    #convert('E:/workspace/github/wtfdict')
    #clearAllOnServer()