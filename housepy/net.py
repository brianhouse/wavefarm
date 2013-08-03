import urllib, urllib2
from lib.poster.encode import multipart_encode
from lib.poster.streaminghttp import register_openers        
from log import log

# note that this will read into memory first. direct to disk would be better

def grab(source, destination, data=None, timeout=30, username=None, password=None, headers=None):
    response = read(source, data=data, timeout=timeout, username=username, password=password, headers=headers)
    f = open(destination, 'w')
    f.write(response)
    f.close()

def read(source, data=None, multipart=False, timeout=30, username=None, password=None, headers=None):
    if multipart:
        register_openers()        
        datagen, headers = multipart_encode(data)   # {'file': open("DSC0001.jpg", "rb")}
        request = urllib2.Request(source, datagen, headers)
    elif data is not None:
        if type(data) == dict:
            data = urllib.urlencode(data)
        request = urllib2.Request(source, data)
    else:
        request = urllib2.Request(source)
    if username and password:
        import base64
        auth = base64.b64encode('%s:%s' % (username, password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % auth) 
    if headers:
        for header, value in headers.items():
            request.add_header(header, value) 
    return urllib2.urlopen(request, timeout=timeout).read()        
        
def urlencode(data):
    import urllib
    return urllib.urlencode(data)

def urldecode(query_string):
    import urlparse
    data = urlparse.parse_qs(query_string, keep_blank_values=True)
    for d in data:
        if len(data[d]) == 0:
            data[d] = ""
        elif len(data[d]) == 1:
            data[d] = data[d][0]
    return data
            
def validate_url(url):
    import re
    pattern = '^(http://|(www)\\.)[a-z0-9-]+(\\.[a-z0-9-]+)+([/?].*)?$'     ## does not support unicode
    return re.match(pattern, url) != None
