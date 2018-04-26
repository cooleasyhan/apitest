import time
import datetime
from collections import Counter

def run_test(tests):
    t = {}
    t['start_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    start = time.time()

    rst = []
    stat = Counter()

    for obj in tests:
        record = {}

        tmp = obj.run_test()
        record['api_name'] = obj.name
        record['project'] = obj.project.name
        record['meta_data'] = {}
        record['meta_data']['duration'] = round(
            tmp.resp_obj.meta_data['duration'], 3)
        record['meta_data']['status'] = 'sucess' if tmp.validator_success else 'failure'

        record['meta_data']['url'] = tmp.resp_obj.request.url
        record['meta_data']['method'] = tmp.resp_obj.request.method
        record['meta_data']['headers'] = tmp.resp_obj.request.headers
        record['meta_data']['request_body'] = tmp.resp_obj.request.body
        record['meta_data']['status_code'] = tmp.parsed_dict()[
            'status_code']
        record['meta_data']['response_headers'] = tmp.parsed_dict()[
            'headers']
        record['meta_data']['response_body'] = tmp.parsed_dict()['body']
        record['meta_data']['elapsed'] = tmp.resp_obj.elapsed
        record['meta_data']['encoding'] = tmp.resp_obj.encoding
        record['meta_data']['content_size'] = len(tmp.resp_obj.content)

        record['validator'] = {'success':tmp.validator_success}
        record['validator']['detail'] = []
        for validator in tmp.validators:
            record['validator']['detail'].append(validator.to_dict())

        rst.append(record)

        stat['total'] += 1
        if tmp.validator_success:
            stat['successes'] += 1
        else:
            stat['failures'] += 1

    end = time.time()
    t['duration'] = round(end - start, 1)
    return {'stat': stat, 'time': t, 'apis': rst}