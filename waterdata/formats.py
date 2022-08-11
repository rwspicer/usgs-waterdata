"""

"""
from pandas import DataFrame, read_table
from io import StringIO

def convert_to_DataFrame(text):
    table = read_table(StringIO(text), comment='#')
    table = table[1:].reset_index(drop=True)
    return table

def parse_header(text):
    header_lines = [ l for l in text.split('\n') if len(l) >0 and l[0] == '#']
    return '\n'.join(header_lines)

def save_as_rdb(filename, callback, **kwargs):
    kwargs['format'] = 'rdb'
    response = callback(**kwargs)
    with open(filename, 'w') as fd:
        fd.write(response)

def save_as_csv(filename, callback, **kwargs):
    
    kwargs['format'] = 'rdb'
    response = callback(**kwargs)
    
    header =  parse_header(response)
    table = convert_to_DataFrame(response)
    with open(filename, 'w') as fd:
        fd.write(header)
        fd.write('\n')
    table.to_csv(filename, mode='a', index=0)


