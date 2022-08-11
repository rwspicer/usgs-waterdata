from . import generic
from . import globals

filters = {
    'stat_code': lambda a, oa: all([len(sc) == 5 for sc in a.split(',')]),
    'format': lambda a, oa: a in ['dict', 'json']
}


# aliases 
aliases = {
    'stat_codes': 'stat_code'
}


def parse_response(html, url):

    content = html.find('div', {"id":"content"})
    stats_rows = content.find('table').find_all('tr')

    stats = {}

    for row in stats_rows:
        cols = row.find_all('td')
        if len(cols) == 0:
            continue
        stats[cols[0].text] = {'name': cols[1].text, 'description': cols[2].text}
        
    return stats

def call(**kwargs):


    clean_args = globals.validate_args(kwargs, filters, aliases)
    if clean_args is None:
        return None

    if 'format' in clean_args:
        format = clean_args['format'] 
        del(clean_args['format'])
    else:
        format = 'dict'
    response = generic.html('stat-cd', parse_response)

    # response = parse_response(response)

    stats = {}

    for stat in clean_args['stat_code'].split(','):
        if stat in response:
            stats[stat] = response[stat]
      
    return stats



