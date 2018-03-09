import BasePage


class AquetiAdminPage(BasePage.BasePage):
    @property
    def sidebar_status(self): return self.find_by(xpath="//nav[@id='sidebar']//a[contains(.,'Status')]")

    @property
    def sidebar_configuration(self): return self.find_by(xpath="//nav[@id='sidebar']//a[contains(.,'Configuration')]")

    @property
    def sidebar_maintenance(self): return self.find_by(xpath="//nav[@id='sidebar']//a[contains(.,'Maintenance')]")

    @property
    def topbar_camera(self): return self.find_by(xpath="//div[@id='topbar']//a[contains(.,'Camera')]")

    @property
    def topbar_storage(self): return self.find_by(xpath="//div[@id='topbar']//a[contains(.,'Storage')]")

    @property
    def topbar_render(self): return self.find_by(xpath="//div[@id='topbar']//a[contains(.,'Render')]")

    def __init__(self, driver, is_nav=False):
        BasePage.BasePage.__init__(self, driver)

        self.pageURL = self.baseURL
        self.pageTitle = "Aqueti Admin"

        if is_nav:
            self.navigate_to()

    def click_links(self):
        self._(self.sidebar_status)
        self._(self.sidebar_configuration)
        self._(self.sidebar_maintenance)
