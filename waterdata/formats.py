"""
Formats 
-------

Functions for converting data formats
"""
from io import StringIO
from pandas import read_table
import yaml

def rdb_to_DataFrame(text):
    """Converts USGS rdb format to DataFrame

    Parameters
    ----------
    text: str
        rdb file text
    
    Returns
    -------
    DataFrame
    """
    table = read_table(StringIO(text), comment='#')
    table = table[1:].reset_index(drop=True)
    return table

def rdb_to_header(text):
    """Parses rdb header info. Header linses start wuith '#'
    
    Parameters
    ----------
    text: str
        rdb file text
    
    Returns
    -------
    str
    """
    header_lines = [ l for l in text.split('\n') if len(l) >0 and l[0] == '#']
    return '\n'.join(header_lines)

def save_as_rdb(filename, callback, **kwargs):
    """Gets a NWIS rdb file and saves it directly as a rdb file
    
    Parameters
    ----------
    filename: path
        name and location of file to save
    callback: function
        web service call function 
    kwargs: dict
        keyword arguments for callback
    """
    kwargs['format'] = 'rdb'
    if type(callback) is str:
        response = callback
    else:
        response = callback(**kwargs)
    with open(filename, 'w') as fd:
        fd.write(response)

def save_as_csv(filename, callback, **kwargs):
    """Gets a NWIS rdb file and saves it directly as a csv file
    
    Parameters
    ----------
    filename: path
        name and location of file to save
    callback: function
        web service call function 
    kwargs: dict
        keyword arguments for callback
    """
    kwargs['format'] = 'rdb'
    if type(callback) is str:
        response = callback
    else:
        response = callback(**kwargs)
    
    header =  rdb_to_header(response)
    table = rdb_to_DataFrame(response)
    with open(filename, 'w') as fd:
        fd.write(header)
        fd.write('\n')
    table.to_csv(filename, mode='a', index=0)


def to_yaml(callback, **kwargs):
    """converts a NWIS service call that supports the "dict" format to 
    yaml string
    
    Parameters
    ----------
    callback: function
        web service call function 
    kwargs: dict
        keyword arguments for callback

    Returns 
    -------
    str
    """

    ## define fomrats supported
    kwargs['format'] = kwargs['format'] if 'format' in kwargs else "dict"
    data = callback(**kwargs)
    return yaml.dump(data, sort_keys=False)

def save_as_yaml(filename, callback, **kwargs):
    """Saves a NWIS service call that supports the "dict" format to 
    yaml file
    
    Parameters
    ----------
    filename: path
         name and location of file to save
    callback: function
        web service call function 
    kwargs: dict
        keyword arguments for callback
    """
    with open(filename, 'w') as fd:
        fd.write(to_yaml(callback, **kwargs))
