import wtf
from wtf import Wtf
from wtfsource import WtfRecord

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def batch_import(path, sep='%%', tagsoverride=None):
    wtf = Wtf()

    f = open(path, 'r')
    lines = f.readlines()
    for line in lines:
        d = {}
        key = None

        params = line.split(sep)
        if len(params) > 0:
            key = params[0]
        if len(params) > 1:
            d[WtfRecord.FIELD_VALUE] = params[1]
        if len(params) > 2:
            d[WtfRecord.FIELD_DETAIL] = params[2]
        if len(params) > 3:
            d[WtfRecord.FIELD_TAGS] = params[3]

        if tagsoverride is not None:
            d[WtfRecord.FIELD_TAGS] = tagsoverride

        if key is not None:
            print('adding ' + str(key) + ', ' + str(d))
            wtf.add(key, d)

    f.close()


def display_help():
    print("import formatted file into wtf dict")
    print("usage:")
    print("    baftch_import.py targetfile tags")
    print("file lines should be formatted as:")
    print("    {key}$LIST_FILE_LINE_IFS{value}$LIST_FILE_LINE_IFS{description}$LIST_FILE_LINE_IFS{tags}")

if __name__ == '__main__':
    import sys

    path = None
    tagsoverride = None

    if len(sys.argv) > 1:
        path = sys.argv[1]
    if len(sys.argv) > 2:
        tagsoverride = sys.argv[2]
    batch_import(path, tagsoverride=tagsoverride)