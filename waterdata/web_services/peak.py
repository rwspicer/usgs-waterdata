
from email.policy import default
from . import generic
from . import globals
from .available import services

from datetime import date



filters = {
   'site_no': globals.default,
   'agency_cd': globals.default,
   'format': lambda a, oa: a == 'rdb',

}


aliases = {
}

# https://nwis.waterdata.usgs.gov/nwis/peak?site_no=15798700&agency_cd=USGS&format=rdb

def call(**kwargs):
    kwargs['format'] = 'rdb'

    clean_args = globals.validate_args(kwargs, filters, aliases)
    
    response = generic.call('peak', **clean_args)
    return response



