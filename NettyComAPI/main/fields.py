from .customobjects import BankDetails
from django.db import models

#create customfield for BankDetails here
class BankDetailsField(models.Field):
    description = "BankDetails"
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 100
        super().__init__(*args, **kwargs)
    def db_type(self, connection):
        return 'varchar(%s)' % self.max_length
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return BankDetails(*value.split(','))
    def to_python(self, value):
        if isinstance(value, BankDetails):
            return value
        if value is None:
            return value
        return BankDetails(*value.split(','))
    def get_prep_value(self, value):
        if value is None:
            return value
        return "{},{}".format(value.account_number, value.bank_name)
    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)
    def deconstruct(self):
        #create deconstruct method
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs