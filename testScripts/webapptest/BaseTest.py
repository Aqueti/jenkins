from selenium.webdriver import ChromeOptions
from selenium import webdriver
import unittest


class BaseTest(unittest.TestCase):
    driver = None
    browser = "chrome"

    _cnt = 0

    @property
    def screenshot_path(self):
        self._cnt = self._cnt + 1
        return '/home/astepenko/Pictures/tests/' + self.script_name + "_" + str(self._cnt) + ".png"

    def __call__(self, *args, **kwargs):
        self.script_name = self.__class__.__name__ + "_" + self.__dict__['_testMethodName']
        self.log_path = '/home/astepenko/Pictures/tests/' + self.script_name + ".txt"

        super(BaseTest, self).__call__(*args, **kwargs)

    def setUp(self):
        if self.browser == "chrome":
            #opts = ChromeOptions()
            #opts.add_experimental_option("detach", True)
            #self.driver = webdriver.Chrome(chrome_options=opts)
            self.driver = webdriver.Chrome()
        elif self.browser == "ff":
            self.driver = webdriver.Firefox()
        else:
            pass

        self.driver.maximize_window()

    def tearDown(self):
        self.driver.close()

    def navigate_to(self, url=""):
        if url == "back":
            self.driver.back()
        elif url == "forward":
            self.driver.forward()
        else:
            if url == "":
                self.driver.get(self.page_url)
            else:
                self.driver.get(url)
