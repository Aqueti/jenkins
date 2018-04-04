from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import ChromeOptions
from selenium import webdriver
import pytest
import datetime
import os
#import pymongo


class BaseTest(object):
    driver = None
    browser = "chrome"

    script_name = ""
    start_time = ""
    end_time = ""
    result = ""
    base_dir = ""
    log_path = ""

    mongo_client = None

    @property
    def screenshot_path(self):
        return '{0}/{1}_{2}.png'.format(self.base_dir, self.script_name, datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))

    @property
    def failure_exception(self):
        class BaseTestFailureException(AssertionError):
            def __init__(self, *args, **kwargs):
                return super(BaseTestFailureException, self).__init__(*args, **kwargs)

            self.result = "FAILED"
        try:
            self.driver.save_screenshot(self.screenshot_path)
        except Exception as e:
            pass

        BaseTestFailureException.__name__ = AssertionError.__name__

        return BaseTestFailureException

    def __call__(self, *args, **kwargs):
        super(BaseTest, self).__call__(*args, **kwargs)

    def setup_method(self, method):
        if self.browser == "chrome":
            opts = ChromeOptions()
            opts.add_experimental_option("detach", True)
            caps = DesiredCapabilities.CHROME
            caps["pageLoadStrategy"] = "normal"  # none
            self.driver = webdriver.Chrome(desired_capabilities=caps)  # chrome_options=opts
        elif self.browser == "ff":
            caps = DesiredCapabilities.FIREFOX
            self.driver = webdriver.Firefox()
        else:
            pass

        self.driver.maximize_window()

        self.script_name = self.__class__.__name__ + "_" + method.__name__

        self.start_time = datetime.datetime.now()

        self.result = "PASSED"

        self.base_dir = '/home/astepenko/Pictures/tests/'

        # client = pymongo.MongoClient("mongodb://tester:tester@192.168.10.254/test_db")

        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

        self.log_path = self.base_dir + self.script_name + "_" + self.start_time.strftime('%Y-%m-%d_%H:%M:%S') + ".txt"

        self.add_to_log("Suite:\t" + self.__class__.__name__ + "\n" +
                        "Test:\t" + method.__name__ + "\n" +
                        "Date:\t" + self.start_time.strftime('%Y-%m-%d %H:%M:%S') + "\n\n")

    def teardown_method(self, method):
        self.end_time = datetime.datetime.now()

        self.add_to_log("\n-----------------------------\n" +
                        "Result: " + self.result + "\n"
                        "Exec time: " +
                        str(datetime.timedelta(seconds=int((self.end_time - self.start_time).total_seconds()))))

        # self.driver.close()
        self.driver.quit()

    def navigate_to(self, url=""):
        if url == "back":
            self.driver.back()
        elif url == "forward":
            self.driver.forward()
        else:
            self.driver.get(url)

    def add_to_log(self, text):
        with open(self.log_path, "a") as log:
            log.write(text)
