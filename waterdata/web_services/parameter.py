
from heapq import merge
from . import generic
from .available import services

from datetime import date

default = lambda a, oa: True

def valid_date_str(date_str):
    try:
        y, m, d = [int(f) for f in date_str.split('-')]
        date(y,m,d)
    except:
        return False
    return True

# https://help.waterdata.usgs.gov/code/parameter_cd_query?fmt=rdb&group_cd=%
# https://help.waterdata.usgs.gov/code/parameter_cd_query?fmt=rdb&inline=true&group_cd=%
# # https://help.waterdata.usgs.gov/code/parameter_cd_nm_query?parm_nm_cd=00060&fmt=rdb&inline=true
# https://help.waterdata.usgs.gov/code/parameter_cd_query?fmt=rdb&group_cd=BIO&inline=true
# https://help.waterdata.usgs.gov/code/fixed_parms_query?fmt=rdb

filters = {
    'fmt': default,
    'group_cd': default,
    'inline': default,
    'parm_nm_cd':default

}

# aliases 
aliases = {
    'format': 'fmt'
}





def call(**kwargs):

    clean_args = globals.validate_args(kwargs, filters, aliases)
    response = generic.call('parameter', **clean_args)
    return response

def lookup(**kwargs):
    """
    """
    kwargs['fmt'] = 'rdb'
    param_codes = kwargs['param_codes']
    del(kwargs['param_codes'])
    merged_response = ""
    for param in param_codes:
        print(param)
        kwargs['parm_nm_cd'] = param
        rsp = call(**kwargs)
        if merged_response == "":
            merged_response += rsp
        else:
            rsp = rsp.split("\n")[-2]
            merged_response += rsp + '\n'
    return merged_response

