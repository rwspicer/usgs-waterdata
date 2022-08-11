from . import generic
from . import globals

##TODO implement other arguments

filters = {
    'site_no': globals.default,
    'agency_cd': globals.default,
    'format': lambda a, oa: a in ['rdb', 'rdb_expanded'],
    
    # 'inventory_output': globals.default
    # rdb_inventory_output=file,
    # TZoutput=0
    # pm_cd_compare=Greater%20than,
    # radio_parm_cds=all_parm_cds,
    # qw_attributes=0
    # qw_sample_wide=wide
    # rdb_qw_attributes=0,
    # date_format=YYYY-MM-DD,
    # rdb_compression=value
    # submitted_form=brief_list
}


aliases = {
}
# https://nwis.waterdata.usgs.gov/usa/nwis/qwdata/?site_no=15798700&agency_cd=USGS&inventory_output=0&rdb_inventory_output=file&TZoutput=0&pm_cd_compare=Greater%20than&radio_parm_cds=all_parm_cds&qw_attributes=0&format=rdb&qw_sample_wide=wide&rdb_qw_attributes=0&date_format=YYYY-MM-DD&rdb_compression=value&submitted_form=brief_list

def call(**kwargs):
    if not 'format' in kwargs:
        kwargs['format'] = 'rdb_expanded'

    clean_args = globals.validate_args(kwargs, filters, aliases)
    
    response = generic.call('qwdata', **clean_args)
    return response



