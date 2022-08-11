"""
"""
from inspect import Parameter
import os

WATERDATA_URL = "https://waterdata.usgs.gov/nwis/"
BASE_WATERDATA_URL = "https://waterdata.usgs.gov"
WATERSERVICES_URL = "https://waterservices.usgs.gov/nwis/"
PARAMETER_URL = 'https://help.waterdata.usgs.gov/code/parameter_cd_nm_query'
FIXED_PARAMETER_URL = 'https://help.waterdata.usgs.gov/code/fixed_parms_query'


class AvailableServiceError(Exception):
    pass


services = [
    "iv", "uv", "rt", "dv", "pk", "sv", "gw", "qw", "id", "aw", "ad",
    "site", 'parameter', 'fixed-parameter', "gwlevels", 'inventory'
]

names = {
    "iv": "Instantaneous values", 
    "uv": "Unit values", 
    "rt": "Real-time data ",
    "dv": "Daily values ", 
    "pk": "Peaks measurements ", 
    "sv": "Site visits", 
    "gw": "Groundwater levels", 
    "qw": "Water-quality", 
    "id": "Historical instantaneous values ", 
    "aw": "Active Groundwater Level Network", 
    "ad": "Annual Water Data Reports", 
    "site": "Site Metadata",
    'parameter': 'parameter code lookup', 
    'fixed-parameter': 'fixed parameter code lookup'
}

descriptions = {
    "iv": (
        "Instantaneous values (time-series measurements typically recorded"
        " by automated equipment at frequent intervals (e.g., hourly)"
    ),
    "uv": "Unit values (alias for iv)",
    "rt": "Real-time data (alias for iv)",
    "dv":(
        "Daily values (once daily measurements or summarized information"
        " for a particular day, such as daily maximum, minimum and mean)"
    ),
    "pk": (
        "Peaks measurements of water levels and streamflow for surface water"
        " sites (such as during floods, may be either an automated or a manual"
        " measurement)"
    ),
    "sv": (
        "Site visits (irregular manual surface water measurements, excluding"
        " peak measurements)"
    ),
    "gw": (
        "Groundwater levels measured at irregular, discrete intervals. For"
        " recorded, time series groundwater levels, use iv or id."
    ),
    "qw": (
        "Water-quality data from discrete sampling events and analyzed in"
        " the field or in a laboratory. For recorded time series water-quality"
        " data, use iv or id."
    ),
    "id": (
        "Historical instantaneous values (sites in the USGS Instantaneous"
        " Data Archive External Link)"
    ),
    "aw": (
        "Sites monitored by the USGS Active Groundwater Level Network"
        " External Link"
    ),
    "ad": "Sites included in USGS Annual Water Data Reports External Link",
    "site": "Site Metadata",
    'parameter': 'parameter code lookup', 
    'fixed-parameter': 'fixed parameter code lookup'
}

def get_url(service):
    if not service in services:
        raise AvailableServiceError (
            "service %s is not a valid web service" % service
        )
    if service == 'parameter':
        url = os.path.join(PARAMETER_URL, service)
    elif service == 'fixed-parameter':
        url = os.path.join(FIXED_PARAMETER_URL, service)
    elif service in ['inventory']:
        url = os.path.join(WATERDATA_URL, service)
    else:
        url = os.path.join(WATERSERVICES_URL, service)
    return url

