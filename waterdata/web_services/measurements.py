from . import generic
from . import globals
from .available import services

from datetime import date



filters = {
    'site_no': globals.default,
    'agency_cd': globals.default,
    'format': lambda a, oa: a in ['rdb','rdb_expanded'],

}


aliases = {
}

# https://waterdata.usgs.gov/nwis/measurements?site_no=15798700&agency_cd=USGS&format=rdb_expanded

def call(**kwargs):
    if not 'format' in kwargs:
        kwargs['format'] = 'rdb_expanded'

    clean_args = globals.validate_args(kwargs, filters, aliases)
    
    response = generic.call('measurements', **clean_args)
    return response



