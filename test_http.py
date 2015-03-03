# -*- coding: utf-8 -*-


import socket
# import json
from settings import WHITE_LIST
from settings import RULE_HTTP_REQUEST, QUERY_ITEMS
from rstr import xeger
import re


class TestHttpServer(object):

    """docstring for TestHttpServer"""

    def __init__(self, dict_http_data):
        self.data = dict_http_data
        self.bad_request = []
        self.native_bad_request = []

        self.pre_handle = None

    def add_handle(self, handle):
        self.pre_handle = handle

    def _connect_server(self, server_host, port, data):
        conn = socket.socket(socket.AF_INET)
        conn.connect((server_host, int(port)))
        conn.send(data)
        return conn.recv(1024)

    def process_data(self):
        for k, raw_request in self.data.items():
            is_first = True
            request = Request(raw_request)
            host, port = self._host_port(k)
            is_pass = None
            for re_rule in WHITE_LIST:
                if re.search(re_rule, self.path):
                    is_pass = True

            if is_pass:
                continue

            if self.pre_handle:
                raw_request = self.pre_handle(
                    request).raw_data  # 前置处理，目前处理cookie

            for i in range(5):
                if is_first:
                    print 'start native  HTTP request'
                    response_data = self._connect_server(
                        host, port, raw_request)
                    if not self._process_response(response_data):
                        print 'there is some error', k
                        self.native_bad_request.append(k)
                    is_first = False
                    continue
                else:
                    print 'start random HTTP request'
                    new_request_object = Request(raw_request)
                    raw_request = gen_random_query(new_request_object)

                    response_data = self._connect_server(
                        host, port, raw_request)
                    if not self._process_response(response_data):
                        self.bad_request.append(k)

        return self.bad_request

    def _process_response(self, response_data):
        # print response_data
        # print 'this is ', response_data.find('\n')
        protocal, response_code, k = response_data[
            :response_data.find('\n')].split()[:3]
        if response_code in ['200', '304']:
            return True

    def _host_port(self, path):
        if 'http://' in path:
            path = path.replace('http://', '')
        new_path = path.split('|')[0]  # www.tango.com/xxx//
        self.path = new_path
        end = new_path.find('/')
        host = new_path[:end]
        if ':' in host[7:]:
            return host.split(':')
        return host, 80


import urlparse


class Request(object):

    """docstring for Request"""

    def __init__(self, raw_data):

        self.raw_data = raw_data
        self.parse_http()

        self.read_first_line = self.http_header.split('\n')[0]

        self.commond, self.path, self.protocal = self.read_first_line.split()

        self.get_param = {}
        self.post_param = {}

    def parse_http(self):
        parse_list = self.raw_data.split('\r\n\r\n')
        if len(parse_list) > 1:
            self.http_header = parse_list[0]
            self.http_body = parse_list[1]
        else:
            self.http_header = parse_list[0]
        return parse_list

    def http_param(self):
        if self.commond == "GET":
            self.parse = urlparse.urlparse(self.path)
            query = self.parse.query
            self.get_param = urlparse.parse_qs(query)
            return self.get_param
        if self.commond == "POST":
            self.post_param = urlparse.parse_qs(
                self.http_body.encode('unicode-escape'))
            print self.post_param
            return self.post_param


def gen_random_query(request_object):
    query_data = request_object.http_param()
    if len(query_data) == 0:
        return request_object.raw_data
    import urllib

    for k, v in query_data.items():
        if k in RULE_HTTP_REQUEST.keys():
            v_re_rules = QUERY_ITEMS[RULE_HTTP_REQUEST[k]]
            random_str = xeger(v_re_rules)
            query_data[k] = random_str
        elif isinstance(v, list):
            query_data[k] = v[0]
    url_query = urllib.urlencode(query_data)
    if request_object.commond == 'GET':
        path = request_object.path
        new_get_url = path[:path.find('?') + 1] + url_query

        new_first_line = 'GET %s HTTP/1.1\n' % new_get_url
        get_url_compile = re.compile(r'GET .*\n')
        return re.sub(get_url_compile, new_first_line, request_object.raw_data)

    if request_object.commond == 'POST':
        new_length = 'Content-Length: %s\r\n' % (len(url_query))
        http_header = re.sub(
            r'Content-Length: \d*\r\n', new_length, request_object.http_header)
        return '%s\r\n\r\n%s' % (http_header, url_query)


def creat_test(data):
    return TestHttpServer(data)

if __name__ == '__main__':
    with open('./http_request_json.json') as f:
        import json
        data = json.loads(f.read())
    result = creat_test(data).process_data()
    if len(result) > 0:
        print 'this is error url', result
    else:
        print 'sahua xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx   no    error 兴奋吧少年no error'

    # pass
