from apitest.utils import import_string
from apitest.comparator import get_comparator
from functools import partial
import builtins


from .logger import log_debug


class Validator(object):
    def __init__(self,  field,  comparator, expect_value, name=None, field_type=None):
        self.field = field
        self._field_type = field_type
        self.comparator = comparator
        self.expect_value = expect_value
        self.name = name or '%s %s %s' % (
            str(field), str(comparator), str(expect_value))

        self.result = None

    def __str__(self):
        return self.name + ' - ' + str(self.result)

    @property
    def field_type(self):
        return getattr(builtins, self._field_type) if self._field_type else type(self.expect_value)

    @property
    def _method(self):
        tmp = import_string('apitest.comparator.' +
                            get_comparator(self.comparator))

        return partial(tmp, expect_value=self.field_type(self.expect_value))

    def check(self, check_value):

        try:
            self._method(check_value=self.field_type(check_value))

            log_debug('check_value %s comparator %s expect_value %s, True' %
                      (str(check_value), self.comparator, str(self.expect_value)))
            self.result = True
            return True
        except AssertionError:

            log_debug('check_value %s comparator %s expect_value %s, False' %
                      (str(check_value), self.comparator, str(self.expect_value)))
            self.result = False
            return False
