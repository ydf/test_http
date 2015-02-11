# test_http
复制流量进行简单的测试
开启浏览器非缓存模式， 设置http代理  127.0.0.1：8000

1. python http.py #录制流量  CTRL + C  保存请求的数据.
2. python http_handle.py#采用复制的流量跑测试

settings 有一些测试的方法配置