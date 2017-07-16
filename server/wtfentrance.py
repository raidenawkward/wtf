# -*- coding: utf-8 -*-

import wtf
import wtf.server
import wtf.server.wtfserver
import wtf.server.database

import flask
from flask import Flask, request


app = Flask(__name__)

@app.route('/')
def queryall():
    server = wtf.server.wtfserver.WtfServer()
    res = server.queryAll()
    return str(res)

@app.route('/add')
def add():
    key = request.args.get('key', '', type=str)
    if key is '':
        return 'must have a key'

    value = request.args.get('value', '', type=str)
    tag = request.args.get('tag', '', type=str)
    createdby = request.args.get('createdby', '', type=str)

    server = wtf.server.wtfserver.WtfServer()
    res = server.add(key, value, tag, createdby)
    return str(res)

@app.route('/delete')
def delete():
    key = request.args.get('key', '', type=str)
    if key is '':
        return 'must have a key'

    server = wtf.server.wtfserver.WtfServer()
    res = server.delete(key)
    return str(res)

