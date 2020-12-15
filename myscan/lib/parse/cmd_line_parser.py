# !/usr/bin/env python3
# @Time    : 2020-02-14
# @Author  : caicai
# @File    : cmd_line_parser.py
import argparse
import os
import sys


def cmd_line_parser(argv=None):
    """
    This function parses the command line parameters and arguments
    """

    if not argv:
        argv = sys.argv

    _ = os.path.basename(argv[0])
    usage = "myscan [options]"
    parser = argparse.ArgumentParser(prog='myscan', usage=usage)
    try:
        parser.add_argument("command", choices=("webscan", "hostscan", "reverse"), type=str,
                            help="选择一个模式，接受 webscan , hostscan, reverse  ")
        parser.add_argument("--version", dest="show_version", action="store_true",
                            help="显示版本号并退出")

        conn = parser.add_argument_group('Connect', "At least one of these "
                                                    "options has to be provided to define the target(s)")
        conn.add_argument("--redis", dest="redis", default="@127.0.0.1:6379:0",
                          help="连接redis主机 (e.g. \"--redis password@host:port:db\"),默认: null@127.0.0.1:6379:0")
        common = parser.add_argument_group('Common', "一般配置")
        # 0:debug 蓝色cyan,1:info 绿色，2:error 黄色，3:critical：红色
        common.add_argument("-v", "--verbose", dest="verbose", type=int, default=1, choices=list(range(4)),
                            help="0 ==> Show :all(debug,info,error,critical .1 ==> Show: info,error,critical 2 ==> Show: error,critical"
                                 "3 ==> Show :critical ")
        common.add_argument("--html-output", dest="html_output", default="myscan_result.html",
                            help="默认myscan_result_{num}.html 指定漏洞输出文件")
        common.add_argument("--clean", dest="clean", action="store_true", help="使用此参数可清除Redis所有数据")
        common.add_argument("--check-reverse", dest="check_reverse", action="store_true", help="检测reverse service 是否正常")
        hostscan = parser.add_argument_group('hostscan', "Config hostscan")
        hostscan.add_argument("--input-nmapxml", dest="input_nmapxml", type=str, default=None, help="从nmap -oX 报告输入")
        hostscan.add_argument("--input-nmaptext", dest="input_nmaptext", type=str, default=None, help="从nmap -oN 报告输入")
        hostscan.add_argument("--input-jsonfile", dest="input_jsonfile", type=str, default=None,
                              help="从指定文件格式输入,格式参考 'docs/Class3-hostscan开发指南.md'")
        pocs = parser.add_argument_group('pocs', "Config pocs args and pocs to targets")
        pocs.add_argument("--disable", dest="disable", nargs='+', default=[],
                          help="默认全部开启POC，使用此参数代表禁止的POCS，根据POC文件名包含字符串判断，e.g. --disable xss sqli un_auth，可使用--disable all 代表关闭全部，此时常配合--plugins 使用")
        pocs.add_argument("--enable", dest="enable", nargs='+', default=[],
                          help="默认全部开启POC，使用此参数代表仅开启的POCS，根据POC文件名包含字符串判断，e.g. --enable xss sqli un_auth"
                               "则POC名字包含xss,sqli,un_auth则都会开启,如果同时使用 --enable --disable ， --enable将不会起作用")
        pocs.add_argument("--dishost", dest="dishost", nargs='+',
                          default=["baidu.com", "google.com", "firefox.com", "mozilla.org", "bdstatic.com",
                                   "mozilla.com"],
                          help='使用此参数代表不扫描主机 .默认"baidu.com","google.com","firefox.com","mozilla.org","bdstatic.com","mozilla.com"')
        pocs.add_argument("--host", dest="host", nargs='+', default=None, help="只扫描的主机,主机名不携带端口")
        pocs.add_argument("--level", dest="level", type=int, default=-1,
                          help="再次筛选poc的level等级，可选择-1，1，2，3，分别代表-1:Info 0:Low  1:Medium 2:High 3:Critical，poc的level>=level则保留poc，常用与只测试高危poc，则--level 2，default:-1")

        controller = parser.add_argument_group('Controller', "")
        controller.add_argument("--threads", dest="threads", type=int, default=3, choices=range(1, 21),
                                help="某些POC的线程数，默认3")
        controller.add_argument("--process", dest="process", type=int, default=5, choices=range(1, 61),
                                help="myscan的POC进程数，默认5")
        controller.add_argument("--process-plugins", dest="process_plugins", type=int, default=5, choices=range(1, 10),
                                help="myscan的Plugin进程数，默认5")

        request = parser.add_argument_group('Request', "配置请求参数")
        request.add_argument("--retry", dest="retry", type=int, default=0, help="定义全局request出错后重新尝试请求次数，默认0")
        request.add_argument("--ipv6", dest="ipv6", action="store_true",
                             help="需网络支持ipv6，使用此参数优先ipv6地址,ipv6无记录再使用ipv4地址")

        # request.add_argument("--cookie", dest="cookie", default=None, help="测试越权使用cookie，一般为低权限cookie")
        # request.add_argument("--timeout", dest="timeout", type=int, default=None,
        #                      help="定义全局request的超时，默认使用poc脚本自定义超时或request默认超时")
        plugin = parser.add_argument_group('Plugin', "对流量进行收集的插件")
        plugin.add_argument("--plugins", dest="plugins", nargs='+', default=None, help="指定插件")

        proxy = parser.add_argument_group('Proxy', "Proxy accept: http,https")
        proxy.add_argument("--proxy", dest="proxy", type=str, default=None,
                           help="网络代理,接受host:port形式,e.g:127.0.0.1:8080")

        args = parser.parse_args()

        return args

    except SystemExit:
        # Protection against Windows dummy double clicking
        pass
        raise
