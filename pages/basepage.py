from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

import config


class BasePage:

    def __init__(self, driver, url):
        self.url = url
        self.driver = driver
        self.mouse = ActionChains(driver)
        self.driver.get(url)

    def find_element_by(self, by, value):
        """ 获取元素"""
        try:
            elem = self.driver.find_element(by=by, value=value)
        except NoSuchElementException:
            print('没有找到相关元素！')
            return False
        else:
            return elem

    @property
    def current_url(self):
        return self.driver.current_url

    @property
    def current_window_handle(self):
        return self.driver.current_window_handle

    @property
    def window_handles(self):
        return self.driver.window_handles

    def switch_to_window(self, handle):
        return self.driver.switch_to.window(handle)

    def get(self, url):
        """ 访问url"""
        self.driver.get(url)

    def click(self, by, value):
        """ 点击元素"""
        self.find_element_by(by, value).click()

    def sent_keys(self, by, value, keys):
        """向元素中输入字符"""
        self.find_element_by(by, value).send_keys(keys)

    def wait_unitl(self, condition, time_out=10, poll_frequency=0.5, message=''):
        """ 显示等待"""
        wait = WebDriverWait(self.driver, time_out, poll_frequency=poll_frequency)
        wait.until(condition, message=message)

    def fullscreen(self):
        self.driver.fullscreen_window()

    def close(self):
        """ 关闭当前窗口"""
        self.driver.close()







