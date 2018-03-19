from selenium.webdriver import ChromeOptions
from selenium import webdriver
import unittest
import datetime


class BaseTest(unittest.TestCase):
    driver = None
    browser = "chrome"

    @property
    def screenshot_path(self):
        return '/home/astepenko/Pictures/tests/' + self.script_name + "_" + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S') + ".png"

    #def __call__(self, *args, **kwargs):
    #    super(BaseTest, self).__call__(*args, **kwargs)

    def setUp(self):
        if self.browser == "chrome":
            opts = ChromeOptions()
            opts.add_experimental_option("detach", True)
            self.driver = webdriver.Chrome(chrome_options=opts)
        elif self.browser == "ff":
            self.driver = webdriver.Firefox()
        else:
            pass

        self.driver.maximize_window()

        self.script_name = self.__class__.__name__ + "_" + self.__dict__['_testMethodName']

        self.start_time = datetime.datetime.now()

        self.log_path = '/home/astepenko/Pictures/tests/' + self.script_name + "_" + self.start_time.strftime('%Y-%m-%d_%H:%M:%S') + ".txt"

        self.add_to_log("Suite:\t" + self.__class__.__name__ + "\n" +
                        "Test:\t" + self.__dict__['_testMethodName'] + "\n" +
                        "Date:\t" + self.start_time.strftime('%Y-%m-%d %H:%M:%S') + "\n\n")

    def tearDown(self):
        self.end_time = datetime.datetime.now()

        self.result = "PASSED"

        self.add_to_log("\n-----------------------------\n" +
                        "Result: " + self.result + "\n"
                        "Exec time: " +
                        str(datetime.timedelta(seconds=int((self.end_time - self.start_time).total_seconds()))))

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

    def add_to_log(self, text):
        with open(self.log_path, "a") as log:
            log.write(text)
