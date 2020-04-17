import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

import config
from utils import format_url


# 获取homepage的内容
resp = requests.request('get', 'https://www.csdn.net/')

# 上方标题栏在是由js文件加载的，是变量tpl的值，获取该js文件内容，并获取该变量值
resp_toolbar = requests.request('get', 'https://csdnimg.cn/public/common/toolbar/js/content_toolbar.js')
re_toolbar = re.compile(r"(?<=var tpl = \').*?</div>(?=\';)", flags=re.DOTALL)
toolbar = re_toolbar.search(resp_toolbar.text).group(0)

soup1 = BeautifulSoup(resp.text, 'html.parser')
soup_toolbar = BeautifulSoup(toolbar, 'html.parser')


class Menus:

    def __init__(self):
        self.var = {}
        self.main()

    def get_menus_of_tb(self):
        # 获取页面上方标题-toolbar元素，页面上方的
        # toolbar的内容是由js加载而来的，先获取js文件内容，再提取出页面代码
        # 返回soup对象
        resp = requests.request('get', 'https://csdnimg.cn/public/common/toolbar/js/content_toolbar.js')
        tb_re = re.compile(r"(?<=var tpl = \').*?</div>(?=\';)", flags=re.DOTALL)
        tb_html = tb_re.search(resp.text).group(0)
        soup = BeautifulSoup(tb_html, 'html.parser')
        menus = soup.find('ul', class_='pull-left left-menu clearfix').find_all('li')[1:]
        for menu in menus:
            text = menu.a.text
            href = format_url(menu.a['href'])
            self.var[text] = href

    def get_menus_of_user(self):

        pass

    def get_menus_of_homepage(self):
        """ 获取主页的标题，位于左侧的一列"""
        resp = requests.request('get', config.HOMEPAGE_URL)
        soup = BeautifulSoup(resp.text, 'html.parser')
        menus = soup.find(id='nav').find_all('a')
        for menu in menus:
            text = menu.text
            href = menu['href']
            parse_href = urlparse(href)
            if parse_href.scheme == parse_href.netloc == '':
                href = config.HOMEPAGE_URL + href
            # self.homepage_menus[text] = href
            self.var[text] = href

    def get_menus_of_edu(self):
        """ 获取博客页的标题"""
        resp = requests.request('get', config.EDU_URL)
        soup = BeautifulSoup(resp.text, 'html.parser')
        pass

    def main(self):
        for funcname in dir(self):
            if funcname.startswith('get_menus_of_'):
                func = getattr(self, funcname)
                varname = funcname[13:]
                self.var = {}
                func()      # 这里如果太长，可以使用多线程
                exec("self." + varname + " = self.var")


m = Menus()




