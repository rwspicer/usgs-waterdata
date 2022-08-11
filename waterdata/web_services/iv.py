from . import generic
from . import globals


filters = {}

filters.update(globals.filters)
filters.update(globals.value_filters)
filters['format'] = lambda a, oa: a in ['waterml', 'waterml,1.1', 'waterml,2.0' , 'rdb', 'rdb,1.0', 'json', 'json,1.1']


aliases = {}
aliases.update(globals.aliases)
aliases.update(globals.value_aliases)


def call(**kwargs):

    clean_args = globals.validate_args(kwargs, filters, aliases)
    
    response = generic.call('iv', **clean_args)
    return response



