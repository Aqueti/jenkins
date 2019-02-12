from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import ChromeOptions
from selenium import webdriver
import pytest
import datetime
import os
import subprocess
import time
import pymongo
import json


class BaseTest(object):
    driver = None
    browser = None

    mongo_client = None

    doc = {}

    log_path = None
    base_dir = "/home/astepenko/Pictures/tests/"
    mongo_path = r"mongodb://10.0.0.176:27017/"
    chrome_path = r'/home/astepenko/Downloads/src/jenkins/testScripts/webapptest/chromedriver'

    @property
    def screenshot_path(self):
        return '{0}/{1}_{2}.png'.format(self.base_dir, self.doc["script_name"], datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))

    @property
    def failure_exception(self):
        class BaseTestFailureException(AssertionError):
            def __init__(self, *args, **kwargs):
                return super(BaseTestFailureException, self).__init__(*args, **kwargs)

            self.doc["result"] = "FAILED"
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

        self.doc["start_time"] = datetime.datetime.now()
        self.doc["start_time_f"] = self.doc["start_time"].strftime('%Y-%m-%d_%H:%M:%S')
        self.doc["end_time"] = None
        self.doc["suite_name"] = self.__class__.__name__
        self.doc["test_name"] = method.__name__
        self.doc["result"] = "PASSED"

        try:
            self.mongo_client = pymongo.MongoClient(self.mongo_path)
        except:
            pass

        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

        self.log_path = self.base_dir + self.doc["suite_name"] + "_" + self.doc["test_name"] + "_" + self.doc["start_time_f"] + ".txt"

        self.add_to_log("Suite:\t" + self.doc["suite_name"] + "\n" +
                        "Test:\t" + self.doc["test_name"] + "\n" +
                        "Date:\t" + self.doc["start_time_f"] + "\n\n")

    def teardown_method(self, method):
        self.doc["end_time"] = datetime.datetime.now()

        if self.mongo_client is not None:
            self.mongo_client["test_res"]["beta"].insert_one(self.doc)

        self.add_to_log("\n-----------------------------\n" +
                        "Result: " + self.doc["result"] + "\n"
                        "Exec time: " +
                        str(datetime.timedelta(seconds=int((self.doc["end_time"] - self.doc["start_time"]).total_seconds()))))

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
