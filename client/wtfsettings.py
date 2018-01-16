
SUPPORTED_SETTINGS = [
    # for user information
    {'key': 'user.name', 'value': '', 'description': 'user name will be added for each item'},
    {'key': 'user.email', 'value': '', 'description': 'till now i have no idea about how to use it'},

    # for server requests
    {'key': 'request.server.url', 'value': 'http://34.213.135.66:1235/', 'description': 'server entrance'},
    {'key': 'request.proxy', 'value': None, 'description': 'set the proxy first before sending any request'},
]


class WtfSettingItem:
    FIELD_KEY = 'key'
    FIELD_VALUE = 'value'
    FIELD_DESCRIPTION = 'description'

    def __init__(self, key=None, value=None, description=None):
        self._key = key
        self._value = value
        self._description = description

    def loadDict(self, d):
        if d is None:
            return

        self._key = d.get(WtfSettingItem.FIELD_KEY)
        self._value = d.get(WtfSettingItem.FIELD_VALUE)
        self._description = d.get(WtfSettingItem.FIELD_DESCRIPTION)

    def toDict(self):
        d = {}
        d[WtfSettingItem.FIELD_KEY] = self.getKey()
        d[WtfSettingItem.FIELD_VALUE] = self.getValue()
        d[WtfSettingItem.FIELD_DESCRIPTION] = self.getDescription()

        return d

    def setValue(self, value):
        self._value = value

    def getValue(self):
        return self._value

    def getKey(self):
        return self._key

    def getDescription(self):
        return self._description




class WtfSettings:

    def __init__(self, defaultsettings=SUPPORTED_SETTINGS):
        self._itemDict = {}

        if defaultsettings is not None:
            for itemDict in defaultsettings:
                item = WtfSettingItem()
                item.loadDict(itemDict)
                self.putItem(item)

    def _getItemDict(self):
        return self._itemDict

    def putItem(self, item):
        if item is None:
            return

        key = item.getKey()
        if key is None:
            return

        self._getItemDict()[key] = item

    def getItem(self, key):
        if key is None:
            return None

        return self._getItemDict().get(key)

    def set(self, key, value):
        if key is None:
            return False

        item = self._getItemDict().get(key)
        if item is None:
            return False

        item.setValue(value)
        return True

    def get(self, key):
        item = self.getItem(key)
        if item is None:
            return None

        return item.getValue()

    def _loadArray(self, a, append=False):
        if a is None:
            return -1

        if not append:
            self._getItemDict().clear()

        for itemDict in a:
            item = WtfSettingItem()
            item.loadDict(itemDict)
            self.putItem(item)

        return len(a)

    def load(self, path):
        import os, json

        if os.path.exists(path) is False:
            return -1

        fp = open(path)
        jarray = json.load(fp)
        fp.close()

        if jarray is None:
            return 0

        return self._loadArray(jarray)

    def _toArray(self):
        a = []

        items = self._getItemDict().items()
        for k, i in items:
            d = i.toDict()
            a.append(d)

        return a

    def save(self, path):
        import os, json

        a = self._toArray()

        fp = open(path, 'w')
        json.dump(a, fp)
        fp.close()

    def getSettingsItemList(self):
        return self._getItemDict().values()

    def getSettingsArray(self):
        a = []
        itemList = self.getSettingsItemList()
        if itemList is None:
            return a

        for item in itemList:
            a.append(item.toDict())

        return a



if __name__ == '__main__':
    settings = WtfSettings()

    #print(settings.getSettingsArray())
    #print(settings.set('user.name', 'tome.huang'))
    #print(settings.get('user.name'))
    #settings.save('settings.test.txt')

    settings.load('settings.test.txt')
    print(settings.getSettingsArray())
    print(settings.get('user.name'))
