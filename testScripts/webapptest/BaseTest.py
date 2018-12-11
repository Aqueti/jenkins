from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import ChromeOptions
from selenium import webdriver
import pytest
import datetime
import os
import subprocess
import time
import pymongo


class BaseTest(object):
    driver = None
    browser = "chrome"

    mongo_client = None

    result = "PASSED"
    script_name = None
    start_time = None
    end_time = None

    log_path = None
    base_dir = "/home/astepenko/Pictures/tests/"
    mongo_path = r"mongodb://10.0.0.120:27017/"
    chrome_path = r'/home/astepenko/Downloads/src/jenkins/testScripts/webapptest/chromedriver'

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
            self.driver = webdriver.Chrome(desired_capabilities=caps,  executable_path=self.chrome_path)  # chrome_options=opts
        elif self.browser == "ff":
            caps = DesiredCapabilities.FIREFOX
            self.driver = webdriver.Firefox()
        else:
            pass

        if self.driver is not None:
            self.driver.maximize_window()

        self.script_name = self.__class__.__name__ + "_" + method.__name__

        self.start_time = datetime.datetime.now()

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
        if self.driver is not None:
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

    def exec(self, cmd):
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.stdout.decode('utf-8') != "":
            return result.stdout.decode('utf-8')
        else:
            return result.stderr.decode('utf-8')

    def get_col_obj(self, db_name, col_name):
        if db_name == "":
            if col_name in ('models', 'reservations', 'scops', 'tracks'):
                db_name = "acos"
            elif col_name in 'files':
                db_name = "acos_local"

        client = pymongo.MongoClient(self.mongo_path)

        return client[db_name][col_name]
