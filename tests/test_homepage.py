import unittest
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.support import expected_conditions as EC
import inspect


from pages.homepage import Homepage
import config
from menus import Menus
from utils import format_url


def setUpModule():
    print('我有没有作用')


def get_menu():
    """ 返回test_links_of_*测试函数的名称后缀"""
    funcname = inspect.stack()[2].function
    return funcname[14:]


class TestHomepage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = Chrome(config.CHROMEDRIVER)  # chromedriver的文件地址
        url = config.HOMEPAGE_URL
        cls.session = Homepage(driver=cls.driver, url=url)
        cls.session.fullscreen()
        cls.m = Menus()

    def setUp(self):
        pass

    def _test_links_in_dict(self, origin_url=None):
        """
        text_links: 标签名及其对应的链接
        origin_url: 所要测试的网页原始url
        测试{text: links}格式的字典中，所有text所对应的元素点击是否跳转到links
        如果链接打开了新窗口，切换窗口获取元素后，关闭窗口并切回原窗口
        """
        menu_name = get_menu()
        text_links = getattr(self.m, menu_name)
        for k, v in text_links.items():
            with self.subTest(text=k, link=v):
                current_url = format_url(self.session.current_url)
                target_url = format_url(v)
                window_handle = self.session.current_window_handle
                if urlparse(current_url).netloc != urlparse(origin_url).netloc:
                    # 如果跳转到了其他域名的页面，回到指定页面
                    self.session.get(origin_url)
                self.session.click(By.LINK_TEXT, k)
                if len(self.session.window_handles) > 1:
                    # 点击打开了新窗口时的情况
                    windows = self.session.window_handles
                    windows.remove(window_handle)
                    self.session.switch_to_window(windows[0])
                    result_url = format_url(self.session.current_url)
                    self.session.close()
                    self.session.switch_to_window(window_handle)
                elif target_url == origin_url == self.session.current_url:
                    # 点击跳转到相同的页面
                    result_url = self.session.current_url
                else:
                    self.session.wait_unitl(EC.url_changes(origin_url))
                    result_url = format_url(self.session.current_url)
                self.assertEqual(result_url, format_url(v))

    def test_homepage_logo(self):
        """ 测试主页logo是否是跳转到首页"""
        self.session.click(By.XPATH, '//a[@title="CSDN首页"]')
        self.assertEqual(self.session.url, config.HOMEPAGE_URL)

    def test_links_of_tb(self):
        """ 测试上方固定标题栏左半部分的链接"""
        self._test_links_in_dict(config.HOMEPAGE_URL)

    def test_links_of_homepage(self):
        """ 测试主页左侧竖列各链接"""
        self._test_links_in_dict(config.HOMEPAGE_URL)

    def test_links_of_edu(self):
        """ 测试edu页的顶端标签"""
        self._test_links_in_dict(config.EDU_URL)

    def test_links_of_user(self):
        """ 测试用户下拉菜单的各链接"""
        pass

    def tearDown(self):
        """ 每一个用例执行完毕后，跳转回首页"""
        self.session.get(config.HOMEPAGE_URL)


# def load_tests(loader, standard_test, pattern):
#     case = TestHomepage('test_links_in_toolbar_left')
#     case.setUpClass()
#     return case


if __name__ == '__main__':
    unittest.main(argv=['', '-v'], exit=False)
