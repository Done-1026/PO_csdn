import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pages.homepage import Homepage
import config


driver = Chrome(r'/Volumes/D/pythoncode/webdriver/chromedriver')
# url = config.HOMEPAGE_URL
url = config.EDU_URL

#driver.implicitly_wait(30)      # 设置隐式等待时长，超过该时间仍未找到元素则跳过操作

page = Homepage(driver=driver, url=url)




