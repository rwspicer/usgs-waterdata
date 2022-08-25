"""
Simple Daily Data Service
-------------------------

Access to waterdata.usgs.gov/nwis/dv/? which is a less robust version of 
the waterservices dv api accessed in waterdata.services.dv which should be
used instead in most cases.  
"""
from . import generic
from . import globals

filters = {
    'cb_all_': globals.default,
    'cb_00060': globals.default, # discharge cfs
    'cb_00065': globals.default, # Gage height, feet
    'cb_00045': globals.default, # precip (not usable data) (mm)
    'cb_00010': globals.default, # water temp c 

    'format': lambda a, oa: a == 'rdb',
    'site_no':globals.default,
    'referred_module':globals.default,
    'period':globals.default,
    'begin_date':globals.default,
    'end_date':globals.default,

}

#alaises
aliases = {
}

def call(**kwargs):
    """calls service to get daily waterdata

    Parameters
    ----------
    **kwargs:
        keyword arguments defined in waterdata.services.daily_data.filters

    Returns
    -------
    response:
        format is defined by kwargs['format']

    """
    kwargs['format'] = 'rdb'

    clean_args = globals.validate_args(kwargs, filters, aliases)
    
    response = generic.call('daily-data', **clean_args)
    return response



