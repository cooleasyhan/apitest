import requests
from apitest.middleware import MIDDLEWARES
from apitest.utils import import_string
from functools import wraps
from apitest.response import TestCaseResponse, ResponseObject
from apitest.logger import log_debug
import time


class BaseHandler:

    def load_middleware(self):
        self._exception_middleware = []
        handler = self._get_response
        for middleware_path in MIDDLEWARES:
            middleware = import_string(middleware_path)
            mw_instance = middleware(handler)

            if hasattr(mw_instance, 'process_exception'):
                self._exception_middleware.append(
                    mw_instance.process_exception)
            handler = mw_instance

        self._middleware_chain = handler

    def _get_response(self, request):
        if hasattr(request, 'client'):
            requests_obj = request.client
        else:
            requests_obj = requests
        # raise Exception('test')

        log_debug('Send %s ' % str(request.prepare()))
        start = time.time()
        rst = requests_obj.request(
            **request.prepare())
        rst.meta_data = {'duration': time.time() - start}

        return ResponseObject(rst)

    def get_response(self, request):
        response = self._middleware_chain(request)
        log_debug('Response: %s' % str(response.parsed_dict()))
        return response
