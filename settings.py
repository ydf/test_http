# -*- coding: utf-8 -*-


# if None , use the default
# 'Cookie: sessionid=xxasfpgq8899g0ygh3atdbqfjb6ul1be\r\n'
COOKIE = ''  # 可用

# eg: www.qq.com:80,  if None , use the default 目前不用配置。
WHITE_LIST = [r'.*bing.com', r'.*\.(jpg|png|css|js)$']


# use this rule to random gen http
QUERY_ITEMS = {
    'int_phone': r'^1\d{10}$',  # int11
    'email': r'^[a-z0-9][\w\.]+@[\w\-\.]+\.[\w]+$',
    'int1-3': r'^\d{1,3}$',
    'datetime': r'^\d{4}-\d{1,2}-\d{1-2}$',
}


RULE_HTTP_REQUEST = {'middleman_id': 'int1-3', 'business_id': 'int1-3'}
