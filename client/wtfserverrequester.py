import urllib, json
from urllib import parse,request


class WtfServerRequester:
    SERVER_URL = 'http://35.162.208.187:1235/'
    API_FETCHALL = ''
    API_RETRIEVE = 'retrieve'
    API_ADD = 'add'
    API_DELETE = 'delete'

    def __init__(self, serverurl=SERVER_URL):
        self._serverurl = serverurl

    def sendRequest(self, url, getdict=None):
        if getdict is not None:
            gets = parse.urlencode(getdict)
            url = url + '?' + gets

        #print(url)
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

        getdict = {}
        getdict['key'] = key
        getdict['value'] = value
        getdict['tag'] = tag
        getdict['createdby'] = createdby

        return self.sendRequest(url, getdict)

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