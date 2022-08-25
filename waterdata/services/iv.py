"""
Instantaneous values Service
----------------------------
"""
from . import generic
from . import globals

# Filters
filters = {}

filters.update(globals.filters)
filters.update(globals.value_filters)
filters['format'] = lambda a, oa: a in ['waterml', 'waterml,1.1', 'waterml,2.0' , 'rdb', 'rdb,1.0', 'json', 'json,1.1']

# Aliases
aliases = {}
aliases.update(globals.aliases)
aliases.update(globals.value_aliases)


def call(**kwargs):
    """calls service to get instantaneous water data mostly discharge and 
        gage-height

        Parameters
        ----------
        **kwargs:
            keyword arguments defined in waterdata.services.iv.filters,
            waterdata.services.globals.filters, and 
            waterdata.services.globals.value_filters.

        Returns
        -------
        response:
            format is defined by kwargs['format']

        """
    clean_args = globals.validate_args(kwargs, filters, aliases)
    
    response = generic.call('iv', **clean_args)
    return response



