from . import generic
from . import globals
from .available import services



filters = {
    'siteOutput': lambda a, oa: a in ['basic','expanded'] and (not 'seriesCatalogOutput' in oa or 'outputDataTypeCd' in oa ), 
    'seriesCatalogOutput': lambda a, oa: a in ['true','false'] and not 'SiteOutput' in oa,
    'outputDataTypeCd':  lambda a, oa: all( [sa in ['all'] + services[:11] for sa in a.split(',')] ) and not 'SiteOutput' in oa, 
    'siteName': globals.default, 
    'siteNameMatchOperator': lambda a, oa: a in ['start', 'any', 'exac' ],
    'hasDataTypeCd': lambda a, oa: all( [sa in ['all'] + services[:11] for sa in a.split(',')] ),
}

filters.update(globals.filters)
filters['format'] = lambda a, oa: a in ['rdb', 'rdb,1.0', 'gm', 'gm,1.0', 'ge', 'ge,1.0', 'mapper', 'mapper,1.0']


# aliases 
aliases = {
    'site_output': 'siteOutput', 
    'outputDataType': 'outputDataTypeCd',
    'siteNm': 'siteName', 
    'stationName': 'siteName', 
    'stationNm': 'siteName',
    'siteNameMatch':'siteNameMatchOperator', 
    'siteNmMatch':'siteNameMatchOperator', 
    'stationNameMatch':'siteNameMatchOperator', 
    'stationNmMatch':'siteNameMatchOperator',
    'hasDataType': 'hasDataTypeCd',
    'dataTypeCd': 'hasDataTypeCd', 
    'dataType': 'hasDataTypeCd',
}

aliases.update(globals.aliases)



def call(**kwargs):
    """calls service to info on sites

    Parameters
    ----------
    **kwargs:
        keyword arguments defined in waterdata.services.site.filters,
        waterdata.services.globals.filters, and 

    Returns
    -------
    response:
        format is defined by kwargs['format']

    """

    clean_args = globals.validate_args(kwargs, filters, aliases)

    response = generic.call('site', **clean_args)
    return response



