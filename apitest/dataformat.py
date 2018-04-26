import builtins
import jinja2
from collections import OrderedDict
from .logger import log_debug
import copy
from .func import g 
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
            if cell.data_type != 'jinja2':
                _func = getattr(builtins, cell.data_type)
                tmp[cell.name] = _func(cell.value)

        for cell in arr:
            if cell.data_type == 'jinja2':
                template = jinja2.Template(cell.value)
                context = copy.copy(g)
                context.update(tmp)
                tmp[cell.name] = template.render(context)

        log_debug('handler tc data format %s' % tmp) 
        return tmp
