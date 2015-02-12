# test_http
复制流量进行简单的测试
开启浏览器非缓存模式， 设置http代理  127.0.0.1：8000

1. python http.py #录制流量  CTRL + C  保存请求的数据.
2. python http_handle.py#采用复制的流量跑测试，并根据配置的参数，进行随机的测试。

settings 有一些测试的方法配置
目前不支持提交json的方法的测试。


++++++++++ settings参数的配置+++++++++++++

COOKIE = ''  # 可用   如果设置成空，采用录制时的cookie

 白名单， 匹配白名单里面出现的就取消对该接口的测试。

WHITE_LIST = [r'.*bing.com', r'.*\.(jpg|png|css|js)$'] #


use this rule to random gen http， 定义的产成随机的数据的正则，可以自行添加， 与RULE_HTTP_REQUEST 配合使用（随机定义过的接口的key值）

QUERY_ITEMS = {
    'int_phone': r'^1\d{10}$',  # int11
    'email': r'^[a-z0-9][\w\.]+@[\w\-\.]+\.[\w]+$',
    'int1-3': r'^\d{1,3}$',
    'datetime': r'^\d{4}-\d{1,2}-\d{1-2}$',
}


RULE_HTTP_REQUEST = {'middleman_id': 'int1-3', 'business_id': 'int1-3'}
