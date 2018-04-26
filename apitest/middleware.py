from apitest.request import TC_DATA_FORMAT, REQUESTS_DATA_FORMAT
from apitest.comparator import comparators
from apitest.utils import import_string
from functools import partial
from apitest.response import TestCaseResponse
from requests.sessions import *
from apitest.dataformat import TCDataCell, TCDataFormatHandler
from .logger import log_debug

class MiddlewareMixin:
    def __init__(self, get_response=None):
        self.get_response = get_response
        super().__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response


class TCDataFormatMiddleware(MiddlewareMixin):
    def process_request(self, request):
        log_debug('Begin TCDataFormatMiddleware')
        log_debug(str(request.data))
        log_debug(str(request.json))
        log_debug(str(request.headers))

        def _handler(fields):
            if isinstance(fields, (list, tuple)):
                if len(fields) >= 1:
                    if isinstance(fields[0], TCDataCell):

                        return TCDataFormatHandler.to_dict(fields)
            return fields

        request.data = _handler(request.data) if request.data else request.data
        request.json = _handler(request.json) if request.json else request.json
        request.headers = _handler(
            request.headers) if request.headers else request.headers


class ValidatorMiddleware(MiddlewareMixin):


    def process_response(self, request, response):
        log_debug('Validators: %s' % str(request.validators))
        if not hasattr(request, 'validators') or not isinstance(response, TestCaseResponse):
            return response

        tmp = True
        for v in request.validators:
            check_value = response.extract_field(v.field)
            if not v.check(check_value):
                tmp = False

        response.validators = request.validators
        response.validator_success = tmp
        return response


class LocustMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # pass validator
        request.validators = []


MIDDLEWARES = [
    'apitest.middleware.ValidatorMiddleware',
    'apitest.middleware.TCDataFormatMiddleware',
]
