#!/usr/bin/env python

import sqlite3, json, time
from housepy import config, log

connection = sqlite3.connect("data.db")
connection.row_factory = sqlite3.Row
db = connection.cursor()

def init():
    try:
        db.execute("CREATE TABLE data (id INTEGER PRIMARY KEY, kind TEXT, t INTEGER, v REAL, r REAL)")
        db.execute("CREATE INDEX data_kind ON data(kind)")
    except Exception as e:
        if hasattr(e, 'message'):
            e = e.message
        if "already exists" not in str(e):
            raise e
    connection.commit()
init()

def insert_data(kind, v, cumulative=False):
    try:
        r = None
        db.execute("SELECT v, t, r FROM data WHERE kind=? ORDER BY id DESC LIMIT 1", (kind,))
        previous = db.fetchone()
        if previous is not None:
            if cumulative and previous['r'] is not None:
                r = v
                v -= previous['r']
            if v == previous['v']:
                log.debug("%s unchanged" % kind)
                return
        elif cumulative:
            r = v
        db.execute("INSERT INTO data (kind, t, v, r) VALUES (?, ?, ?, ?)", (kind, int(time.time()), v, r))
        log.debug("%s -> %s" % (kind, v))
    except Exception as e:
        log.error(log.exc(e))
        return
    connection.commit()

