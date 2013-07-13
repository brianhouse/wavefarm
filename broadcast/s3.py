#!/usr/bin/env python

import mimetypes, os, sys, time, datetime, boto
from config import config
    
def list_contents():
    print("s3.list")
    connection = boto.connect_s3(config['aws']['access_key_id'], config['aws']['secret_access_key'])
    print("--> listing %s" % (config['aws']['bucket']))        
    try:
        bucket = connection.get_bucket(config['aws']['bucket'])
        contents = [key.name.encode('utf-8') for key in bucket.list()]
    except Exception as e:
        print("--> failed: %s" % e)
        return False
    print("--> %s" % contents)
    return contents

def download(path, destination=None):
    if destination is None:
        destination = path
    print("s3.download")        
    connection = boto.connect_s3(config['aws']['access_key_id'], config['aws']['secret_access_key'])
    print("--> downloading %s/%s" % (config['aws']['bucket'], path))        
    try:
        bucket = connection.get_bucket(config['aws']['bucket'])
        key = bucket.get_key(path)    
        key.get_contents_to_filename(destination)
    except Exception as e:
        print("--> failed: %s" % e)
        return False
    print("--> successfully wrote %s" % destination)
    return True
    
