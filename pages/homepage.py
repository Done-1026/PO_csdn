from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from .basepage import BasePage


class Homepage(BasePage):

    def has_logined(self):
        return not bool(self.find_element_by(By.LINK_TEXT, '登录/注册'))

    def to_loginpage(self):
        self.click(By.LINK_TEXT, '登录/注册')

    def login_in_username(self, user, pwd):
        """
        使用用户名及密码登录
        由于使用selenium登录被csdn网页识别，因此滑块验证无法通过,
        目前找到识别selenium的js文件为122.js,因只考虑测试而非爬虫，在此略过
        """
        self.click(By.LINK_TEXT, '账号密码登录')
        self.sent_keys(By.NAME, 'all', user)
        self.sent_keys(By.NAME, 'pwd', pwd)
        self.click(By.XPATH, '//button[@class="btn btn-primary"]')
        btn_slide = self.find_element_by(By.ID, 'nc_1_n1z')
        if btn_slide:
            self.mouse.drag_and_drop_by_offset(btn_slide, 300, 0)


    def logout(self):
        pass







