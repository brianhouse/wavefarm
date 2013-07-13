#!/usr/bin/env python

import s3

keys = s3.list_contents()
keys.sort()
filename = keys[-1]

s3.download(filename, "change_ringing.aif")
