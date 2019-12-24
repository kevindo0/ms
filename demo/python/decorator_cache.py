import json

file_name = '/tmp/demo.dat'

def cache(seconds=10):
    def outer(func):
        def innter(*args, **kwargs):
            key = 'key-'
            for item in args:
                key += item
            for _, val in kwargs.items():
                key += val
            print(args, kwargs)
            print(key, seconds)
            with open(file_name) as f:
                f.read
            res = func(*args, **kwargs)
            return res
        return innter
    return outer

@cache(20)
def accounts(fbid):
    print('accounts:', fbid)
    return 'hello'

if __name__ == '__main__':
    accounts(fbid='me')
