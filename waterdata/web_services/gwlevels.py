
from distutils.command.clean import clean
from . import generic
from . import globals
from .available import services

from datetime import date


filters = {}

filters.update(globals.filters)
filters.update(globals.value_filters)
filters['format'] = lambda a, oa: a in ['waterml', 'waterml,1.2', 'waterml,2.0' , 'rdb', 'rdb,1.0', 'json', 'json,1.2']


aliases = {}
aliases.update(globals.aliases)
aliases.update(globals.value_aliases)


def call(**kwargs):

    clean_args = globals.validate_args(kwargs, filters, aliases)
    
    response = generic.call('gwlevels', **clean_args)
    return response



