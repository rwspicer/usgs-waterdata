from . import generic
from . import globals

filters = {
    'site_no': globals.default,
    'agency_cd': globals.default,
    'format': lambda a, oa: a in ['rdb','rdb_expanded'],

}


aliases = {
}

# https://waterdata.usgs.gov/nwis/measurements?site_no=15798700&agency_cd=USGS&format=rdb_expanded

def call(**kwargs):
    """calls service to access streamflow field measurements 

    Parameters
    ----------
    **kwargs:
        keyword arguments defined in waterdata.services.measurements.filters,

    Returns
    -------
    response:
        format is defined by kwargs['format']

    """
    if not 'format' in kwargs:
        kwargs['format'] = 'rdb_expanded'

    clean_args = globals.validate_args(kwargs, filters, aliases)
    
    response = generic.call('measurements', **clean_args)
    return response



