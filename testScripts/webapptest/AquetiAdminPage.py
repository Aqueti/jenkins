from BasePage import BasePage


class AquetiAdminPage(BasePage):
    @property
    def sidebar_status(self): return self.find_by(xpath="//nav[@id='sidebar']//a[contains(.,'Status')]")

    @property
    def sidebar_configuration(self): return self.find_by(xpath="//nav[@id='sidebar']//a[contains(.,'Configuration')]")

    @property
    def sidebar_maintenance(self): return self.find_by(xpath="//nav[@id='sidebar']//a[contains(.,'Maintenance')]")

    @property
    def system_current_time(self): return self.find_by(id="system-current-time")

    @property
    def system_current_date(self): return self.find_by(id="system-current-date")

    @property
    def sidebar_button(self): return self.find_by(css="button.sidebar-toggle")

    @property
    def submit_issue_link(self): return self.find_by(partial_link_text="Submit Issue")

    @property
    def search_link(self): return self.find_by(css="a.search-open.nav-link")

    def __init__(self, driver):
        BasePage.__init__(self, driver)

    def click_links(self):
        self._(self.sidebar_status)
        self._(self.sidebar_configuration)
        self._(self.sidebar_maintenance)


class AquetiAdminPageStatus(AquetiAdminPage):
    @property
    def topbar_camera(self): return self.find_by(xpath="//div[@id='topbar']//a[contains(.,'Camera')]")

    @property
    def topbar_storage(self): return self.find_by(xpath="//div[@id='topbar']//a[contains(.,'Storage')]")

    @property
    def topbar_render(self): return self.find_by(xpath="//div[@id='topbar']//a[contains(.,'Render')]")

    def __init__(self, driver):
        AquetiAdminPage.__init__(self, driver)


class AquetiAdminPageConfiguration(AquetiAdminPage):
    @property
    def topbar_system(self): return self.find_by(xpath="//div[@id='topbar']//a[contains(.,'System')]")

    @property
    def topbar_camera(self): return self.find_by(xpath="//div[@id='topbar']//a[contains(.,'Camera')]")

    @property
    def topbar_storage(self): return self.find_by(xpath="//div[@id='topbar']//a[contains(.,'Storage')]")

    @property
    def topbar_render(self): return self.find_by(xpath="//div[@id='topbar']//a[contains(.,'Render')]")

    def __init__(self, driver):
        AquetiAdminPage.__init__(self, driver)


class AquetiAdminPageMaintenance(AquetiAdminPage):
    @property
    def topbar_camera(self): return self.find_by(xpath="//div[@id='topbar']//a[contains(.,'Camera')]")

    @property
    def topbar_storage(self): return self.find_by(xpath="//div[@id='topbar']//a[contains(.,'Storage')]")

    @property
    def topbar_render(self): return self.find_by(xpath="//div[@id='topbar']//a[contains(.,'Render')]")
    def __init__(self, driver):
        AquetiAdminPage.__init__(self, driver)


class AquetiAdminPageCamera(AquetiAdminPage):
    @property
    def prop_status(self): return self.find_by(id="status")

    @property
    def prop_recording(self): return self.find_by(id="recording")

    @property
    def prop_serialid(self): return self.find_by(id="serial")

    @property
    def prop_software(self): return self.find_by(id="software")

    @property
    def prop_kernel(self): return self.find_by(id="kernel")

    @property
    def prop_host(self): return self.find_by(id="host")

    @property
    def components(self): return self.find_by(css="nav#combar li")

    @property
    def prop_cam_nickname(self): return self.find_by(id="nickname")

    @property
    def prop_cam_model(self): return self.find_by(id="model")

    @property
    def prop_cam_label(self): return self.find_by(id="label")

    def __init__(self, driver):
        AquetiAdminPage.__init__(self, driver)


class AquetiAdminPageStorage(AquetiAdminPage):
    @property
    def prop_status(self): return self.find_by(id="status")

    @property
    def prop_serialid(self): return self.find_by(id="id")

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


class AquetiAdminPageRender(AquetiAdminPage):
    @property
    def prop_serialid(self): return self.find_by(id="id")

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


class AquetiAdminPageSystem(AquetiAdminPage):
    def __init__(self, driver):
        AquetiAdminPage.__init__(self, driver)


class AquetiAdminPageIssue(AquetiAdminPage):
    @property
    def title_field(self): return self.find_by(id="title") #Title

    @property
    def summary_field(self): return self.find_by(id="summary") #Summary

    @property
    def description_field(self): return self.find_by(id="description") #Description

    @property
    def submit_button(self): return self.find_by(id="submit")

    def __init__(self, driver):
        AquetiAdminPage.__init__(self, driver)

        self.page_url += "/submit_issue"

    def submit_issue(self, title, summary, description):
        self._(self.title_field, title)
        self._(self.summary_field, summary)
        self._(self.description_field, description)
        self._(self.submit_button)

        return AquetiAdminPageStatusCamera(self.driver)


class AquetiAdminPageStatusCamera(AquetiAdminPageStatus, AquetiAdminPageCamera):
    @property
    def prop_sensor_model(self): return self.find_by(id="sensor_model")

    @property
    def prop_sensor_host(self): return self.find_by(id="sensor_host")

    @property
    def prop_sensors(self): return self.find_by(id="sensor-svg")

    def __init__(self, driver):
        AquetiAdminPage.__init__(self, driver)

        self.page_url += "/scop_status"


class AquetiAdminPageStatusStorage(AquetiAdminPageStatus, AquetiAdminPageStorage):
    def __init__(self, driver):
        AquetiAdminPage.__init__(self, driver)

        self.page_url += "/storage_status"


class AquetiAdminPageStatusRender(AquetiAdminPageStatus, AquetiAdminPageRender):
    def __init__(self, driver):
        AquetiAdminPage.__init__(self, driver)

        self.page_url += "/render_status"


class AquetiAdminPageConfigurationSystem(AquetiAdminPageConfiguration, AquetiAdminPageSystem):
    @property
    def node_graph(self): return self.find_by(id="node-graph")

    def __init__(self, driver):
        AquetiAdminPage.__init__(self, driver)

        self.page_url += "/pipeline_configuration"


class AquetiAdminPageConfigurationCamera(AquetiAdminPageConfiguration, AquetiAdminPageCamera):
    @property
    def prop_sensors(self): return self.find_by(id="sensor-svg")

    def __init__(self, driver):
        AquetiAdminPage.__init__(self, driver)

        self.page_url += "/scop_configuration"


class AquetiAdminPageConfigurationStorage(AquetiAdminPageConfiguration, AquetiAdminPageStorage):
    def __init__(self, driver):
        AquetiAdminPage.__init__(self, driver)

        self.page_url += "/storage_configuration"


class AquetiAdminPageConfigurationRender(AquetiAdminPageConfiguration, AquetiAdminPageRender):
    def __init__(self, driver):
        AquetiAdminPage.__init__(self, driver)

        self.page_url += "/render_configuration"


class AquetiAdminPageMaintenanceCamera(AquetiAdminPageMaintenance, AquetiAdminPageCamera):
    def __init__(self, driver):
        AquetiAdminPage.__init__(self, driver)

        self.page_url += "/scop_maintenance"


class AquetiAdminPageMaintenanceStorage(AquetiAdminPageMaintenance, AquetiAdminPageStorage):
    def __init__(self, driver):
        AquetiAdminPage.__init__(self, driver)

        self.page_url += "/storage_maintenance"


class AquetiAdminPageMaintenanceRender(AquetiAdminPageMaintenance, AquetiAdminPageRender):
    def __init__(self, driver):
        AquetiAdminPage.__init__(self, driver)

        self.page_url += "/render_maintenance"
