# -*- coding: utf-8 -*-

import socket
import thread
import select
import json
import time
# this come from the internet http://code.google.com/p/python-proxy/, fix
# for test my project
__version__ = '0.1.0 Draft 1'
BUFLEN = 8192
VERSION = 'Python Proxy/' + __version__
HTTPVER = 'HTTP/1.1'
__fixauth__ = 'tesla.yang'

http_request_data = None


class ConnectionHandler:

    def __init__(self, connection, address, timeout):
        self.client = connection
        self.client_buffer = ''
        self.timeout = timeout
        self.method, self.path, self.protocol = self.get_base_header()
        if self.method == 'CONNECT':
            self.method_CONNECT()
        elif self.method in ('OPTIONS', 'GET', 'HEAD', 'POST', 'PUT',
                             'DELETE', 'TRACE'):
            self.method_others()
        self.client.close()
        self.target.close()

    def get_base_header(self):
        while 1:
            self.client_buffer += self.client.recv(BUFLEN)
            end = self.client_buffer.find('\n')
            if end != -1:
                break
        # print '%s' % self.client_buffer[:end]  # debug
        data = (self.client_buffer[:end + 1]).split()
        self.client_buffer = self.client_buffer[end + 1:]
        return data

    # def method_CONNECT(self):
    #     self._connect_target(self.path)
    #     print self.path
    #     self.client.send(HTTPVER + ' 200 Connection established\n' +
    #                      'Proxy-agent: %s\n\n' % VERSION)
    #     self.client_buffer = ''
    #     self._read_write()

    def method_others(self):
        self.path = self.path[7:]
        i = self.path.find('/')
        host = self.path[:i]
        path = self.path[i:]
        self._connect_target(host)
        request_data = '%s %s %s\n' % (
            self.method, path, self.protocol) + self.client_buffer

        request_key = self.path + '|%s' % int(time.time())
        print request_key
        http_request_data[request_key] = request_data  # http request

        self.target.send(request_data)
        self.client_buffer = ''
        self._read_write()

    def _connect_target(self, host):
        i = host.find(':')
        if i != -1:
            port = int(host[i + 1:])
            host = host[:i]
        else:
            port = 80
        (soc_family, _, _, _, address) = socket.getaddrinfo(host, port)[0]
        self.target = socket.socket(soc_family)
        self.target.connect(address)

    def _read_write(self):
        time_out_max = self.timeout / 3
        socs = [self.client, self.target]
        count = 0
        while 1:
            count += 1
            (recv, _, error) = select.select(socs, [], socs, 3)
            if error:
                break
            if recv:
                for in_ in recv:
                    data = in_.recv(BUFLEN)
                    if in_ is self.client:
                        if data:
                            url = data[:data.find('\n')].split()[1]
                            request_key = url + '|%s' % int(time.time())
                            http_request_data[request_key] = data
                        out = self.target
                    else:
                        out = self.client
                    if data:
                        out.send(data)
                        count = 0
            if count == time_out_max:
                break


def start_server(host='localhost', port=8000, IPv6=False, timeout=10,
                 handler=ConnectionHandler):
    global http_request_data
    print 'please select 1: to start new log, \r\nselect 2 : to continue log'
    select_id = raw_input('------>')
    if select_id == '1':
        print 'start new log'
        http_request_data = {}
    else:
        with open('./http_request_json.json', 'r') as f:
            data = f.read()
            if len(data) > 1:
                http_request_data = json.loads(data)
    if IPv6 is True:
        soc_type = socket.AF_INET6
    else:
        soc_type = socket.AF_INET
    soc = socket.socket(soc_type)
    soc.bind((host, port))
    print "Serving on %s:%d." % (host, port)  # debug
    soc.listen(0)
    try:
        while 1:
            # print http_request_data
            thread.start_new_thread(handler, soc.accept() + (timeout,))
    except KeyboardInterrupt:
        print 'will save data, please wait'
        time.sleep(3)
        json_http_data = json.dumps(http_request_data)
        with open('./http_request_json.json', 'w') as f:
            f.write(json_http_data)


if __name__ == '__main__':

    start_server()
