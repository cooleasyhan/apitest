from apitest.handler import BaseHandler
from apitest.request import TestCaseRequest
from apitest.validator import Validator
from apitest.dataformat import TCDataCell

v = Validator(field='status_code', comparator='equals', expect_value=200) 
cell1 = TCDataCell('name','value')
cell2 = TCDataCell('name2','{{ name }}')

request = TestCaseRequest(name='test', method='get', url='http://www.baidu.com',validators=[v],
data=[cell1,cell2])

handler = BaseHandler()

handler.load_middleware()

rst = handler.get_response(request)
# print(rst._validators())

rst.raise_exception()

print(dir(rst))

print(rst.validators[0])
print(rst.parsed_dict().keys())

print(rst.validator_success)
print((rst.resp_obj.request.body))