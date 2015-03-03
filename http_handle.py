# -*-coding:utf-8-*-
""" this is simply parse http header and body, dont support 0101 body"""


import re
import json

from settings import COOKIE
from test_http import creat_test
with open('./http_request_json.json') as f:
    data = json.loads(f.read())
result = creat_test(data)


@result.add_handle
def sub_cookie(reuqest_object):  # this is replace cookie that what u want to
    if len(COOKIE) > 0:
        cookie_compile = re.compile(r'Cookie: .*\r\n')
        reuqest_object.raw_data = re.sub(
            cookie_compile, COOKIE, reuqest_object.raw_data)
    return reuqest_object

if __name__ == '__main__':
    result.process_data()
    if len(result.bad_request) > 0:
        print 'there is some error by random data', result.bad_request
        print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX以上随机的产生的结果，可能不是预料的,我是卖夢的分割线XXXXXXXXXXXXXXXXXXX'
    if len(result.native_bad_request) > 0:
        print 'there is some error', result.native_bad_request
    if len(result.native_bad_request) == len(result.bad_request) == 0:
        print 'this is no error, thanks'
