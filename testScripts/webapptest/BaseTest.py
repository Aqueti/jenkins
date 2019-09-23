from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import ChromeOptions
from selenium import webdriver
import unittest
import pytest
import datetime
import os
import subprocess
import time
import pymongo
from collections import OrderedDict
from decorators import *
from os.path import expanduser
import logging
import json
import sys
from contextlib import suppress


class DB:
    server_ip = "10.0.0.189"
    server2_ip = "10.0.0.176"

    dbs = ["acos", "acos_local"]
    col_names = ["scops", "models", "reservations", "tracks", "render_parameters", "files"]

    def __init__(self, server_ip=""):
        if server_ip == "":
            server_ip = self.server_ip

        self.mc = pymongo.MongoClient("mongodb://" + server_ip + ":27017")

    def query(self, query, db="acos", col="scops"):
        return list(self.mc[db][col].find(query))

    def drop(self, db="acos", col="scops"):
        self.db.mc[db][col].drop()

class BaseTest(): # unittest.TestCase
    driver = None
    browser = None

    db = None
    logger = None

    log_path = None
    script_dir = None
    cur_dir = None
    home_dir = expanduser("~")
    base_dir = home_dir + "/Pictures/tests/"

    chrome_path = home_dir + "/Downloads/src/jenkins/testScripts/webapptest/chromedriver"

    doc = OrderedDict()


    def raises(self):
        pass

    @property
    def screenshot_path(self):
        return '{0}/{1}_{2}.png'.format(self.cur_dir, self.doc["test_name"], datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))

    @property
    def failure_exception(self, *args, **kwargs):
        class BaseTestFailureException(AssertionError):
            def __init__(self, *args, **kwargs):
                return super(BaseTestFailureException, self).__init__(*args, **kwargs)

            def __call__(self, *args, **kwargs):
                self.add_to_log(args[0])

                with suppress(Exception): self.driver.save_screenshot(self.screenshot_path)

        BaseTestFailureException.__name__ = Exception.__name__   # AssertionError.__name__

        return BaseTestFailureException

    def __call__(self, *args, **kwargs):
        super(BaseTest, self).__call__(*args, **kwargs)

    @classmethod
    def setup_class(self):
        self.db = DB()
        self.logger = logging.getLogger(__name__)

        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.cur_dir = self.base_dir + self.__name__ + "/" + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        if not os.path.exists(self.cur_dir):
            os.makedirs(self.cur_dir)

    @classmethod
    def teardown_class(self):
        pass

    def error_processing(func):
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except AssertionError:
                raise

        return wrapper

    def setup_method(self, method):
        if self.browser == "chrome":
            opts = ChromeOptions()
            opts.add_experimental_option("detach", True)
            opts.add_experimental_option("w3c", False)
            caps = DesiredCapabilities.CHROME
            caps["pageLoadStrategy"] = "normal"  # none
            self.driver = webdriver.Chrome(options=opts, desired_capabilities=caps,  executable_path=self.chrome_path)  # chrome_options=opts
        elif self.browser == "ff":
            caps = DesiredCapabilities.FIREFOX
            self.driver = webdriver.Firefox()
        else:
            pass

        if self.driver is not None:
            self.driver.maximize_window()

        self.doc["suite_name"] = self.__class__.__name__
        self.doc["test_name"] = method.__name__
        self.doc["case_id"] = 0 if "test_case" not in method.__name__ else int(method.__name__[method.__name__.rindex('_') + 1:])
        self.doc["start_time"] = datetime.datetime.now()
        self.doc["end_time"] = None
        self.doc["result"] = -1

        self.doc["user"] = "script"
        self.doc["project"] = pytest.config.getoption('--project')
        self.doc["branch"] = pytest.config.getoption('--branch')
        self.doc["build"] = pytest.config.getoption('--build')
        self.doc["timestamp"] = int(self.doc["start_time"].timestamp() * 1e3)

        self.log_path = self.cur_dir + "/" + self.doc["test_name"] + ".txt"

        self.add_to_log("Suite:\t" + self.doc["suite_name"] + "\n" +
                        "Test:\t" + self.doc["test_name"] + "\n" +
                        "Date:\t" + self.doc["start_time"].strftime('%Y-%m-%d_%H:%M:%S') + "\n\n")

    def teardown_method(self, method):
        with open(self.script_dir + '/pytest.log', 'r') as f:
            log = f.read()

        self.doc["end_time"] = datetime.datetime.now()
        self.doc["duration"] = int((self.doc["end_time"] - self.doc["start_time"]).total_seconds())
        self.doc["log"] = log

        if self.doc["result"] == 1:
            result = "PASSED"
        else:
            result = "FAILED" if self.doc["result"] == 0 else "ERROR"
            with suppress(Exception): self.driver.save_screenshot(self.screenshot_path)

        self.add_to_log("\nExec time: " + str(datetime.timedelta(seconds=self.doc["duration"])) + "\nRESULT: " + result + "\n\n")

        with suppress(Exception): DB(DB.server2_ip).mc["qa"]["auto"].insert_one(self.doc)

        if self.driver is not None:
            self.driver.quit()
            # self.driver.close()

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

    def exec_cmd(self, cmd):
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.stdout.decode('utf-8') != "":
            return result.stdout.decode('utf-8')
        else:
            return result.stderr.decode('utf-8')
