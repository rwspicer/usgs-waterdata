from . import generic
from .available import services

from datetime import date

default = lambda a, oa: True



def valid_date_str(date_str):
    try:
        y, m, d = [int(f) for f in date_str.split('-')]
        date(y,m,d)
    except:
        return False
    return True


filters = {
    'fmt': default,
    'inline': default,

}

# aliases 
aliases = {
    'format': 'fmt'
}





def call(**kwargs):
    
    clean_args = globals.validate_args(kwargs, filters, aliases)
    response = generic.call('fixed-parameter', **clean_args)
    return response

