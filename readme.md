# README

python interface to USGS NWIS waterdata sites and services

## installation  
 
- Install packages from `requirements.txt`
- Run `python setup.py install`

## How to use

all services and pseudo-services  are called with the same format passing 
filters as keyword arguments to the serrvices call function. See each
services' domination for valid filters. They return the response in the 
format specified. 

```
import waterdata

response = waterdata.services.dv.call(
    sites='15798700', 
    parameterCd='00065,00060,00010', 
    startDt='2001-01-01, endDt='2001-21-31'
    format='rdb'
)
```

`waterdata.formats` and `waterdata.views` also provide functions for converting
and saving responses to useful formats. These functions typically take the 
service function and keywords filters as some arguments. See the documntation
in `waterdata.formats` and `waterdata.views`  for more info. For example you
can save a response as a csv file. 

```
import waterdata

waterdata.formats.save_as_csv(
    'daily_2001_15798700_data.csv', # filename
    waterdata.services.dv.call, # service callback
    sites='15798700',  ## the rest are keyword filter arguments for the callback
    parameterCd='00065,00060,00010', 
    startDt='2001-01-01, endDt='2001-21-31'
    format='rdb'
)
```
