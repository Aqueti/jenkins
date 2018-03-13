from selenium.webdriver.remote.webelement import WebElement


class WebElem:
    def __init__(self, web_elem):
        self.web_elem = web_elem

    def __call__(self):
        return self.web_elem

    def get_parent(self):
        return self.web_elem.find_element_by_xpath("..")

    def get_label(self):
        labels = self.web_elem.parent.find_elements_by_tag_name("label")
        if labels is not None:
            return labels[0]
