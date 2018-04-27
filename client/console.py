import sys
import wtf
from wtf import Wtf
from wtfsource import WtfRecord


def usage(value=None, args=None):
    print('wtf - personal abbr management')

    for d in PARAM_LIST:
        line = ''
        if d[0] is not None and d[0] != '!':
            line = line + '-' + d[0] + ', '
        line = line + '--' + d[2]
        line = line + '\t\t\t\t' + d[3]
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

    d = {}

    val = args[0]
    tags = ''
    detail = ''

    if arglen > 1:
        tags = args[1]

    if arglen > 2:
        detail = args[2]

    d[WtfRecord.FIELD_VALUE] = val
    d[WtfRecord.FIELD_DETAIL] = detail
    d[WtfRecord.FIELD_TAGS] = tags

    wtf = Wtf()
    wtf.add(key, d)

def delete(value, args):
    key = value
    id = None
    if len(args) > 0:
        id = args[0]

    wtf = Wtf()
    (res, err) = wtf.remove(key, id)
    if not res:
        print(err)

def edit(value, args):
    key = value
    if len(args) <= 1:
        usage()
        return

    d = {}
    d[WtfRecord.FIELD_ID] = args[0]
    d[WtfRecord.FIELD_VALUE] = args[1]

    if len(args) > 2:
        d[WtfRecord.FIELD_TAGS] = args[2]

    if len(args) > 3:
        d[WtfRecord.FIELD_DETAIL] = args[3]

    wtf = Wtf()
    (res, err) = wtf.edit(key, d[WtfRecord.FIELD_ID], d)
    if not res:
        print(err)

def retrieve(value, args):
    key = None
    if value is not None:
        key = value
    else:
        key = args[0]

    wtf = Wtf()
    arr = wtf.retrieve(key)

    if arr is None:
        print('nothing found for \'' + key + '\'')
    else:
        if len(arr) == 0:
            print('nothing found for \'' + key + '\'')
        else:
            print('result for [' + key + ']')
            for r in arr:
                key = r.getKey()
                value = r.get(WtfRecord.FIELD_VALUE)
                detail = r.get(WtfRecord.FIELD_DETAIL)
                tags = r.get(WtfRecord.FIELD_TAGS)
                user = r.get(WtfRecord.FIELD_USER)
                id = r.get(WtfRecord.FIELD_ID)
                stamp = r.get(WtfRecord.FIELD_TIMESTAMP)

                item = '[' + key + ']'
                item = item + '\n' + value
                if detail != '' and detail is not None:
                    item = item + '\n-----\n' + detail
                item = item + '\nid: ' + id
                if tags != '' and tags is not None:
                    item = item + '\ntags: ' + tags
                if user != '' and user is not None:
                    item = item + '\nuser: ' + user

                timestr = None
                try:
                    import time
                    timestr = time.ctime(int(stamp))
                except:
                    timestr = None

                if timestr is not None:
                    item = item + '\nstamp: ' + timestr

                item = item + '\n====='
                print(item)

def list_all(value, args):
    wtf = Wtf()
    records = wtf.getSource().getAllRecords()

    for r in records:
        print(r.toString())

    print('total: ' + str(len(records)))

def fetch(value, args):
    wtf = Wtf()
    res = wtf.fetch()
    if res:
        print('fetch succeed')
    else:
        print('fetch failed')

def set_proxy(value, args):
    key = None
    if value is not None:
        key = value
    else:
        key = args[0]

    wtf = Wtf()

    wtf.setProxy(key)

    print('save the proxy as \'' + str(key) + '\'')

def set_serverurl(value, args):
    key = None
    if value is not None:
        key = value
    else:
        key = args[0]

    wtf = Wtf()

    wtf.setServerUrl(key)

    print('save the serverurl as \'' + str(key) + '\'')

def set_configure(value, args):
    key = value
    arglen = len(args)
    val = None

    if arglen > 0:
        val = args[0]

    wtf = Wtf()

    if val is not None:
        wtf.setSetting(key, val)
    else:
        print('' + wtf.getSettings().get(key))

def delete_configure(value, args):
    key = value
    arglen = len(args)
    val = None

    if arglen > 0:
        val = args[0]

    wtf = Wtf()

    if key is not None:
        res = wtf.deleteSetting(key)
        if res:
            print('delete setting ' + key + ' succeed.')
        else:
            print('delete setting ' + key + ' failed.')

def display_configure(value, args):
    wtf = Wtf()
    settings = wtf.getSettings()
    if settings is not None:
        keys = settings.keys()
        for key in keys:
            print('' + str(key) + ' : ' + str(settings.get(key)))

def set_user(value, args):
    wtf = Wtf()
    wtf.setUser(value)

def show_user(value, args):
    wtf = Wtf()
    print('' + wtf.getUser())

def output_dict(value, args):
    target = value
    if target is None:
        usage()
        return

    wtf = Wtf()
    res = wtf.getSource().exportSource(target)

    if res:
        print('export succeed to ' + target)
    else:
        print('export failed to ' + target)

def input_dict(value, args):
    if value is None:
        usage()
        return

    path = value
    wtf = Wtf()
    original_count = wtf.getSource().getRecordCount()
    res = wtf.importSource(path, appendix=True)

    if res:
        new_count = wtf.getSource().getRecordCount()
        print('import succeed! ' + str(new_count - original_count) + ' item increased (' + str(new_count) + ') totally now.')
    else:
        print('import failed')

def input_dict_no_appendix(value, args):
    if value is None:
        usage()
        return

    path = value
    wtf = Wtf()
    original_count = wtf.getSource().getRecordCount()
    res = wtf.importSource(path, appendix=False)

    if res:
        new_count = wtf.getSource().getRecordCount()
        print('import succeed! ' + str(new_count - original_count) + ' item increased (' + str(new_count) + ') totally now.')
    else:
        print('import failed')

def display_total_count(value, args):
    wtf = Wtf()
    print('' + str(len(wtf.getWtfDict())))



'''
    [opt, contains_param, longopt, explain, entrance]
'''
PARAM_LIST = [
    ['v', False, 'version', 'display version', version],
    ['a', True, 'add', 'add new record: wtf -a key value [tag1,tag2,..] [detail]', add],
    ['d', True, 'delete', 'delete value by key: wtf -d key [id]', delete],
    ['e', True, 'edit', 'edit and restore old record: wtf -e key value [tag1,tag2,..] [detail] [id]', edit],
    ['r', True, 'retrieve', 'retrieve records by key: wtf key or wtf -r key', retrieve],
    ['L', False, 'list-all', 'list all restored items', list_all],
    ['f', False, 'fetch', 'fetch the latest wtf database(network required)', fetch],
    ['P', True, 'proxy', 'set and restore the proxy', set_proxy],
    ['S', True, 'serverurl', 'set and restore the server url', set_serverurl],
    ['u', True, 'set-user', 'set user\'s name', set_user],
    ['U', False, 'show-user', 'show user\'s name', show_user],
    ['o', True, 'output-dict', 'output dict into file', output_dict],
    ['i', True, 'import-dict', 'import dict for current wtf database, appendix = True', input_dict],
    ['I', True, 'import-dict-no-appendix', 'import dict for current wtf database, appendix = False', input_dict_no_appendix],
    ['h', False, 'help', 'display help information', usage],
    ['!', False, 'config-list', 'list all current configurations', display_configure],
    ['!', False, 'count-total', 'display the total count', display_total_count],
    ['!', True, 'config-delete', 'delete configure key and its value', delete_configure],
    ['c', True, 'configure', 'set the configure key pairs (key = value). if only given \'key\', value will be displayed', set_configure],
]


def generateOptParams(paramList=PARAM_LIST):
    opts = ''
    longopts = []

    for d in paramList:
        if d[0] is not None:
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
        hit = False

        if d[0] is None:
            if opt == '--' + d[2]:
                hit = True
        else:
            if opt == '-' + d[0] or opt == '--' + d[2]:
                hit = True

        if hit:
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
            retrieve(None, args)
            return
        elif len(opts) > 0:
            for opt, value in opts:
                entrance, withParam = getEntrance(opt)
                if entrance is None:
                    print('no entrance was found: ' + str(opt))
                    usage()
                    return

                entrance(value, args)
        else:
            usage()

    except getopt.GetoptError:
        usage()




def update_created_by(user):
    wtf = Wtf()
    arr = wtf.getWtfDict()
    for d in arr:
        d['createdby'] = user
    print('' + str(len(arr)) + ' items modified.')
    wtf.save()

def upload():
    wtf = Wtf()
    arr = wtf.getWtfDict()

    total = len(arr)
    index = 1
    for d in arr:
        key = d['key']
        value = d['value']
        tag = d['tag']
        createdby = d['createdby']

        res = wtf._requester.add(key, value, tag, createdby)

        print('(' + str(index) + '/' + str(total) + ') key: ' + str(key) + ', res: ' + str(res))

        index = index + 1


if __name__ == '__main__':
    main(sys.argv[1:])
    #update_created_by('tome')
    #upload()
    #path = 'C:\\Users\\Administrator\\Desktop\\attrs.txt'
    #appendFromFile(path)
    #convert('E:/workspace/github/wtfdict')
    #clearAllOnServer()