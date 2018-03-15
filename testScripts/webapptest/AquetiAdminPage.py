from BasePage import BasePage
from selenium.webdriver.common.action_chains import ActionChains


class AquetiAdminPage(BasePage):
    @property
    def sidebar_status(self): return self.find_by(css="nav#sidebar a:contains(Status)")

    @property
    def sidebar_configuration(self): return self.find_by(css="nav#sidebar a:contains(Configuration)")

    @property
    def sidebar_maintenance(self): return self.find_by(css="nav#sidebar a:contains(Maintenance)")

    @property
    def system_current_time(self): return self.find_by(id="system-current-time")

    @property
    def system_current_date(self): return self.find_by(id="system-current-date")

    @property
    def sidebar_btn(self): return self.find_by(css="button.sidebar-toggle")

    @property
    def submit_issue_link(self): return self.find_by(css="nav a:contains(Submit Issue)")

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
    def topbar_camera(self): return self.find_by(css="#topbar a:contains(Camera)")

    @property
    def topbar_storage(self): return self.find_by(css="#topbar a:contains(Storage)")

    @property
    def topbar_render(self): return self.find_by(css="#topbar a:contains(Render)")

    def __init__(self, driver):
        AquetiAdminPage.__init__(self, driver)


class AquetiAdminPageConfiguration(AquetiAdminPage):
    @property
    def topbar_system(self): return self.find_by(css="#topbar a:contains(System)")

    @property
    def topbar_camera(self): return self.find_by(css="#topbar a:contains(Camera)")

    @property
    def topbar_storage(self): return self.find_by(css="#topbar a:contains(Storage)")

    @property
    def topbar_render(self): return self.find_by(css="#topbar a:contains(Render)")

    def __init__(self, driver):
        AquetiAdminPage.__init__(self, driver)


class AquetiAdminPageMaintenance(AquetiAdminPage):
    @property
    def topbar_camera(self): return self.find_by(css="#topbar a:contains(Camera)")

    @property
    def topbar_storage(self): return self.find_by(css="#topbar a:contains(Storage)")

    @property
    def topbar_render(self): return self.find_by(css="#topbar a:contains(Render)")

    @property
    def update_software_btn(self): return self.find_by(css="button:contains(Update Software)")

    @property
    def time_btn(self): return self.find_by(css="button:contains(Time)")

    @property
    def system_btn(self): return self.find_by(css="button:contains(System)")

    @property
    def time_set_host_time(self): return self.find_by(css="ul.dropdown-menu a:contains(Set Host Time)")

    @property
    def time_specify_host_ntp(self): return self.find_by(css="ul.dropdown-menu a:contains(Specify Host NTP)")

    @property
    def system_reboot_host_device(self): return self.find_by(css="ul.dropdown-menu a:contains(Reboot Host Device)")

    @property
    def system_shutdown_host_device(self): return self.find_by(css="ul.dropdown-menu a:contains(Shutdown Host Device)")

    @property
    def system_set_host_ip(self): return self.find_by(css="ul.dropdown-menu a:contains(Set Host IP)")

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
    def submit_btn(self): return self.find_by(id="submit")

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

    @property
    def button_play(self): return self.find_by(id="button_play")

    @property
    def button_stop(self): return self.find_by(id="button_stop")

    @property
    def button_window(self): return self.find_by(id="button_window")

    @property
    def image(self): return self.find_by(id="myCanvas")

    @property
    def radio_camera(self): return self.find_by(id="camera")

    @property
    def radio_sensor(self): return self.find_by(id="sensor")

# Image

    @property
    def image_tab(self): return self.find_by(css="a[role='tab']:contains(Image)")

    @property
    def auto_gain(self): return self.find_by(id="auto_gain")

    @property
    def gain_minus(self): return self.find_by(xpath="//*[@id='panel1']//input[@id='auto_gain']/../..//button[contains(.,'-')]")

    @property
    def gain_plus(self): return self.find_by(xpath="//*[@id='panel1']//input[@id='auto_gain']/../..//button[contains(.,'+')]")

    @property
    def gain_field(self): return self.find_by(id="gain")

    @property
    def auto_whitebalance(self): return self.find_by(id="auto_whitebalance")

    @property
    def whitebalance_minus(self): return self.find_by(xpath="//*[@id='panel1']//input[@id='auto_whitebalance']/../..//button[contains(.,'-')]")

    @property
    def whitebalance_plus(self): return self.find_by(xpath="//*[@id='panel1']//input[@id='auto_whitebalance']/../..//button[contains(.,'+')]")

    @property
    def whitebalance_field(self): return self.find_by(id="whitebalance")

    @property
    def auto_shutter(self): return self.find_by(id="auto_shutter")

    @property
    def shutter_minus(self): return self.find_by(xpath="//*[@id='panel1']//input[@id='auto_shutter']/../..//button[contains(.,'-')]")

    @property
    def shutter_plus(self): return self.find_by(xpath="//*[@id='panel1']//input[@id='auto_shutter']/../..//button[contains(.,'+')]")

    @property
    def shutter_field(self): return self.find_by(id="shutter")

    @property
    def sharpening_slider(self): return self.find_by(css="#panel1 div#sharpening_slider div[role='slider']")

    @property
    def sharpening_slider_ribbon(self): return self.find_by(css="#panel1 div#sharpening_slider div.noUi-base")

    @property
    def denoising_slider(self): return self.find_by(css="#panel1 div#denoising_slider div[role='slider']")

    @property
    def denoising_slider_ribbon(self): return self.find_by(css="#panel1 div#denoising_slider div.noUi-base")

    @property
    def night_mode_chkb(self): return self.find_by(id="night_mode")

    @property
    def transport_mode_10bit(self): return self.find_by(css="#panel1 button a:contains(10 bit)")

    @property
    def transport_mode_12bit(self): return self.find_by(css="#panel1 button a:contains(12 bit)")

    @property
    def framerate_25fps(self): return self.find_by(css="#panel1 button a:contains(25 fps)")

    @property
    def framerate_30fps(self): return self.find_by(css="#panel1 button a:contains(30 fps)")

    @property
    def transport_mode_dd(self): return self.find_by(id="transport_mode")

    @property
    def framerate_dd(self): return self.find_by(id="framerate")

# Compression

    @property
    def compression_tab(self): return self.find_by(css="a[role='tab']:contains(Compression)")

    @property
    def quality_high(self): return self.find_by(css="#panel2 a:contains(High)")

    @property
    def quality_medium(self): return self.find_by(css="#panel2 a:contains(Medium)")

    @property
    def quality_low(self): return self.find_by(css="#panel2 a:contains(Low)")

    @property
    def encoding_jpeg(self): return self.find_by(css="#panel2 a:contains(JPEG)")

    @property
    def encoding_h264(self): return self.find_by(css="#panel2 a:contains(H264)")

    @property
    def encoding_h265(self): return self.find_by(css="#panel2 a:contains(H265)")

    @property
    def quality_dd(self): return self.find_by(id="quality")

    @property
    def encoding_dd(self): return self.find_by(id="encoding")

# Focus

    @property
    def focus_tab(self): return self.find_by(css="#panel3 a[role='tab']:contains(Focus)")

    @property
    def focus_chkb(self): return self.find_by(id="checkboxCustom2")

    @property
    def focus_now_btn(self): return self.find_by(css="#panel3 button:contains(Focus Now)")

# Sensor

    @property
    def sensor_tab(self): return self.find_by(css="a[role='tab']:contains(Sensor)")

    @property
    def focus_minus(self): return self.find_by(css="#panel4 button.btn.btn-default.bootstrap-touchspin-down:contains(-)")

    @property
    def focus_plus(self): return self.find_by(css="#panel4 button.btn.btn-default.bootstrap-touchspin-up:contains(+)")

    @property
    def focus_field(self): return self.find_by(id="sensorfocus")

    @property
    def auto_focus_btn(self): return self.find_by(id="sensorAutoFocus")

    def __init__(self, driver):
        AquetiAdminPage.__init__(self, driver)

        self.page_url += "/scop_configuration"

    def move_sharpening_slider(self, pos):
        move = ActionChains(self.driver)
        dx = self.sharpening_slider_ribbon.size["width"] / 100

        move.move_to_element(self.sharpening_slider).click_and_hold(self.sharpening_slider).move_by_offset(pos * dx, 0).release().perform()

    def move_denoising_slider(self, pos):
        move = ActionChains(self.driver)
        dx = self.denoising_slider_ribbon.size["width"] / 100

        move.move_to_element(self.denoising_slider).click_and_hold(self.denoising_slider).move_by_offset(pos * dx, 0).release().perform()


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
