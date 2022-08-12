from io import StringIO
import re

from pandas import DataFrame

from .services import inventory, stat_cd, parameter
from . import formats



QUALIFICATION_CODES = {
    'e': 'edited/estimated', #The value has been edited or estimated by USGS personnel'
    '<': 'value is known to be less than reported value', #'The Value is known to be less than reported value.
    '>': 'value is known to be greater than reported value', #The value is known to be greater than reported value.
    'R': 'revised', #Records for these data have been revised.
    'A': 'approved', #Approved for publication -- Processing and review completed.
    'P': 'provisional', #Provisional data subject to revision.
    '':''
}

def qc_map_function (qc):

    if qc in QUALIFICATION_CODES:
        return QUALIFICATION_CODES[qc]
    multi_qc = []
    for sqc in qc.split(':'):
        try:
            multi_qc.append(QUALIFICATION_CODES[sqc])
        except:
            multi_qc.append(sqc)
    return ','.join(multi_qc)

def build_summary_table(sites, inventory_callback=inventory.call, verbose = False):

    site_list = []
    for idx in range(len(sites)):
        site_id = sites[idx]
        if verbose:
            print(site_id, idx, 'of', len(sites))
        si = inventory_callback(site_id)
        row = {
            'site-id': site_id, 
            'site-name':si["name"],
            'site-type': si["site-type"],
            "organization": si["organization"],
            "link": si['url'],
            'huc8': si['geolocation']['huc8'],    
        }
        try:
            lat, long, elev = inventory.geolocation_to_wgs84(si)
        except:
            print(si)
            break
        row['latitude'] = lat
        row['longitude'] = long 
        row['elevation'] = elev
        

        for dt in si['inventory']:
            row[dt] = True


        site_list.append(row)
    st = DataFrame(site_list)
    st[st.columns[8:]] = st[st.columns[9:]].fillna(False) 
    return st

def readable_rdb_DatafFame(callback, **kwargs):
    
    kwargs['format'] = 'rdb'
    if type(callback) is str:
        response = callback
    else:
        response = callback(**kwargs)

    table = formats.rdb_to_DataFrame(response)
    table = table.fillna('')  ## fill na with empty str


    cols = list(table.columns)
    new_cols = []

    param_pat = re.compile("^\d{4}_\d{5}_\d{5}$")
    cix = 0
    while cix < len(cols):
        col = cols[cix]
        if col == 'agency_cd':
            new_cols.append('agency')
        elif param_pat.match(col) is not None:
            
            ts, pc, sc = col.split('_')
            pc_tab = formats.rdb_to_DataFrame(
                parameter.call(parm_nm_cd=pc, fmt='rdb')
            )
            
            name = str(pc_tab['parm_nm'].values[0])
            stat = stat_cd.call(stat_code=sc)[sc]['name'].lower()
            new_cols.append('%s (%s)' % (name, stat))
            cix+=1
            col =  cols[cix] # now qualification col using old name
            new_cols.append('%s (%s) qualification' % (name, stat))
            
            table[col] = table[col].apply(qc_map_function)
            
        else:
            new_cols.append(col)## fallback
        cix += 1
            
    table.columns=new_cols

    return table


def statistics_cd_DataFrame(stats):
    t = DataFrame(stat_cd.call(stat_code=','.join(stats))).T
    t.index.name='code'
    return t
