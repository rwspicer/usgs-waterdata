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
    """used to lookup fixed parameter codes

    Parameters
    ----------
    **kwargs:
        keyword arguments defined in waterdata.services.fixed_parameter.filters.

    Returns
    -------
    response:
        format is defined by kwargs['fmt']

    """
    clean_args = globals.validate_args(kwargs, filters, aliases)
    response = generic.call('fixed-parameter', **clean_args)
    return response

