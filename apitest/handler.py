import time
from functools import wraps

import requests
from requests.api import request

from apitest.logger import log_debug
from apitest.middleware import MIDDLEWARES
from apitest.response import ResponseObject, TestCaseResponse, ExceptionResponse
from apitest.utils import import_string


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
        try:
            response = self._middleware_chain(request)
            log_debug('Response: %s' % str(response.parsed_dict()))
            return response
        except Exception as e:
            return ExceptionResponse(request, e)
