# -*- coding: utf-8 -*-

import wtf
import wtf.server
import wtf.server.wtfserver
import wtf.server.database

import flask
from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('/')
def queryall():
    server = wtf.server.wtfserver.WtfServer()
    res = server.queryAll()
    err = 0
    if res is None:
        err = -1
    return jsonify(err=err, count=len(res), data=res)

@app.route('/retrieve')
def query():
    key = request.args.get('key', '', type=str)
    if key is '':
        return 'must have a key'

    server = wtf.server.wtfserver.WtfServer()
    res = server.query(key)
    err = 0
    if res is None:
        err = -1
    return jsonify(err=err, data=res)

@app.route('/add')
def add():
    key = request.args.get('key', '', type=str)
    if key is '':
        return 'must have a key'

    value = request.args.get('value', '', type=str)
    tag = request.args.get('tag', '', type=str)
    createdby = request.args.get('createdby', '', type=str)

    server = wtf.server.wtfserver.WtfServer()
    server.add(key, value, tag, createdby)
    return jsonify(err=0)

@app.route('/delete')
def delete():
    key = request.args.get('key', '', type=str)
    if key is '':
        return 'must have a key'

    server = wtf.server.wtfserver.WtfServer()
    server.delete(key)
    return jsonify(err=0)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1235)
