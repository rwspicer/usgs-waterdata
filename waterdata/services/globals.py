"""
Globals
-------

Global values and functions for services
"""
from datetime import date

# Default filter function
default = lambda a, oa: True

STATES = [
    'AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI','ID','IL','IN',
    'IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH',
    'NJ','NM','NY','NC','ND','OH','OK','OR','PA','PR','RI','SC','SD','TN','TX',
    'UT','VT','VA','VI','WA','WV','WI','WY'
]

SITE_TYPES = [
    'AG','AS','AT','AW','ES','FA','FA-AWL','FA-CI','FA-CS','FA-DV','FA-FON',
    'FA-GC','FA-HP','FA-LF','FA-OF','FA-PV','FA-QC','FA-SEW','FA-SPS','FA-STS',
    'FA-TEP','FA-WDS','FA-WIW','FA-WTP','FA-WU','FA-WWD','FA-WWTP','GL','GW',
    'GW-CR','GW-EX','GW-HZ','GW-IW','GW-MW','GW-TH','LA','LA-EX','LA-OU',
    'LA-PLY','LA-SH','LA-SNK','LA-SR','LA-VOL','LK','OC','OC-CO','SB','SB-CV',
    'SB-GWD','SB-TSM','SB-UZ','SP','SS','ST','ST-CA','ST-DCH','ST-TS','WE'
]

LOCATION_FILTERS = ['sites', 'stateCd', 'huc', 'bBox', 'countyCd']

def contains_location_filter(arguments):
    """tests if augments contains a location filter
    
    Parameters
    ----------
    arguments: dict

    Returns
    -------
    bool
    """
    for f in arguments:
        if f in LOCATION_FILTERS:
            return True
    return False



def valid_date_str(date_str): # need to have a datetime version
    """Tests if date string has valid forma
    
    parameters
    ----------
    date_str: string

    Returns
    -------
    Bool 
        True if format is 'YYYY-MM-DD'
    """
    try:
        y, m, d = [int(f) for f in date_str.split('-')]
        date(y,m,d)
    except:
        return False
    return True

## Default filters that most services use
filters = {
    'sites': lambda a, oa: len(a.split(',')) <= 100 and not contains_location_filter(oa),
    'stateCd': lambda a, oa: a in STATES and not contains_location_filter(oa), 
    'huc': lambda a, oa: ((len(a) == 2 and 0<int(a)<=21) or len(a) == 8) and not contains_location_filter(oa), #Could be better
    'bBox': lambda a, oa: len(a.split(',')) == 4 and not contains_location_filter(oa), #Could be better
    'countyCd': lambda a, oa: len(a.split(',')) == 5 and not contains_location_filter(oa), #Could be better 
    'format': default,
    'startDt': lambda a, oa: valid_date_str(a) and not 'period' in oa,
    'endDt': lambda a, oa: valid_date_str(a) and not 'period' in oa,
    'period': lambda a, oa: not ('startDt' in oa or 'endDt' in oa),
    'siteType': lambda a, oa: all([st in SITE_TYPES  for st in a.split(',')]),
    'modifiedSince': default,
    'agencyCd': default,
    'siteStatus': lambda a, oa: a in ['all', 'active', 'inactive' ],
    'altMinVa': default, 
    'altMaxVa': default, 
    'drainAreaMin': default,  
    'drainAreaMax': default, 
    'aquiferCd': default,
    'localAquiferCd': default,
    'wellDepthMin': default,
    'wellDepthMax': default,
    'holeDepthMin': default,
    'holeDepthMax': default,
}

## value filters that many services
value_filters = {
    'indent': lambda a, oa: a in ['on','off'],
    'parameterCd': lambda a, oa: len(a.split(',')) <= 100 and all([len(p) == 5 for p in a.split(',')]),
}

## aliases for default services
aliases = {
    'site': 'sites',
    'location': 'sites',
    'stateCds': 'stateCd',
    'hucs': 'huc',
    'countyCds': 'countyCd',
    'siteTypes': 'siteType', 
    'siteTypeCd': 'siteType', 
    'siteTypeCds': 'siteType',
    'variable': 'parameterCd', 
    'parameterCds': 'parameterCd', 
    'variables': 'parameterCd', 
    'var': 'parameterCd', 
    'vars': 'parameterCd', 
    'parmCd': 'parameterCd',
    'agencyCds': 'agencyCd',
    'altMin': 'altMinVa', 
    'altMax': 'altMinVa', 
    'drainAreaMinVa': 'drainAreaMin',  
    'drainAreaMaxVa': 'drainAreaMax', 
    'wellDepthMinVa': 'wellDepthMin',
    'wellDepthMaxVa': 'wellDepthMax',
    'holeDepthMinVa': 'holeDepthMin',
    'holeDepthMaxVa': 'holeDepthMax',
}

# Aliases for value filters
value_aliases =  {
    'variable': 'parameterCd', 
    'parameterCds': 'parameterCd', 
    'variables': 'parameterCd', 
    'var': 'parameterCd', 
    'vars': 'parameterCd', 
    'parmCd':'parameterCd'
}


def validate_args(kwargs, filters, aliases):
    """Checks that arguments pass filter functions

    Parameters
    ----------
    kwargs: dict
        dict of Rest Service parameters
    filters: dict
        dict of validator function matching format <function __main__.f(a, oa)>
        and returns an bool, where a is the agumnet and oa is the list of
        other arguments
    aliases:
        dict mapping alias names to cannon names
    
    Retunrs
    -------
    dict
        cleaned and cannon argument dict
    """
    clean_args = {}
    for arg in kwargs:
        if arg in aliases:
            clean_args[aliases[arg]] = kwargs[arg]
        else:
            clean_args[arg] = kwargs[arg]

    for arg in clean_args:
        clean_args[arg] = str(clean_args[arg])
    
    for arg in clean_args:
        
        other = set(clean_args.keys())
        other.remove(arg)
        # print(arg, other, print(filters[arg]))
        if not filters[arg](clean_args[arg], other):
            print('Filter: %s, is invalid' % arg )
            return None
    return clean_args

