import datetime as dt
import logging
import os
import json
import subprocess
from collections import OrderedDict
from contextlib import suppress
from os.path import expanduser

import pymongo
import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class DB:
    server_ip = "10.0.0.204"
    db_server_ip = "10.0.0.204"

    dbs = ["acos", "acos_local"]
    col_names = ["scops", "models", "reservations", "tracks", "render_parameters", "files"]

    def __init__(self, server_ip=""):
        if server_ip == "":
            server_ip = self.server_ip

        daemon_config = self.load_json("/etc/aqueti/daemonConfiguration.json")
        self.dbs = [daemon_config["globalDatabase"]["name"], daemon_config["localDatabase"]["name"]]

        self.mc = pymongo.MongoClient("mongodb://" + server_ip + ":27017")

    def load_json(self, f_name):
        with open(f_name, "r", encoding='utf-8') as f:
            return json.load(f)

    def query(self, query, db=None, col=None):
        if db is None and col is None:
            db, col = self.dbs[0], "scops"

        return list(self.mc[db][col].find(query))

    def query_one(self, query, db="acos", col="scops"):
        return self.mc[db][col].find_one(query, sort = [('_id', pymongo.DESCENDING)])

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

    server_ip = "10.0.0.204"

    home_dir = expanduser("~")
    base_dir = home_dir + "/Downloads/tests/"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_dir = script_dir[:script_dir.rindex('/')]

    doc = OrderedDict()

    def raises(self):
        pass

    @property
    def screenshot_path(self):
        return '{0}/{1}_{2}.png'.format(self.cur_dir, self.doc["test_name"], dt.datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))

    @property
    def driver_path(self):
        driver_path = "drivers/linux/"

        if self.browser == "chrome":
            driver_path += "chromedriver"
        elif self.browser == "firefox":
            driver_path += "geckodriver"
        elif self.browser == "ie":
            driver_path += "IEDriverServer"
        else:
            pass

        return os.path.join(self.script_dir, driver_path)

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

        self.cur_dir = self.base_dir + self.__name__ + "/" + dt.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
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

    def setUp(self):
        pass

    def setup_method(self, method):
        self.browser = os.getenv('BROWSER', 'chrome')

        if self.browser == "chrome":
            opts = ChromeOptions()
            opts.add_experimental_option("detach", True)
            opts.add_experimental_option("w3c", False)
            opts.add_argument('ignore-certificate-errors')
            caps = DesiredCapabilities.CHROME
            caps = {"browserName": "chrome", 'version': '', 'platform': 'ANY', "pageLoadStrategy": "normal"}

            #self.driver = webdriver.Chrome(options=opts, desired_capabilities=caps, executable_path=self.driver_path)  # chrome_options=opts

            self.driver = webdriver.Remote(options=opts, desired_capabilities=caps, command_executor="http://{}:4444/wd/hub".format(self.server_ip))

        elif self.browser == "ff":
            caps = DesiredCapabilities.FIREFOX

            caps = {"pageLoadStrategy": "normal", "browserName": "firefox"}
            #self.driver = webdriver.Firefox(desired_capabilities=caps, executable_path=self.driver_path)

            self.driver = webdriver.Remote(desired_capabilities=caps, command_executor="http://{}:4444/wd/hub".format(self.server_ip))

        elif self.browser == "ie":
            caps = DesiredCapabilities.INTERNETEXPLORER
            caps = {"browserName": "iexplorer"}
            #self.driver = webdriver.Ie(desired_capabilities=caps, executable_path=self.driver_path)

            self.driver = webdriver.Remote(desired_capabilities=caps, command_executor="http://{}:4444/wd/hub".format(self.server_ip))
        else:
            pass


        if self.driver is not None:
            self.driver.maximize_window()

        self.doc["suite_name"] = self.__class__.__name__
        self.doc["test_name"] = method.__name__
        self.doc["case_id"] = 0 if "test_case" not in method.__name__ else int(method.__name__[method.__name__.rindex('_') + 1:])
        self.doc["start_time"] = dt.datetime.now()
        self.doc["end_time"] = None
        self.doc["result"] = -1

        self.doc["user"] = "script"
        self.doc["project"] = pytest.config.getoption('--project')
        self.doc["branch"] = pytest.config.getoption('--branch')
        self.doc["build"] = pytest.config.getoption('--build')
        self.doc["timestamp"] = int(self.doc["start_time"].timestamp() * 1e3)

        self.log_path = self.cur_dir + "/" + self.doc["test_name"] + ".log"

        self.add_to_log("Suite:\t" + self.doc["suite_name"] + "\n" +
                        "Test:\t" + self.doc["test_name"] + "\n" +
                        "Date:\t" + self.doc["start_time"].strftime('%Y-%m-%d_%H:%M:%S') + "\n\n")

    def teardown_method(self, method):
        with open(self.script_dir + '/logs/pytest.log', 'r') as f:
            log = f.read()

        self.doc["end_time"] = dt.datetime.now()
        self.doc["duration"] = int((self.doc["end_time"] - self.doc["start_time"]).total_seconds())
        self.doc["log"] = log

        if self.doc["result"] == 1:
            result = "PASSED"
        else:
            result = "FAILED" if self.doc["result"] == 0 else "ERROR"
            with suppress(Exception): self.driver.save_screenshot(self.screenshot_path)

        self.add_to_log("\nExec time: " + str(dt.timedelta(seconds=self.doc["duration"])) + "\nRESULT: " + result + "\n\n")

        with suppress(Exception): DB(DB.db_server_ip).mc["qa"]["auto"].insert_one(self.doc)

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
