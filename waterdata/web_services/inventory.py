
from . import generic
from . import globals
from .available import BASE_WATERDATA_URL, WATERDATA_URL

from datetime import date
import geojson 
import pyproj
import copy
import numpy as np


filters = {
    'site_no':globals.default,
    'agency_cd':globals.default,
    'format': lambda a, oa: a in ['dict', 'geojson']
}


# aliases 
aliases = {
}


def convert_degrees(degrees_in):
    if type(degrees_in) is str:
        degrees_in = degrees_in.strip()
        degrees, mmss = degrees_in.split('°')
        mm, ss = mmss[:-1].split("'")
        return float(degrees) + float(mm)/60 + float(ss)/3600
    else:
        degrees = degrees_in // 1
        decimal = degrees_in - degrees
        mm  = decimal * 60 // 1
        ss = (decimal * 60 - mm) * 60
        return '''%i°%02i'%02i"''' % (degrees, mm, ss)

def parse_response(html, url):

    

    site_inventory = {}
    site_table = html.find("div", {"id":"stationTable"})

    # for item in st.findAll('dd'):
    site_id_name = html.find('h2').text.strip()
    words = site_id_name.split(' ')

    site_inventory["id"] = int(words[1])
    site_inventory["name"] = ' '.join(words[2:])
    site_inventory["organization"] = words[0]
    site_inventory["url"] = url

    site_inventory["site-type"] = html.find('h3').text.strip()


    site_inventory['geolocation'] = {}
    site_inventory['inventory'] = {}
    ops_note = None 
    for item in site_table.findAll('dd'):
        text = item.text
        # print(text)
        if 'Latitude' in text:
            # print(text)
            idx1 = text.find('Latitude') + len('Latitude')
            idx2 = text.find('"') + 1
            site_inventory['geolocation']['latitude'] = \
                convert_degrees(text[idx1:idx2])
            
            text = text[idx2:]
            idx1 =  text.find('Longitude') + len('Longitude')
            idx2 = text.find('"') + 1
            site_inventory['geolocation']['longitude'] = \
                convert_degrees(text[idx1:idx2]) * -1
                ## because this is west need -1
            
            site_inventory['geolocation']['datum'] = text[idx2:].strip()
            text = text[idx2:]

        if 'Hydrologic Unit' in text:
            # if len(text.split(',')) == 3:
            region, state, unit = text.split(',')
            # else:
            #     print('>>', text, '<<')
            #     raise(KeyError)


            site_inventory['geolocation']['region'] = region.strip()
            site_inventory['geolocation']['state'] = state.strip()
            site_inventory['geolocation']['huc8'] = int(unit.strip()[-8:])

        if 'Drainage area' in text:
            words = text.split(':')[1].strip().split(' ')
            area = words[0]
            units = ' '.join(words[1:])
            site_inventory['geolocation']['drainage-area'] = \
                float(area.replace(',',''))
            site_inventory['geolocation']['drainage-area-units'] = units.strip()
        if 'Datum of gage' in text:
            words = text.split(':')[1].strip().split(' ')
            # print(words)
            site_inventory['geolocation']['elevation'] = \
                float(words[0].replace(',',''))
            site_inventory['geolocation']['elevation-units'] = words[1].strip()
            site_inventory['geolocation']['vertical-datum'] = \
                words[-1][:-1].strip()
            # text.split(' ')

        if "OPERATION:" in text:
            ops_note = ""
        if ops_note:
            ops_note += text.strip()

    site_inventory['operation'] = text
            
    inv_rows = site_table.find('table').find_all('tr')
    # last_row_url = None
    data_type = None
    for row in inv_rows:
        cols = row.find_all('td')
        # r(len(cols), cols)
        if len(cols) == 0:
            continue
        if len(cols)>=4:
            param = ""
            for ix in range(4):#  USGS 15907900 ARTHUR C NR PUMP STATION 3 AK
                elem = cols[ix]
                
                text = elem.text.strip()
                # print(text)
                if ix == 0:
                    if text in ['Revisions','Additional Data Sources']:
                        break
                    if (elem.find('a')):
                        
                        if 'availability statement' in text:
                            text = text.split('(')[0].strip()
                        data_type = text
                        url = BASE_WATERDATA_URL+elem.find('a')['href']
                        site_inventory['inventory'][text] = {
                            "url": url,
                            "parameters": {}
                        }
                        param = 'all'
                        if 'availability statement' in text:
                            site_inventory\
                                ['inventory']\
                                [data_type]\
                                ['data-availability-statement']\
                            = WATERDATA_URL + '?IV_data_availability.html'
                    else:
                        param = text
                    site_inventory\
                        ['inventory'][data_type]['parameters'][param]= {}   
                if ix == 1: 
                    site_inventory\
                        ['inventory'][data_type]['parameters']\
                        [param]['begin-date'] = text 
                if ix == 2: 
                    site_inventory['inventory'][data_type]['parameters']\
                        [param]['end-date'] = text 
                if ix == 3: 
                    site_inventory['inventory'][data_type]['parameters']\
                        [param]['count'] = int(text) if len(text) >0 else None
        elif len(cols)==1:
            
            url = BASE_WATERDATA_URL+cols[0].find('a')['href']
            text = cols[0].text.strip()
            data_type = text
            site_inventory['inventory'][data_type] = {
                "url": url,
                "parameters": {}
            }

        else:
            pass

    return site_inventory      


def geolocation_to_wgs84(site_inventory):
    lat = site_inventory['geolocation']['latitude']
    long = site_inventory['geolocation']['longitude']

    if not 'elevation' in site_inventory['geolocation']:
        return([long, lat, np.nan])

    if site_inventory['geolocation']['elevation-units'] == "feet":
        elev = site_inventory['geolocation']['elevation'] * 0.3048
    else:
        print(site_inventory['geolocation']['elevation-units'])
        raise TypeError()
    datum = site_inventory['geolocation']['datum']
    v_datum = site_inventory['geolocation']['vertical-datum'] 
    
    wgs84 = pyproj.crs.CRS.from_epsg(4326)
    nad83 = pyproj.crs.CRS.from_epsg(4269)
    nad83_navd88 = pyproj.crs.CRS.from_epsg(5498)   
    nad27_ngvd29= pyproj.crs.CRS.from_epsg(7406)

    if datum == 'NAD83' and v_datum == 'NAVD88':
        crs_to_use = nad83_navd88
    elif datum == 'NAD27' and v_datum == 'NGVD29':
        crs_to_use = nad27_ngvd29
    elif datum == 'NAD83':
        crs_to_use = nad83
    else:
        print(datum, v_datum)
        return None

    t = pyproj.transformer.Transformer.from_crs(
        crs_from=crs_to_use, crs_to=wgs84
    ) 
    return t.transform(*[long,lat,elev])
    


def inventory_to_geoJSON(site_inventory):
    point = geojson.Point(geolocation_to_wgs84(site_inventory))

    properties = copy.deepcopy(site_inventory)
    properties['geojson-note'] = (
        'geoJSON coordinates were converted to wgs84'
        ' while coordinates in properties use CRS indicated by'
        ' datum and vertical datum.'
    )

    feature = geojson.Feature(geometry=point, properties=properties)
    return feature


def call(**kwargs):

    clean_args = globals.validate_args(kwargs, filters, aliases)
    if 'format' in clean_args:
        format = clean_args['format'] 
        del(clean_args['format'])
    else:
        format = 'dict'
    response = generic.html('inventory', parse_response, **clean_args)

    # response = parse_response(response)
    if format == 'geojson':
        response = inventory_to_geoJSON(response)
    return response



