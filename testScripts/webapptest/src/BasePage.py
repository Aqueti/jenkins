from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.command import Command
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotVisibleException
from src.decorators import *
import hashlib
import random
import time


class BasePage:
    @property
    def url(self):
        return self.driver.current_url

    @property
    def curl(self):
        s = self.driver.current_url
        s = s[s.index("://") + 3:]
        s = s[s.index("/"):]

        return s


    @property
    def title(self):
        return self.driver.title

    @property
    def source(self):
        return self.driver.page_source

    @property
    def source_hash(self):
        return hashlib.md5(self.driver.page_source.encode('utf-8')).hexdigest()

    prev_page_url = ""
    step_name = ""
    page_title = ""
    base_url = ""
    page_url = ""

    def __init__(self, *args):
        page_obj = self

        def call(self, *args, **kwargs):
            @async
            def highlight(elem):
                page_obj.exec_js("arguments[0].style.cssText += 'border: 1px solid yellow; overflow: auto;'", elem)
                time.sleep(0.3)
                page_obj.exec_js("arguments[0].style.cssText = arguments[0].style.cssText.replace('border: 1px solid yellow; overflow: auto;', '');", elem)
                time.sleep(0.1)

            highlight(self)

            if len(kwargs) == 0:
                page_obj._(self)
            else:
                if "value" in kwargs.keys():
                    page_obj._(self, str(kwargs["value"]))
                elif "act" in kwargs.keys():
                    if "click" in kwargs.values():
                        times = kwargs["times"] if "times" in kwargs.keys() else 1

                        for i in range(times):
                            page_obj.__add_to_log(page_obj.__get_description(self))
                            self.click()
                            time.sleep(0.25)
                    elif "rightclick" in kwargs.values():
                        actionChains = ActionChains(page_obj.driver)
                        actionChains.context_click(self).perform()
                    elif "dblclick" in kwargs.values():
                        actionChains = ActionChains(page_obj.driver)
                        actionChains.double_click(self).perform()
                    elif "focus" in kwargs.values():
                        page_obj.exec_js("arguments[0].focus();", self)
                    elif "scroll_to" in kwargs.values():
                        page_obj.exec_js("arguments[0].scrollIntoView(true);", self)
                    elif "check" in kwargs.values():
                        if not self.is_selected():
                            page_obj._(self)
                    elif "uncheck" in kwargs.values():
                        if self.is_selected():
                            page_obj._(self)
                    elif "default" in kwargs.values():
                        # page_obj.driver.execute_script("arguments[0].setAttribute(arguments[1], arguments[2]);", self, "default", "")
                        page_obj._(self)

        def click(self, *args, **kwargs):
            try:
                self._execute(Command.CLICK_ELEMENT)
            except (ElementClickInterceptedException, ElementNotVisibleException) as e:
                page_obj.exec_js("return arguments[0].click()", self)

        def is_checked(self):
            e = page_obj.find_by(xpath="//input[@type='radio' or @type='checkbox']", elem=self)
            if e is not None:
                if e.get_attribute("aria-checked") == "true":
                    return True

            return False

        def is_focused(self):
            pass

        WebElement.__call__ = call
        WebElement.click = click
        WebElement.is_checked = is_checked
        WebElement.is_focused = is_focused

        self.TIMEOUT = 10

        if "Context" in str(type(args[0])):
            self.driver = args[0].test.driver
            self.test = args[0].test
        else:
            self.driver = args[0].driver
            self.test = args[0]


    def find_by(self, **kwargs):
        if 'elem' in kwargs.keys():
            elems = kwargs['elem']
        else:
            elems = None

        IS_VISIBLE = True
        if "param" in kwargs.keys():
            if kwargs["param"] == "invisible":
                IS_VISIBLE = False

        try:
            if "id" in kwargs.keys():
                if IS_VISIBLE:
                    WebDriverWait(self.driver, self.TIMEOUT).until(EC.presence_of_element_located((By.ID, kwargs["id"])))
                elems = self.driver.find_element_by_id(kwargs["id"])
            else:
                for key, val in sorted(kwargs.items(), key=lambda x: x[0]):
                    if key == "name":
                        if elems is None:
                            if IS_VISIBLE:
                                WebDriverWait(self.driver, self.TIMEOUT).until(
                                    EC.visibility_of_any_elements_located((By.NAME, val)))
                            elems = self.driver.find_elements_by_name(val)
                        else:
                            elems = elems.find_elements_by_name(val)
                    elif key == "link_text":
                        if elems is None:
                            if IS_VISIBLE:
                                WebDriverWait(self.driver, self.TIMEOUT).until(
                                    EC.visibility_of_any_elements_located((By.LINK_TEXT, val)))
                            elems = self.driver.find_elements_by_link_text(val)
                        else:
                            elems = elems.find_elements_by_link_text(val)
                    elif key == "partial_link_text":
                        if elems is None:
                            if IS_VISIBLE:
                                WebDriverWait(self.driver, self.TIMEOUT).until(
                                    EC.visibility_of_any_elements_located((By.PARTIAL_LINK_TEXT, val)))
                            elems = self.driver.find_elements_by_partial_link_text(val)
                        else:
                            elems = elems.find_elements_by_partial_link_text(val)
                    elif key == "tag_name":
                        if elems is None:
                            if IS_VISIBLE:
                                WebDriverWait(self.driver, self.TIMEOUT).until(
                                    EC.visibility_of_any_elements_located((By.TAG_NAME, val)))
                            elems = self.driver.find_elements_by_tag_name(val)
                        else:
                            elems = elems.find_elements_by_tag_name(val)
                    elif key == "class_name":
                        if elems is None:
                            if IS_VISIBLE:
                                WebDriverWait(self.driver, self.TIMEOUT).until(
                                    EC.visibility_of_any_elements_located((By.CLASS_NAME, val)))
                            elems = self.driver.find_elements_by_class_name(val)
                        else:
                            elems = elems.find_elements_by_class_name(val)
                    elif key == "css":
                        if elems is None:
                            if IS_VISIBLE:
                                WebDriverWait(self.driver, self.TIMEOUT).until(
                                    EC.visibility_of_any_elements_located((By.CSS_SELECTOR, val)))
                            elems = self.driver.find_elements_by_css_selector(val)
                        else:
                            elems = elems.find_elements_by_css_selector(val)
                    elif key == "xpath":
                        if elems is None:
                            if IS_VISIBLE:
                                WebDriverWait(self.driver, self.TIMEOUT).until(
                                    EC.visibility_of_any_elements_located((By.XPATH, val)))
                            elems = self.driver.find_elements_by_xpath(val)
                        else:
                            elems = elems.find_elements_by_xpath("." + val)
                    else:
                        continue

                    if elems is not None:
                        if len(elems) == 1:
                            return elems[0]
                        elif len(elems) == 0:
                            return None

        except Exception as e:
            err_msg = "\tELEMENT NOT FOUND: " + str(kwargs) + "\n"
            self.__add_to_log(err_msg)
            if self.test is not None:
                self.test.failure_exception(err_msg)

        return elems


    def __human_type(self, elem, text):
        for char in text:
            time.sleep(random.uniform(0.01, 0.05))
            elem.send_keys(char)

    def __perf_action(self, elem, value=""):
        if elem is None:
            return

        value = value.lower()
        tag_name = str(elem.get_attribute('tagName')).lower()

        if tag_name == "select":
            select = Select(elem)
            select.select_by_value(value)
        elif tag_name == "textarea":
            elem.clear()
            elem.send_keys(value)
        elif tag_name == "div":
            class_name = elem.get_attribute('class')
            if class_name is not None:
                if "v-slider__thumb" in class_name:
                    arr = value.split(';')
                    offset = int(float(arr[0]) * float(arr[1]))

                    move = ActionChains(self.driver)
                    move.click_and_hold(elem).move_by_offset(offset, 0).release().perform()

                    return

            elem.click()
        elif tag_name == "iframe":
            pass
        elif tag_name == "input":
            type = elem.get_attribute('type').lower()
            if type in ("button", "submit"):
                if "className" in dir(elem):
                    if "bootstrap-touchspin-" in elem.className:
                        self.exec_js("return $(arguments[0]).trigger('mousedown').trigger('touchcancel');", elem)
                else:
                    elem.click()
            elif type in ("number", "text", "password"):
                if elem.get_attribute('value') != "":
                    elem.click()

                    self.exec_js("arguments[0].setAttribute('value','')", elem)

                    while elem.get_attribute('value') != "":
                        elem.send_keys(Keys.DELETE, Keys.BACKSPACE)

                    elem.click()

                if elem.text != "":
                    elem.clear()

                self.__human_type(elem, value)
            elif type in ("radio", "checkbox"):
                elem.click()
            else:
                elem.click()
        else:
            elem.click()

    def _(self, elem, value="", step_name=""):
        if elem is not None:
            self.__add_to_log(self.__get_description(elem, value, step_name))

            self.exec_js("arguments[0].scrollIntoView(true);", elem)

            self.__perf_action(elem, value)

            if "Internal Server Error" in self.source:
                if self.test is not None:
                    self.test.fail()

    def switch_to(self, obj="", obj_name=""):
        if obj == "window":
            if obj_name in range(0, 9):
                self.driver.switch_to.window(self.driver.window_handles[obj_name])
            else:
                self.driver.switch_to.window(obj_name)
        elif obj == "alert":
            self.driver.switch_to.alert()
        elif obj == "active_elem":
            self.driver.switch_to.active_element()
        elif obj == "frame":
            self.driver.switch_to.frame(obj_name)
        elif obj == "p_frame":
            self.driver.switch_to.parent_frame(obj_name)
        else:
            self.driver.switch_to.default_content()

    def exec_js(self, js, elem=None):
        self.driver.execute_script(js, elem)

    def reload(self):
        self.exec_js("location.reload();")

    def __get_description(self, elem, value="", step_name=""):
        if elem is None:
            return

        out = "\t"

        if self.prev_page_url != self.url:
            self.prev_page_url = self.url
            out = self.url + "\n" + out
        if step_name != self.step_name:
            self.step_name = step_name
            out = self.step_name + "\n" + out

        value = value.lower()
        tag_name = str(elem.get_attribute('tagName')).lower()

        if tag_name == "a":
            out += "Click '" + elem.get_attribute('innerText').strip().replace('\n', ' ') + "' link"
        elif tag_name == "select":
            out += "Select '" + value + "' in '" + self.get_label(elem) + "' dropdown"
        elif tag_name == "textarea":
            out += "Enter '" + value + "' into '" + self.get_label(elem) + "' field"
        elif tag_name == "button":
            out += "Click '" + elem.get_attribute('innerText').strip() + "' button"
        elif tag_name == "div":
            class_name = elem.get_attribute('class')
            if "v-slider__thumb" in class_name:
                out += "Move slider '" + self.get_label(elem) + "' by " + value
            else:
                out += "Click unknown element, tagName=" + elem.tag_name
        elif tag_name == "iframe":
            pass
        elif tag_name == "input":
            type = elem.get_attribute('type').lower()

            if type in ("button", "submit"):
                out += "Click '" + elem.get_attribute('value').strip() + "' button"
            elif type in ("text", "password"):
                out += "Enter '" + value + "' into '" + self.get_label(elem) + "' field"
            elif type in "radio":
                out += "Click '" + self.get_label(elem) + "' radio button"
            elif type in "checkbox":
                if elem.is_selected():
                    out += "Uncheck '" + self.get_label(elem) + "' check box"
                else:
                    out += "Check '" + self.get_label(elem) + "' check box"
            else:
                out += "Click unknown element, tagName=input, type=" + type
        else:
            out += "Click unknown element, tagName=" + elem.tag_name

        return out + "\n"

    def __add_to_log(self, text):
        if self.test is not None:
            with open(self.test.log_path, "a") as log:
                log.write(text)

    def get_label(self, elem):
        max_depth = 2

        if elem.get_attribute('type') == 'text':
            max_depth = 5

        t_elem = elem
        labels = []
        try:
            labels = self.driver.find_elements_by_css_selector("label[for=" + elem.get_attribute('id') + "]")
        except Exception as e:
            pass

        while len(labels) == 0 and max_depth > 0:
            t_elem = t_elem.find_element_by_xpath("..")

            labels = t_elem.find_elements_by_xpath("./label")

            max_depth -= 1

        if len(labels) > 0:
            return labels[0].get_attribute("innerText").strip()
        else:
            return ""

    def make_screenshot(self, path=""):
        if path == "":
            if self.test is not None:
                self.driver.save_screenshot(self.test.screenshot_path)
        else:
            self.driver.save_screenshot(path)

    def navigate_to(self, url=""):
        if url == "":
            print(self.page_url)
            self.driver.get(self.page_url)
        else:
            self.driver.get(url)
