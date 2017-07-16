import urllib, urllib.request, os, shutil, json


class WtfServerRequester:
    SERVER_URL = 'http://35.162.208.187:1235/'
    API_FETCHALL = ''
    API_RETRIEVE = 'retrieve'
    API_ADD = 'add'
    API_DELETE = 'delete'

    def __init__(self, serverurl=SERVER_URL):
        self._serverurl = serverurl

    def sendRequest(self, url):
        try:
            rfp = urllib.request.urlopen(url)
            if rfp is None:
                return None
            content = rfp.read()
            rfp.close()
        except:
            return None

        content = json.loads(content.decode())

        return content

    def fetchAll(self):
        url = self._serverurl + WtfServerRequester.API_FETCHALL
        return self.sendRequest(url)

    def add(self, key, value, tag=None, createdby=None):
        url = self._serverurl + WtfServerRequester.API_ADD
        if key is None:
            return None

        url = url + '?key=' + key

        if value is not None:
            url = url + '&value=' + value

        if tag is not None:
            url = url + '&tag=' + tag

        if createdby is not None:
            url = url + '&createdby=' + createdby

        return self.sendRequest(url)

    def delete(self, key):
        url = self._serverurl + WtfServerRequester.API_DELETE
        if key is None:
            return None
        url = url + '?key=' + key
        return self.sendRequest(url)

    def retrieve(self, key):
        url = self._serverurl + WtfServerRequester.API_RETRIEVE
        if key is None:
            return None
        url = url + '?key=' + key
        return self.sendRequest(url)


if __name__ == '__main__':
    requester = WtfServerRequester()
    #res = requester.add('clientkey', 'clientvalue', 'clienttag')
    #res = requester.delete('clientkey')
    res = requester.retrieve('key1')
    print(res)
    all = requester.fetchAll()
    print(all)