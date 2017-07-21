#!/user/bin python
# -*- coding:utf-8 -*- 
# Author:Bing
# Contact:amazing_bing@outlook.com
# DateTime: 2016-12-21 11:46:49
# Description:  coding 

import sys
sys.path.append("..")

from common.captcha import Captcha
from common.wukong_Func import *
from common.wukong_TypeCheck import *

#target,result=[]
class WuKong(object):
    def __init__(self,  target = ""):
        # 类的参函数和输出格式
        # target 扫描目标格式验证，结果返回[]
        self.target = target
        self.timeout = 0.5
        self.site = 'http://searchdns.netcraft.com'
        self.result = {
        "bug_author" : "Bing",
        "bug_name" : "Netcraft subdomain api",
        "bug_summary" : "Subdomain search", 
        "bug_level" : "Normal" , 
        "bug_detail" : [] ,
        "bug_repair" : "none"
        }

    def run(self):
        #验证数据格式
        if is_domain(self.target) == False :
            return 0
        target = '.'.join(self.target.split(".")[1:])
        #执行获取结果
        try:
            self.cookie = self.get_cookie().get('cookie')
            url = '{0}/?restriction=site+contains&position=limited&host=.{1}'.format(
                self.site, target )
            r = http_request_get(url, custom_cookie=self.cookie)
            self.parser(r.text)
        except Exception, e:
            pass

    def parser(self, response):
        npage = re.search('<A href="(.*?)"><b>Next page</b></a>', response)
        if npage:
            for item in self.get_subdomains(response):
                if is_domain(item):
                    self.result["bug_detail"].append(item.encode('gbk'))
            nurl = '{0}{1}'.format(self.site, npage.group(1))
            r = http_request_get(nurl, custom_cookie=self.cookie)
            time.sleep(3)
            self.parser(r.text)
        else:
            for item in self.get_subdomains(response):
                if is_domain(item):
                    self.result["bug_detail"].append(item.encode('gbk'))

    def get_subdomains(self, response):
        _regex = re.compile(r'(?<=<a href\="http://).*?(?=/" rel\="nofollow")')
        domains = _regex.findall(response)
        for sub in domains:
            yield sub

    def get_cookie(self):
        try:
            cmdline = 'phantomjs ph_cookie.js'
            run_proc = subprocess.Popen(cmdline,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            (stdoutput,erroutput) = run_proc.communicate()
            response = {
                'cookie': stdoutput.rstrip(),
                'error': erroutput.rstrip(),
            }
            return response
        except Exception, e:
            return {'cookie':'', 'error': str(e)}

# netcraft = WuKong(target ='www.nknu.edu.tw')
# netcraft.run()
# print netcraft.result 
