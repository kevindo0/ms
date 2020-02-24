error_dict = {
    'TokenBad': {
        'code': 1103,
        'message': '{info}'
    },
    'MysqlError': {
        'code': 9001,
        'message': 'mysql error'
    }
}


def __init__(self, **kwargs):
    ''' make returned error message'''
    # the replace for json format
    self.message = self.message.format(**kwargs)


def __str__(self):
    return self.message


def __repr__(self):
    return self.message


class HttpException(Exception):
    pass


bases = (HttpException,)
attrs = {
    '__init__': __init__,
    '__str__': __str__,
    '__repr__': __repr__
}

for (error_name, attr) in error_dict.items():
    attrs.update(attr)
    error = type(str(error_name), bases, attrs)
    globals().update({error_name: error})
