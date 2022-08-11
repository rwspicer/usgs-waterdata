"""
"""
import os
import urllib.request

import requests
from bs4 import BeautifulSoup
import validators


from . import available

class ValidURLError(Exception):
    pass

class BadResponseError(Exception):
    pass

class NoDataError(Exception):
    pass

def execute(urlbase, **kwargs):

    args = '&'.join([ '%s=%s' % (k, kwargs[k]) for k in kwargs])
    args = '?' + args.replace(', ',',').replace('[','').replace(']','')

    url = os.path.join(urlbase, args)
    print(url)
    if 'https://' not in url:
        url = 'https://' + url
   
        # print(url)
    if not validators.url(url):
        raise ValidURLError('URL invalid: %s' % url)

    r = requests.get(url)
    if r.status_code != 200:
        raise BadResponseError('Invalid Response: %s' % r.status_code + r.text)

    if r.text == 'No sites/data found using the selection criteria specified':
        raise NoDataError(r.text)
        
    return r.text

def call(service, **kwargs):
    """
    """
    base_url = available.get_url(service)
    
    return execute(base_url, **kwargs)

def html(service, parser, **kwargs):
    base_url = available.get_url(service)
    if len(kwargs) > 0:
        args = '&'.join([ '%s=%s' % (k, kwargs[k]) for k in kwargs])
        args = '?' + args.replace(', ',',').replace('[','').replace(']','')
        url = os.path.join(base_url,args)
    else:
        url = base_url
    # print(url)
    fp = urllib.request.urlopen(url)
    html = BeautifulSoup(fp, "html.parser")
    return parser(html, url)

    

