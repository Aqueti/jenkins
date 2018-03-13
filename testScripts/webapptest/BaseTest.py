from selenium.webdriver import ChromeOptions
from selenium import webdriver
import unittest
import time


class BaseTest(unittest.TestCase):
    driver = None
    browser = "chrome"

    log_path = '/home/astepenko/Pictures/tests/base_test.txt'
    screenshot_path = '/home/astepenko/Pictures/tests/test.png'

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
        time.sleep(1)
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

    def make_screenshot(self, path=""):
        if path == "":
            self.driver.save_screenshot(self.screenshot_path)
        else:
            self.driver.save_screenshot(path)
