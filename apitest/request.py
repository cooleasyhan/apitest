import requests
from requests.hooks import default_hooks
from requests.models import PreparedRequest, Request

TC_DATA_FORMAT = "TC"
REQUESTS_DATA_FORMAT = 'REQUESTS'


class RequestObject(object):
    pass


class TestCaseRequest(RequestObject):

    def __init__(self, name, attr1=None, attr2=None, attr3=None,  method=None, url=None, headers=None, files=None, data=None,
                 params=None, auth=None, cookies=None, hooks=None, json=None, validators=None, client=None):
        data = [] if data is None else data
        files = [] if files is None else files
        headers = {} if headers is None else headers
        params = {} if params is None else params
        hooks = {} if hooks is None else hooks
        validators = [] if validators is None else validators

        self.hooks = default_hooks()
        for (k, v) in list(hooks.items()):
            self.register_hook(event=k, hook=v)

        self.method = method
        self.url = url
        self.headers = headers
        self.files = files
        self.data = data
        self.json = json
        self.params = params
        self.auth = auth
        self.cookies = cookies

        self.validators = validators
        self.name = name
        self.attr1 = attr1
        self.attr2 = attr2
        self.attr3 = attr3
        self.client = client or requests

    def __repr__(self):
        return '<TestCaseRequest [%s]>' % (self.name)

    def prepare(self):
        return {
            "method": self.method,
            "url": self.url,
            "headers": self.headers,
            "files": self.files,
            "data": self.data,
            "json": self.json,
            "params": self.params,
            "auth": self.auth,
            "cookies": self.cookies,
            "hooks": self.hooks}

    # def _parse_data(self):
    #     tmp = OrderedDict()
    #     for f in self.config_data:
    #         if f['data_type'] != 'jinja2':
    #             _func = getattr(builtins, f['data_type'])
    #             tmp[f['name']] = _func(f['value'])

    #     for f in fields:
    #         if f['data_type'] == 'jinja2':
    #             template = Template(f['value'])
    #             context = copy.copy(g)
    #             context.update(tmp)
    #             tmp[f['name']] = template.render(context)

    #     return tmp

    # def _parse_validator(self):
    #     tmp = OrderedDict()

    #  def validate(self, data):
    #     try:
    #         value = data
    #         for field in self.field_name.split('/'):
    #             value = data[field]
    #         if self.comparator == 'exists':
    #             return True

    #     except KeyError:
    #         if self.comparator == 'not_exists':
    #             return True
    #         raise

    #     func = getattr(builtins, self.data_type)
    #     value = func(value)
    #     expected_value = func(self.expected)

    #     comparator_func = getattr(comparator, self.comparator)
    #     try:
    #         comparator_func(value, expected_value)
    #     except AssertionError:
    #         return False

    #     return True, value, expected_value, self.comparator
