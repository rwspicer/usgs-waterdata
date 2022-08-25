"""
Daily Values Service
--------------------

new waterservices daily values service
"""
from . import generic
from . import globals

# filters
filters = {
    'statCd': lambda a, oa: len(a.split(',')) <= 20 and all([len(p) == 5 for p in a.split(',')])
}

filters.update(globals.filters)
filters.update(globals.value_filters)
filters['format'] = lambda a, oa: a in ['waterml', 'waterml,1.1', 'waterml,2.0' , 'rdb', 'rdb,1.0', 'json', 'json,1.1']

# aliases
aliases = {
    'statisticCd':'statCd'
}
filters.update(globals.aliases)
aliases.update(globals.value_aliases)


def call(**kwargs):
    """calls service to get daily water data mostly discharge and gage-height

    Parameters
    ----------
    **kwargs:
        keyword arguments defined in waterdata.services.dv.filters,
        waterdata.services.globals.filters, and 
        waterdata.services.globals.value_filters.

    Returns
    -------
    response:
        format is defined by kwargs['format']

    """

    clean_args = globals.validate_args(kwargs, filters, aliases)
    
    response = generic.call('dv', **clean_args)
    return response



