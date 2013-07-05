#!/usr/bin/env python

import sqlite3, json, time
from housepy import config, log

connection = sqlite3.connect("data.db")
connection.row_factory = sqlite3.Row
db = connection.cursor()

def init():
    try:
        db.execute("CREATE TABLE IF NOT EXISTS data (kind TEXT, t INTEGER, v REAL, r REAL)")
        db.execute("CREATE INDEX IF NOT EXISTS data_kind ON data(kind)")
        db.execute("CREATE UNIQUE INDEX IF NOT EXISTS data_kind_t ON data(kind, t)")
        #
        db.execute("CREATE TABLE IF NOT EXISTS venues (venue_id TEXT, people INTEGER)")
        db.execute("CREATE UNIQUE INDEX IF NOT EXISTS venues_venue_id ON venues(venue_id)")
    except Exception as e:
        log.error(log.exc(e))
        return
    connection.commit()
init()

def insert_data(kind, v, t=None, cumulative=False):
    try:
        r = None
        db.execute("SELECT v, t, r FROM data WHERE kind=? ORDER BY t DESC LIMIT 1", (kind,))
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
        if t is None:
            t = int(time.time())
        db.execute("INSERT INTO data (kind, t, v, r) VALUES (?, ?, ?, ?)", (kind, t, v, r))
        entry_id = db.lastrowid            
        log.info("%s -> %s (%s)" % (kind, v, entry_id))
    except Exception as e:
        log.error(log.exc(e))
        return
    connection.commit()
    return entry_id


####

def add_venue(venue):
    log.info("adding venue %s" % venue['venue_id'])
    try:
        db.execute("INSERT INTO venues (venue_id, people) VALUES (?, ?)", (venue['venue_id'], venue['people']))
    except Exception as e:
        log.warning(log.exc(e))
        return
    connection.commit()

def get_venues():
    db.execute("SELECT * FROM venues")
    venues = [dict(venue) for venue in db.fetchall()]    
    return venues

def update_venues(venues):
    for venue in venues:
        db.execute("UPDATE venues SET people=? WHERE venue_id=?", (venue['people'], venue['venue_id']))
    log.debug("updated %s venues" % len(venues))
    connection.commit()

