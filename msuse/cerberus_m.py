from cerberus import Validator
from cerberus.errors import BasicErrorHandler

class CustomErrorHandler(BasicErrorHandler):
    def __init__(self, schema):
        self.schema = schema

    def _format_message(self, field, error):
        # 返回错误信息
        _error = self.schema[field].get('meta', {}).get('error')
        if _error is None:
            _error = super(CustomErrorHandler, self)._format_message(field, error)
        return _error

schema = {'id': {'type': 'string', 'meta': {'error': '请入id'}},
          'name': {'type': 'string', 'required': True}}
v = Validator(schema, error_handler=CustomErrorHandler(schema))
d = {'id': 90}
v.validate(d)
print(v.errors)
# {'id': ['请入id'], 'name': ['required field']}
