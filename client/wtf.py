# for checking abbrs that i have already known
# by tome.huang@samsung.com

import sys
import wtfserverrequester


class Wtf:
    import os

    WTF_IDENTITY = '201707162123'
    VERSION = '2.02'
    DATABASE_NAME = 'wtfdict'
    SETTINGS_NAME = 'wtfsettings'
    SERVER_URL = 'http://34.213.135.66:1235/'
    SYNC_URL = 'http://35.162.208.187/wtf/wtfdict'
    HOME_DIR = os.path.expanduser('~/.wtf')

    KEY_SETTINGS_PROXY = 'settings.proxy'
    KEY_SETTINGS_SERVER_URL = 'settings.server.url'
    KEY_SETTINGS_USER_NAME = 'settings.user.name'
    KEY_SETTINGS_USER_EMAIL = 'settings.user.email'


    def __init__(self, serverurl=None):
        self._dict = {}
        self._settings = {}

        self.load()

        serverurl = self.getServerUrl()
        if serverurl is None:
            serverurl = Wtf.SERVER_URL

        self._requester = wtfserverrequester.WtfServerRequester(serverurl=serverurl)
        self._requester.setProxy(self.getProxy())

        self.save()

    def getDict(self):
        return self._dict

    def getWtfDict(self):
        return self.getDict()

    def getVersion(self):
        return Wtf.VERSION

    def getDatabaseVersion(self):
        return ''

    def getSettings(self):
        return self._settings

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


    def loadDict(self, dirname=HOME_DIR, filename=DATABASE_NAME):
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


    def loadSettings(self, dirname=HOME_DIR, filename=SETTINGS_NAME):
        import os, json

        path = os.path.join(dirname, filename)
        if os.path.exists(path) is False:
            return False

        fp = open(path)
        newdict = json.load(fp)
        fp.close()

        if newdict is None:
            return False

        self._settings = newdict

        return True

    def load(self, dirname=HOME_DIR):
        resSettings = self.loadSettings(dirname=dirname)
        resDict = self.loadDict(dirname=dirname)
        return resDict

    def _saveDict(self, dirname=HOME_DIR, filename=DATABASE_NAME):
        '''
        save current Wtf dict into home dir
        '''
        import os, json

        if os.path.exists(dirname) is False:
            os.makedirs(dirname)

        path = os.path.join(dirname, filename)
        fp = open(path, 'w')
        json.dump(self._dict, fp)
        fp.close()

    def _saveSettings(self, dirname=HOME_DIR, filename=SETTINGS_NAME):
        import os, json

        if os.path.exists(dirname) is False:
            os.makedirs(dirname)

        path = os.path.join(dirname, filename)
        fp = open(path, 'w')
        json.dump(self._settings, fp)
        fp.close()

    def save(self, dirname=HOME_DIR):
        self._saveDict(dirname)
        self._saveSettings(dirname)

    def exportDict(self, targetPath):
        import os, json

        if targetPath is None:
            return False

        res = True

        try:
            path = os.path.join(targetPath)
            fp = open(path, 'w')
            json.dump(self.getWtfDict(), fp)
            fp.close()
        except:
            res = False

        return res

    def importDict(self, path, appendix=True):
        import os, json

        if os.path.exists(path) is False:
            return False

        fp = open(path)
        newdict = json.load(fp)
        fp.close()

        if newdict is None:
            return False

        if appendix is False:
            self._dict = newdict
        else:
            self.getWtfDict().extend(newdict)

        self._saveDict()

        return True



    def add(self, key, value, tag='', createdby=None):
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
        self._saveDict()

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

        self._saveDict()
        return True

    def remove(self, key):
        if key is None:
            return False

        d = self.getWtfDict()[:]
        for item in d:
            if item['key'] == key:
                self.getWtfDict().remove(item)

        self._saveDict()

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

    def setServerUrl(self, serverurl):
        if self._requester is None:
            return

        self._requester.setServerUrl(serverurl)
        self.getSettings()[Wtf.KEY_SETTINGS_SERVER_URL] = serverurl

        self._saveSettings()

    def setSettings(self, key, value):
        if value is None:
            try:
                del self.getSettings()[key]
            except KeyError:
                pass
        else:
            self.getSettings()[key] = value

        self._saveSettings()

    def getServerUrl(self):
        return self.getSettings().get(Wtf.KEY_SETTINGS_SERVER_URL)

    def setProxy(self, proxy):
        if self._requester is None:
            return

        self._requester.setProxy(proxy)
        self.getSettings()[Wtf.KEY_SETTINGS_PROXY] = proxy

        self._saveSettings()

    def getProxy(self):
        return self.getSettings().get(Wtf.KEY_SETTINGS_PROXY)

    def setUser(self, user):
        self.getSettings()[Wtf.KEY_SETTINGS_USER_NAME] = user
        self._saveSettings()

    def getUser(self):
        return self.getSettings().get(Wtf.KEY_SETTINGS_USER_NAME)


if __name__ == '__main__':
    pass