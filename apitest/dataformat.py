import builtins
import copy
import json
from collections import OrderedDict

import jinja2

from .func import g
from .logger import log_debug


class TCDataCell(object):

    def __init__(self, name, value, data_type='str'):
        self.data_type = data_type
        self.name = name
        self.value = value


class TCDataFormatHandler(object):

    @staticmethod
    def to_dict(arr):
        """
        transfer TCDataCell List to OrderedDict
        """
        # log_debug('handler tc data format')
        tmp = OrderedDict()
        for cell in arr:
            if cell.data_type not in ('jinja2', 'json'):
                _func = getattr(builtins, cell.data_type)
                tmp[cell.name] = _func(cell.value) if cell.value else None

        for cell in arr:
            if cell.data_type in ('jinja2', 'json'):
                template = jinja2.Template(cell.value)
                context = {'f': copy.copy(g)}
                context['v'] = tmp
                tmp[cell.name] = template.render(context)

        for cell in arr:
            if cell.data_type == 'json':
                tmp[cell.name] = json.loads(tmp[cell.name])
                


        tmp = {key: value for key, value in tmp.items() if not key.startswith('_')}
        log_debug('handler tc data format %s' % tmp)

        return tmp
