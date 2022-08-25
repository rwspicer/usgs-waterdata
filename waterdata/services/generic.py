"""
Generic
-------

Generic service adn simulated service functions
"""
import os
import urllib.request

import requests
from bs4 import BeautifulSoup
import validators

from . import available

class ValidURLError(Exception):
    """Exception raised if URL is invalid"""
    pass

class BadResponseError(Exception):
    """Exception raised if HTTP response is not 200"""
    pass

class NoDataError(Exception):
    """Exception raised if no data is returned"""
    pass

def execute(urlbase, **kwargs):
    """Execute a HTTP request by joining REST like arguments to an url

    Parameters
    ----------
    urlbase: str
        service url
    kwargs: dict 
        key value pairs to pass as REST argument

    Exceptions
    ----------
    ValidURLError, BadResponseError, NoDataError 
        These are returned if if response is invalid in some form 
    
    Returns
    -------
    str
        response text if response is valid
    """
    args = '&'.join([ '%s=%s' % (k, kwargs[k]) for k in kwargs])
    args = '?' + args.replace(', ',',').replace('[','').replace(']','')

    url = os.path.join(urlbase, args)
    # print(url)
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
    """Generic call to REST url

    Parameters
    ----------
    service: str
        name of available service see available.py
    kwargs: dict 
        key value pairs to pass as REST argument
    

    Returns
    -------
    str
        response text
    """
    base_url = available.get_url(service)
    
    return execute(base_url, **kwargs)

def html(service, parser, **kwargs):
    """Generic call to HTML simulated service  url

    Parameters
    ----------
    service: str
        name of available service see available.py
    parser: function
        function that parses html response
    kwargs: dict 
        key value pairs to pass as REST argument
    

    Returns
    -------
    str
        response text
    """
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

    

