from . import generic
from . import globals


filters = {
    'fmt':  globals.default,
    'inline':  globals.default,

}

# aliases 
aliases = {
    'format': 'fmt'
}



def call(**kwargs):
    
    clean_args = globals.validate_args(kwargs, filters, aliases)
    response = generic.call('fixed-parameter', **clean_args)
    return response

