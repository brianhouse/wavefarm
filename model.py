#!/usr/bin/env python

import sqlite3, json, time
from housepy import config, log

connection = sqlite3.connect("data.db")
connection.row_factory = sqlite3.Row
db = connection.cursor()

def init():
    try:
        db.execute("CREATE TABLE IF NOT EXISTS readings (device TEXT, kind TEXT, t INTEGER, v REAL, r REAL)")
        db.execute("CREATE UNIQUE INDEX IF NOT EXISTS device_kind_t ON readings(device, kind, t)")
        #
        db.execute("CREATE TABLE IF NOT EXISTS events (device TEXT, kind TEXT, t INTEGER, v REAL, d REAL, q REAL)")
        db.execute("CREATE UNIQUE INDEX IF NOT EXISTS device_kind_t ON events(device, kind, t)")
        ##
        db.execute("CREATE TABLE IF NOT EXISTS venues (venue_id TEXT, people INTEGER)")
        db.execute("CREATE UNIQUE INDEX IF NOT EXISTS venues_venue_id ON venues(venue_id)")
    except Exception as e:
        log.error(log.exc(e))
        return
    connection.commit()
init()

def insert_reading(device, kind, v, t=None, cumulative=False):
    """ Cumulative: input will be monotonic, but we only want the delta in value
                    eg, getting amount of rain per hour from a continuously updated daily total
    """
    try:
        r = None
        db.execute("SELECT t, v, r FROM readings WHERE device=? AND kind=? ORDER BY t DESC LIMIT 1", (device, kind))
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
        db.execute("INSERT INTO readings (device, kind, t, v, r) VALUES (?, ?, ?, ?, ?)", (device, kind, t, v, r))
        entry_id = db.lastrowid            
        log.info("%s,%s -> %s (%s)" % (device, kind, v, entry_id))
    except Exception as e:
        log.error(log.exc(e))
        return
    connection.commit()
    return entry_id

def fetch_readings(kind, start_t, stop_t):
    # need to account for unchanged readings starting prior to t
    db.execute("SELECT * FROM readings WHERE kind=? AND t>=? AND t<?", (kind, start_t, stop_t))
    rows = [dict(reading) for reading in db.fetchall()]
    if not len(rows) or rows[0]['t'] > start_t:
        db.execute("SELECT * FROM readings WHERE kind=? AND t<? ORDER BY t DESC LIMIT 1", (kind, start_t))
        r = db.fetchone()
        if r is None:
            log.warning("complete data not available for %s" % kind)
            return []
        r = dict(r)
        r['t'] = start_t
        rows.insert(0, r)
    return rows 

def insert_event(device, kind, v, t=None, d=0.0, q=None):
    if t is None:
        t = int(time.time())    
    try:
        db.execute("INSERT INTO events (device, kind, t, v, d, q) VALUES (?, ?, ?, ?, ?, ?)", (device, kind, t, v, d, q))
        entry_id = db.lastrowid
        log.info("%s,%s -> %s%s (%s)" % (device, kind, v, ("%s " % q if q is not None else ""), entry_id))
    except Exception as e:
        log.error(log.exc(e))
        return
    connection.commit()
    return entry_id

def fetch_events(kind, start_t, stop_t):
    db.execute("SELECT * FROM events WHERE kind=? AND t>=? AND t<?", (kind, start_t, stop_t))
    rows = [dict(event) for event in db.fetchall()]
    return rows 


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

