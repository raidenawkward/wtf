# for checking abbrs that i have already known
# by tome.huang@samsung.com

import sys
import wtfserverrequester
from wtfsource import WtfRecord, WtfSource
from hashsource import HashSource

class Wtf:
    import os

    WTF_IDENTITY = '201707162123'
    VERSION = '2.12'

    DATABASE_NAME = 'wtfdict'
    SETTINGS_NAME = 'wtfsettings'
    SERVER_URL = 'http://34.213.135.66:1235/'
    SYNC_URL = 'http://35.162.208.187/wtf/wtfdict'
    HOME_DIR = os.path.expanduser('~/.wtf')
    SOURCE_DIR = os.path.join(HOME_DIR, 'hashsource')

    KEY_SETTINGS_PROXY = 'settings.proxy'
    KEY_SETTINGS_SERVER_URL = 'settings.server.url'
    KEY_SETTINGS_USER_NAME = 'settings.user.name'
    KEY_SETTINGS_USER_EMAIL = 'settings.user.email'


    def __init__(self, serverurl=None):
        self._dict = {}
        self._settings = {}
        self._source = None

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

    def getSource(self):
        return self._source

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


    '''
    def loadDict(self, dirname=HOME_DIR, filename=DATABASE_NAME):
        # change
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
    '''

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
        self.loadSettings(dirname=dirname)
        self._source = HashSource(homedir=Wtf.SOURCE_DIR)

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
        #self._saveDict(dirname)
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

    def exportSource(self, path):
        return self.getSource().exportSource(path)

    def importSource(self, path, appendix=True):
        return self.getSource().importSource(path=path, allowMerge=appendix)

    def add(self, key, dictionary):
        if key is None:
            return False

        if dictionary.get(WtfRecord.FIELD_USER) is None:
            user = self.getUser()

        d = dictionary.copy()
        d[WtfRecord.FIELD_KEY] = key
        d[WtfRecord.FIELD_USER] = user

        return self.getSource().add(dictionary=d, restrict=False)
        '''
        try:
            self._requester.add(key, value, tag, user)
            pass
        except:
            print('something wrong occured when uploading it to server')
        '''

    def edit(self, key, id, dictionary):
        d = dictionary.copy()
        d[WtfRecord.FIELD_USER] = self.getUser()
        return self.getSource().edit(key, id, dictionary=dictionary)

    def remove(self, key, id=None):
        return self.getSource().remove(key, id)

    def retrieve(self, key):
        res = []
        if key is None:
            return res

        res = self.getSource().retrieveByKey(key)
        res1 = self.getSource().retrieveByKey(key.upper())

        c = res.copy()
        for r in res1:
            found = False
            for r0 in c:
                if r.getId() == r0.getId():
                    found = True
                    break
            if not found:
                res.append(r)

        return res

    def upload(self, url):
        pass

    def setServerUrl(self, serverurl):
        if self._requester is None:
            return

        self._requester.setServerUrl(serverurl)
        self.getSettings()[Wtf.KEY_SETTINGS_SERVER_URL] = serverurl

        self._saveSettings()

    def setSetting(self, key, value):
        if value is None:
            try:
                del self.getSettings()[key]
            except KeyError:
                pass
        else:
            self.getSettings()[key] = value

        self._saveSettings()

    def deleteSetting(self, key):
        try:
            del self.getSettings()[key]
        except KeyError:
            return False

        self._saveSettings()
        return True

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