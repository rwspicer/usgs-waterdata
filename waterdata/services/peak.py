"""
Peak Flow Service
-----------------
"""
from . import generic
from . import globals

# Filters
filters = {
    'site_no': globals.default,
    'agency_cd': globals.default,
    'format': lambda a, oa: a == 'rdb',
}

# aliases
aliases = {
}

# https://nwis.waterdata.usgs.gov/nwis/peak?site_no=15798700&agency_cd=USGS&format=rdb

def call(**kwargs):
    """calls service to get peak yearly discharge and gage-height

    Parameters
    ----------
    **kwargs:
       keyword arguments defined in waterdata.services.peak.filters,

    Returns
    -------
    response:
       format is defined by kwargs['format']

    """
    kwargs['format'] = 'rdb'

    clean_args = globals.validate_args(kwargs, filters, aliases)
   
    response = generic.call('peak', **clean_args)
    return response



