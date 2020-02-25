from wtforms import Form, validators
from wtforms import StringField, IntegerField, SelectField
from wtforms import ValidationError
from apps.utils import exceptions


class GetForm(Form):
    name = StringField('策略名称', [validators.DataRequired(message='请填写策略名称')])
    script = StringField('策略脚本', [validators.Optional()])
    count = IntegerField('数量', [validators.DataRequired(message='请填写数据')])
    
    def __init__(self, *args, **kwagrs):
        super(GetForm, self).__init__(*args, **kwagrs)
        if not self.validate():
            raise exceptions.ParamsError(info=self.errors)

    def validate_count(form, field):
        if int(field.data) < 15:
            raise ValidationError("值必须大于15")
