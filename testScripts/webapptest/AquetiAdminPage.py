from BasePage import BasePage


class AquetiAdminPage(BasePage):
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

    def __init__(self, driver):
        BasePage.__init__(self, driver)

    def click_links(self):
        self._(self.sidebar_status)
        self._(self.sidebar_configuration)
        self._(self.sidebar_maintenance)


class AquetiAdminPageConfiguration(AquetiAdminPage):
    @property
    def topbar_system(self): return self.find_by(xpath="//div[@id='topbar']//a[contains(.,'System')]")

    @property
    def prop_serial(self): return self.find_by(id="id")

    @property
    def prop_software(self): return self.find_by(id="software")

    @property
    def prop_kernel(self): return self.find_by(id="kernel")

    @property
    def prop_host(self): return self.find_by(id="host")

    def __init__(self, driver):
        AquetiAdminPage.__init__(self, driver)


class AquetiAdminPageMaintenance(AquetiAdminPage):
    @property
    def prop_serial(self): return self.find_by(id="id")

    @property
    def prop_software(self): return self.find_by(id="software")

    @property
    def prop_kernel(self): return self.find_by(id="kernel")

    @property
    def prop_host(self): return self.find_by(id="host")

    def __init__(self, driver):
        AquetiAdminPage.__init__(self, driver)


class AquetiAdminPageStatus(AquetiAdminPage):
    @property
    def prop_software(self): return self.find_by(id="software")

    @property
    def prop_kernel(self): return self.find_by(id="kernel")

    @property
    def prop_host(self): return self.find_by(id="host")

    @property
    def components(self): return self.find_by(css="nav#combar li")

    def __init__(self, driver):
        AquetiAdminPage.__init__(self, driver)


class AquetiAdminPageStatusCamera(AquetiAdminPageStatus):
    @property
    def prop_status(self): return self.find_by(id="status")

    @property
    def prop_serial(self): return self.find_by(id="serial")

    @property
    def prop_recording(self): return self.find_by(id="recording")

    @property
    def prop_sensor_module(self): return self.find_by(id="sensor_model")

    @property
    def prop_sensor_host(self): return self.find_by(id="sensor_host")

    def __init__(self, driver):
        AquetiAdminPageStatus.__init__(self, driver)

        self.page_url += "/scop_status"

    def get_status_value(self):
        return self.prop_status.get_attribute('innerText').replace("&nbsp;", " ")


class AquetiAdminPageStatusRender(AquetiAdminPageStatus):
    @property
    def prop_serial(self): return self.find_by(id="id")

    def __init__(self, driver):
        AquetiAdminPageStatus.__init__(self, driver)

        self.page_url += "/render_status"


class AquetiAdminPageStatusStorage(AquetiAdminPageStatus):
    @property
    def prop_status(self): return self.find_by(id="status")

    @property
    def prop_serial(self): return self.find_by(id="id")

    def __init__(self, driver):
        AquetiAdminPageStatus.__init__(self, driver)

        self.page_url += "/storage_status"
