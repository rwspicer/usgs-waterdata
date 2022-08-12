from . import generic
from . import globals






# https://help.waterdata.usgs.gov/code/parameter_cd_query?fmt=rdb&group_cd=%
# https://help.waterdata.usgs.gov/code/parameter_cd_query?fmt=rdb&inline=true&group_cd=%
# # https://help.waterdata.usgs.gov/code/parameter_cd_nm_query?parm_nm_cd=00060&fmt=rdb&inline=true
# https://help.waterdata.usgs.gov/code/parameter_cd_query?fmt=rdb&group_cd=BIO&inline=true
# https://help.waterdata.usgs.gov/code/fixed_parms_query?fmt=rdb

filters = {
    'fmt': globals.default,
    'group_cd': globals.default,
    'inline': globals.default,
    'parm_nm_cd': globals.default

}

# aliases 
aliases = {
    'format': 'fmt'
}





def call(**kwargs):
    """calls service to look up a parameter code

    Parameters
    ----------
    **kwargs:
        keyword arguments defined in waterdata.services.parameter.filters,

    Returns
    -------
    response:
        format is defined by kwargs['format']

    """
    clean_args = globals.validate_args(kwargs, filters, aliases)
    response = generic.call('parameter', **clean_args)
    return response

def lookup(**kwargs):
    """Sudo service look up multiple param codes using parameter.call and 
    merge response

    Parameters
    ----------
    **kwargs:
        keyword arguments defined in waterdata.services.parameter.filters,

    Returns
    -------
    response:
        format is defined by kwargs['format']

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

