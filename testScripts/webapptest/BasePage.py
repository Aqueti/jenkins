from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time
import hashlib


class BasePage:
    baseURL = ""
    pageURL = ""
    pageTitle = ""

    TIMEOUT = 5

    def __init__(self, driver):
        self.baseURL = "http://10.0.0.207:5000"

        self.driver = driver

    screenshot_path = '/home/astepenko/Pictures/tests/test.png'

    def find_by(self, **kwargs):
        elems = None

        try:
            if "id" in kwargs.keys():
                WebDriverWait(self.driver, self.TIMEOUT).until(EC.presence_of_element_located((By.ID, kwargs["id"])))
                elems = self.driver.find_element_by_id(kwargs["id"])
            else:
                for key, val in sorted(kwargs.items(), key=lambda x: x[0]):
                    if key == "name":
                        if elems is None:
                            WebDriverWait(self.driver, self.TIMEOUT).until(
                                EC.visibility_of_any_elements_located((By.NAME, val)))
                            elems = self.driver.find_element_by_name(val)
                        else:
                            elems = elems.find_element_by_name(val)
                    elif key == "link_text":
                        if elems is None:
                            WebDriverWait(self.driver, self.TIMEOUT).until(
                                EC.visibility_of_any_elements_located((By.LINK_TEXT, val)))
                            elems = self.driver.find_element_by_link_text(val)
                        else:
                            elems = elems.find_element_by_link_text(val)
                    elif key == "partial_link_text":
                        if elems is None:
                            WebDriverWait(self.driver, self.TIMEOUT).until(
                                EC.visibility_of_any_elements_located((By.PARTIAL_LINK_TEXT, val)))
                            elems = self.driver.find_element_by_partial_link_text(val)
                        else:
                            elems = elems.find_element_by_partial_link_text(val)
                    elif key == "tag_name":
                        if elems is None:
                            WebDriverWait(self.driver, self.TIMEOUT).until(
                                EC.visibility_of_any_elements_located((By.TAG_NAME, val)))
                            elems = self.driver.find_element_by_tag_name(val)
                        else:
                            elems = elems.find_element_by_tag_name(val)
                    elif key == "class_name":
                        if elems is None:
                            WebDriverWait(self.driver, self.TIMEOUT).until(
                                EC.visibility_of_any_elements_located((By.CLASS_NAME, val)))
                            elems = self.driver.find_element_by_class_name(val)
                        else:
                            elems = elems.find_element_by_class_name(val)
                    elif key == "css":
                        if elems is None:
                            WebDriverWait(self.driver, self.TIMEOUT).until(
                                EC.visibility_of_any_elements_located((By.CSS_SELECTOR, val)))
                            elems = self.driver.find_element_by_css_selector(val)
                        else:
                            elems = elems.find_element_by_css_selector(val)
                    elif key == "xpath":
                        if elems is None:
                            WebDriverWait(self.driver, self.TIMEOUT).until(
                                EC.visibility_of_any_elements_located((By.XPATH, val)))
                            elems = self.driver.find_element_by_xpath(val)
                        else:
                            elems = elems.find_element_by_xpath(val)
                    else:
                        pass
        except Exception as e:
            pass

        return elems

    def human_type(self, elem, text):
        for char in text:
            time.sleep(random.uniform(0.05, 0.2))
            elem.send_keys(char)

    def perf_action(self, elem, value=""):
        if elem is None:
            return

        value = value.lower();
        tag_name = str(elem.get_attribute('tagName')).lower()

        if tag_name == "select":
            for option in elem:
                if option.get_attribute("value").lower() == value:
                    option.click()
        elif tag_name == "textarea":
            elem.clear()
            elem.send_keys(value)
        elif tag_name == "iframe":
            pass
        elif tag_name == "input":
            type = elem.get_attribute('type').lower()
            if type in ("button", "submit"):
                elem.click()
            elif type in ("text", "password"):
                elem.clear()
               #elem.send_keys(value, Keys.ARROW_DOWN)
                self.human_type(elem, value)
            elif type in ("radio", "checkbox"):
                elem.click()
            else:
                elem.click()
        else:
            elem.click()

    def _(self, elem, value=""):
        self.perf_action(elem, value)

    def switch_to(self, obj="", obj_name=""):
        if obj == "window":
            self.driver.switch_to.window(obj_name)
        elif obj == "alert":
            self.driver.switch_to.alert()
        elif obj == "act_elem":
            self.driver.switch_to.active_element()
        elif obj == "frame":
            self.driver.switch_to.frame(obj_name)
        elif obj == "p_frame":
            self.driver.switch_to.parent_frame(obj_name)
        else:
            self.driver.switch_to.default_content()

    def navigate_to(self, url=""):
        if url == "back":
            self.driver.back()
        elif url == "forward":
            self.driver.forward()
        else:
            if url == "":
                self.driver.get(self.pageURL)
            else:
                self.driver.get(url)


    def make_screenshot(self, path=""):
        if path == "":
            self.driver.save_screenshot(self.screenshot_path)
        else:
            self.driver.save_screenshot(path)