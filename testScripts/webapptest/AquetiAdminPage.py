from BasePage import *
from selenium.webdriver.common.action_chains import ActionChains


class AquetiAdminLoginPage(BasePage):
    @Property
    def username_field(self): return self.find_by(id="login-username")

    @Property
    def password_field(self): return self.find_by(id="login-password")

    @Property
    def login_btn(self): return self.find_by(css="form#login-form input[type='submit']")

    def login(self, username, password):
        self.username_field(value=username)
        self.password_field(value=password)
        self.login_btn()
        if self.cur_page_url == (self.base_url + "/scop_status"):
            return AquetiAdminPageStatusCamera(self)

    def __init__(self, driver):
        BasePage.__init__(self, driver)

        self.page_title = "Aqueti Admin"
        self.base_url = "http://10.0.0.207:5003"
        self.page_url = self.base_url + "/login"


class AquetiAdminPage(BasePage):
    @Property
    def sidebar_status(self): return self.find_by(partial_link_text="Status")

    @Property
    def sidebar_configuration(self): return self.find_by(partial_link_text="Configuration")

    @Property
    def sidebar_maintenance(self): return self.find_by(partial_link_text="Maintenance")

    @Property
    def system_current_time(self): return self.find_by(id="system-current-time")

    @Property
    def system_current_date(self): return self.find_by(id="system-current-date")

    @Property
    def sidebar_btn(self): return self.find_by(css="button.sidebar-toggle")

    @Property
    def submit_issue(self): return self.find_by(css="nav a:contains(Submit Issue)")

    @Property
    def search(self): return self.find_by(css="a.search-open.nav-link")

    @Property
    def logout(self): return self.find_by(id="logout")

# Search

    @Property
    def search_field(self): return self.find_by(css="searchForm input")

    @Property
    def search_btn(self): return self.find_by(css="searchForm button")

    @Property
    def close(self): return self.find_by(css="div.close-btn i.fa-close")

    def __init__(self, driver):
        BasePage.__init__(self, driver)

        self.page_title = "Aqueti Admin"
        self.base_url = "http://10.0.0.207:5003"  # .185:5000
        self.page_url = self.base_url

    def __call__(self, text):
        super(BasePage, self).__call__()

    def click_links(self):
        self.sidebar_status()
        self.sidebar_configuration()
        self.sidebar_maintenance()
        self.sidebar_status()


class VideoPanel:
    @Property
    def button_play(self): return self.find_by(id="button_play")

    @Property
    def button_stop(self): return self.find_by(id="button_stop")

    @Property
    def button_window(self): return self.find_by(id="button_window")

    @Property
    def image(self): return self.find_by(id="video")

    @Property
    def camera_radio(self): return self.find_by(id="camera")

    @Property
    def sensor_radio(self): return self.find_by(id="sensor")

    @Property
    def zoom_in_btn(self): return self.find_by(id="button_zoom_in")

    @Property
    def zoom_out_btn(self): return self.find_by(id="button_zoom_out")

    @Property
    def arrow_left_btn(self): return self.find_by(id="button_arrow_left")

    @Property
    def arrow_right_btn(self): return self.find_by(id="button_arrow_right")

    @Property
    def arrow_up_btn(self): return self.find_by(id="button_arrow_up")

    @Property
    def arrow_down_btn(self): return self.find_by(id="button_arrow_up")


class AquetiAdminPageStatus(AquetiAdminPage):
    @Property
    def topbar_camera(self): return self.find_by(xpath="//*[@id='topbar']//a[contains(.,'Camera')]")

    @Property
    def topbar_storage(self): return self.find_by(xpath="//*[@id='topbar']//a[contains(.,'Storage')]")

    @Property
    def topbar_render(self): return self.find_by(xpath="//*[@id='topbar']//a[contains(.,'Render')]")

    def __init__(self, driver):
        AquetiAdminPage.__init__(self, driver)


class AquetiAdminPageConfiguration(AquetiAdminPage):
    @Property
    def topbar_system(self): return self.find_by(xpath="//*[@id='topbar']//a[contains(.,'System')]")

    @Property
    def topbar_camera(self): return self.find_by(xpath="//*[@id='topbar']//a[contains(.,'Camera')]")

    @Property
    def topbar_storage(self): return self.find_by(xpath="//*[@id='topbar']//a[contains(.,'Storage')]")

    @Property
    def topbar_render(self): return self.find_by(xpath="//*[@id='topbar']//a[contains(.,'Render')]")

    def __init__(self, driver):
        AquetiAdminPage.__init__(self, driver)


class AquetiAdminPageMaintenance(AquetiAdminPage):
    @Property
    def topbar_camera(self): return self.find_by(xpath="//*[@id='topbar']//a[contains(.,'Camera')]")

    @Property
    def topbar_storage(self): return self.find_by(xpath="//*[@id='topbar']//a[contains(.,'Storage')]")

    @Property
    def topbar_render(self): return self.find_by(xpath="//*[@id='topbar']//a[contains(.,'Render')]")

    @Property
    def update_software_btn(self): return self.find_by(css="button:contains(Update Software)")

    @Property
    def time_btn(self): return self.find_by(css="button:contains(Time)")

    @Property
    def system_btn(self): return self.find_by(css="button:contains(System)")

    @Property
    def time_set_host_time(self): return self.find_by(css="ul.dropdown-menu a:contains(Set Host Time)")

    @Property
    def time_specify_host_ntp(self): return self.find_by(css="ul.dropdown-menu a:contains(Specify Host NTP)")

    @Property
    def system_reboot_host_device(self): return self.find_by(css="ul.dropdown-menu a:contains(Reboot Host Device)")

    @Property
    def system_shutdown_host_device(self): return self.find_by(css="ul.dropdown-menu a:contains(Shutdown Host Device)")

    @Property
    def system_set_host_ip(self): return self.find_by(css="ul.dropdown-menu a:contains(Set Host IP)")

    @Property
    def search_field(self): return self.find_by(css="input.form-control[type='search']")

    @Property
    def show_entries_dd(self): return self.find_by(css="select[name='example_length']")

    @Property
    def previous(self): return self.find_by(partial_link_text="Previous")

    @Property
    def next(self): return self.find_by(partial_link_text="Next")

    @Property
    def time_sort(self): return self.find_by(xpath="//table[@id='example']//th[contains(.,'Time')]")

    @Property
    def type_sort(self): return self.find_by(xpath="//table[@id='example']//th[contains(.,'Type')]")

    @Property
    def location_sort(self): return self.find_by(xpath="//table[@id='example']//th[contains(.,'Location')]")

    @Property
    def message_sort(self): return self.find_by(xpath="//table[@id='example']//th[contains(.,'Message')]")

    @Property
    def entries_info(self): return self.find_by(id="example_info")

# Update Software

    @Property
    def us_upload_form(self): return self.find_by(id="upload")

    @Property
    def us_checksum_field(self): return self.find_by(id="checksum")

    @Property
    def us_upload_btn(self): return self.find_by(id="uploadButton")

# Time - Set Host Time

    @Property
    def sht_datetime_field(self): return self.find_by(css="div#set_host_time div.modal-body input.form_datetime")

    @Property
    def sht_update_btn(self): return self.find_by(css="div#set_host_time div.modal-footer button.btn-primary")

    @Property
    def sht_close_btn(self): return self.find_by(css="div#set_host_time div.modal-footer button.btn-secondary")

# Time - Specify Host NTP

    @Property
    def shn_ipv4_field(self): return self.find_by(css="div#set_host_NTP div.modal-body input.form-control")

    @Property
    def shn_update_btn(self): return self.find_by(css="div#set_host_NTP div.modal-footer button.btn-primary")

    @Property
    def shn_close_btn(self): return self.find_by(css="div#set_host_NTP div.modal-footer button.btn-secondary")

# System - Reboot Host Device

    @Property
    def rhd_reboot_btn(self): return self.find_by(css="div#reboot_host div.modal-footer button.btn-primary")

    @Property
    def rhd_close_btn(self): return self.find_by(css="div#reboot_host div.modal-footer button.btn-secondary")

# System - Shutdown Host Device

    @Property
    def shd_shutdown_btn(self): return self.find_by(css="div#shutdown_host div.modal-footer button.btn-primary")

    @Property
    def shd_close_btn(self): return self.find_by(css="div#shutdown_host div.modal-footer button.btn-secondary")

# System - Set Host IP

    @Property
    def shi_ipv4_field(self): return self.find_by(css="div#set_host_ip div.modal-body input.form-control")

    @Property
    def shi_update_btn(self): return self.find_by(css="div#set_host_ip div.modal-footer button.btn-primary")

    @Property
    def shi_close_btn(self): return self.find_by(css="div#set_host_ip div.modal-footer button.btn-secondary")

    def __init__(self, driver):
        AquetiAdminPage.__init__(self, driver)


class AquetiAdminPageRecordings(AquetiAdminPage, VideoPanel):
    @Property
    def components(self): return self.find_by(css="nav#combar li")

    @Property
    def update_nickname_pic(self): return self.find_by(css="a[data-target='#change_nickname']")

    @Property
    def show_entries_dd(self): return self.find_by(css="div#example_length select")

    @Property
    def search_field(self): return self.find_by(css="div#example_filter input")

    @Property
    def start_time_sort(self): return self.find_by(xpath="//table[@id='example']//th[contains(.,'Start Time')]")

    @Property
    def start_end_sort(self): return self.find_by(xpath="//table[@id='example']//th[contains(.,'End Time')]")

    @Property
    def entries(self): return self.find_by(css="table#example tr")

    @Property
    def entries_info(self): return self.find_by(id="example_info")

    @Property
    def previous(self): return self.find_by(id="example_previous")

    @Property
    def next(self): return self.find_by(id="example_next")

    # Edit Component

    @Property
    def ec_nickname_field(self): return self.find_by(css="div.modal-content input.form-control")

    @Property
    def ec_close_btn(self): return self.find_by(xpath="//button[contains(.,'Close')]")

    @Property
    def ec_update_btn(self): return self.find_by(xpath="//button[contains(.,'Update')]")

    def update_nickname(self, name):
        self.update_nickname_pic()
        self.ec_nickname_field(value=name)
        self.ec_update_btn()

    def __init__(self, driver):
        AquetiAdminPage.__init__(self, driver)

        self.page_url += "/system_recordings"


class AquetiAdminPageCamera(AquetiAdminPage):
    @Property
    def prop_status(self): return self.find_by(id="status")

    @Property
    def prop_recording(self): return self.find_by(id="recording")

    @Property
    def prop_serialid(self): return self.find_by(id="serial")

    @Property
    def prop_software(self): return self.find_by(id="software")

    @Property
    def prop_kernel(self): return self.find_by(id="kernel")

    @Property
    def prop_host(self): return self.find_by(id="host")

    @Property
    def host(self): return self.find_by(css="#host a")

    @Property
    def components(self): return self.find_by(css="nav#combar li")

    @Property
    def prop_cam_nickname(self): return self.find_by(id="nickname")

    @Property
    def prop_cam_model(self): return self.find_by(id="model")

    @Property
    def prop_cam_label(self): return self.find_by(id="label")

    @Property
    def nickname(self): return self.find_by(css="div.card>h1")

    @Property
    def update_nickname_pic(self): return self.find_by(css="a[data-target='#change_nickname']")

# Edit Component

    @Property
    def ec_nickname_field(self): return self.find_by(css="div.modal-content input.form-control")

    @Property
    def ec_close_btn(self): return self.find_by(xpath="//button[contains(.,'Close')]")

    @Property
    def ec_update_btn(self): return self.find_by(xpath="//button[contains(.,'Update')]")

    def update_nickname(self, name):
        self.update_nickname_pic()
        self.ec_nickname_field(value=name)
        self.ec_update_btn()

    def __init__(self, driver):
        AquetiAdminPage.__init__(self, driver)


class AquetiAdminPageStorage(AquetiAdminPage):
    @Property
    def prop_status(self): return self.find_by(id="status")

    @Property
    def prop_serialid(self): return self.find_by(id="id")

    @Property
    def prop_software(self): return self.find_by(id="software")

    @Property
    def prop_kernel(self): return self.find_by(id="kernel")

    @Property
    def prop_host(self): return self.find_by(id="host")

    @Property
    def components(self): return self.find_by(css="nav#combar li")

    @Property
    def update_nickname_pic(self): return self.find_by(css="a[data-target='#change_nickname']")

# Edit Component

    @Property
    def ec_nickname_field(self): return self.find_by(css="div.modal-content input.form-control")

    @Property
    def ec_close_btn(self): return self.find_by(xpath="//button[contains(.,'Close')]")

    @Property
    def ec_update_btn(self): return self.find_by(xpath="//button[contains(.,'Update')]")

    def __init__(self, driver):
        AquetiAdminPage.__init__(self, driver)


class AquetiAdminPageRender(AquetiAdminPage):
    @Property
    def prop_serialid(self): return self.find_by(id="id")

    @Property
    def prop_software(self): return self.find_by(id="software")

    @Property
    def prop_kernel(self): return self.find_by(id="kernel")

    @Property
    def prop_host(self): return self.find_by(id="host")

    @Property
    def components(self): return self.find_by(css="nav#combar li")

    @Property
    def update_nickname_pic(self): return self.find_by(css="a[data-target='#change_nickname']")

# Edit Component

    @Property
    def ec_nickname_field(self): return self.find_by(css="div.modal-content input.form-control")

    @Property
    def ec_close_btn(self): return self.find_by(xpath="//button[contains(.,'Close')]")

    @Property
    def ec_update_btn(self): return self.find_by(xpath="//button[contains(.,'Update')]")

    def __init__(self, driver):
        AquetiAdminPage.__init__(self, driver)


class AquetiAdminPageSystem(AquetiAdminPage):
    def __init__(self, driver):
        AquetiAdminPage.__init__(self, driver)


class AquetiAdminPageIssue(AquetiAdminPage):
    @Property
    def title_field(self): return self.find_by(id="title")  # Title

    @Property
    def summary_field(self): return self.find_by(id="summary")  # Summary

    @Property
    def description_field(self): return self.find_by(id="description")  # Description

    @Property
    def submit_btn(self): return self.find_by(id="submit")

    def __init__(self, driver):
        AquetiAdminPage.__init__(self, driver)

        self.page_url += "/submit_issue"

    def submit_issue(self, title, summary, description):
        self.title_field(value=title)
        self.summary_field(value=summary)
        self.description_field(value=description)
        self.submit_btn()

        return AquetiAdminPageStatusCamera(self)


class AquetiAdminPageStatusCamera(AquetiAdminPageStatus, AquetiAdminPageCamera):
    @Property
    def prop_sensor_model(self): return self.find_by(id="sensor_model")

    @Property
    def prop_sensor_host(self): return self.find_by(id="sensor_host")

    @Property
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
    @Property
    def node_graph(self): return self.find_by(id="node-graph")

    def __init__(self, driver):
        AquetiAdminPage.__init__(self, driver)

        self.page_url += "/pipeline_configuration"


class AquetiAdminPageConfigurationCamera(AquetiAdminPageConfiguration, AquetiAdminPageCamera, VideoPanel):
    @Property
    def prop_sensors(self): return self.find_by(id="sensor-svg")

    @Property
    def image_tab(self): return self.find_by(partial_link_text="Image")

    @Property
    def compression_tab(self): return self.find_by(partial_link_text="Compression")

    @Property
    def focus_tab(self): return self.find_by(partial_link_text="Focus")

    @Property
    def sensor_tab(self): return self.find_by(partial_link_text="Sensor")

# Image

    @Property
    def auto_gain_chkb(self): return self.find_by(id="auto_gain")

    @Property
    def gain_minus_btn(self): return self.find_by(
        xpath="//*[@id='panel1']//input[@id='auto_gain']/../..//button[contains(.,'-')]")

    @Property
    def gain_plus_btn(self): return self.find_by(
        xpath="//*[@id='panel1']//input[@id='auto_gain']/../..//button[contains(.,'+')]")

    @Property
    def gain_field(self): return self.find_by(id="gain")

    @Property
    def auto_whitebalance_chkb(self): return self.find_by(id="auto_whitebalance")

    @Property
    def whitebalance_minus_btn(self): return self.find_by(
        xpath="//*[@id='panel1']//input[@id='auto_whitebalance']/../..//button[contains(.,'-')]")

    @Property
    def whitebalance_plus_btn(self): return self.find_by(
        xpath="//*[@id='panel1']//input[@id='auto_whitebalance']/../..//button[contains(.,'+')]")

    @Property
    def whitebalance_field(self): return self.find_by(id="whitebalance")

    @Property
    def auto_shutter_chkb(self): return self.find_by(id="auto_shutter")

    @Property
    def shutter_minus_btn(self): return self.find_by(
        xpath="//*[@id='panel1']//input[@id='auto_shutter']/../..//button[contains(.,'-')]")

    @Property
    def shutter_plus_btn(self): return self.find_by(
        xpath="//*[@id='panel1']//input[@id='auto_shutter']/../..//button[contains(.,'+')]")

    @Property
    def shutter_field(self): return self.find_by(id="shutter")

    @Property
    def sharpening_slider(self): return self.find_by(css="#panel1 div#sharpening_slider div[role='slider']")

    @Property
    def sharpening_slider_ribbon(self): return self.find_by(css="#panel1 div#sharpening_slider div.noUi-base")

    @Property
    def denoising_slider(self): return self.find_by(css="#panel1 div#denoising_slider div[role='slider']")

    @Property
    def denoising_slider_ribbon(self): return self.find_by(css="#panel1 div#denoising_slider div.noUi-base")

    @Property
    def night_mode_chkb(self): return self.find_by(id="night_mode")

    @Property
    def transport_mode_10bit(self): return self.find_by(css="#panel1 button a:contains(10 bit)")

    @Property
    def transport_mode_12bit(self): return self.find_by(css="#panel1 button a:contains(12 bit)")

    @Property
    def framerate_25fps(self): return self.find_by(css="#panel1 button a:contains(25 fps)")

    @Property
    def framerate_30fps(self): return self.find_by(css="#panel1 button a:contains(30 fps)")

    @Property
    def transport_mode_dd(self): return self.find_by(id="transport_mode")

    @Property
    def framerate_dd(self): return self.find_by(id="framerate")

    def move_sharpening_slider(self, pos):
        move = ActionChains(self.driver)
        dx = self.sharpening_slider_ribbon.size["width"] / 100

        move.move_to_element(self.sharpening_slider).click_and_hold(self.sharpening_slider).move_by_offset(pos * dx, 0).release().perform()

    def move_denoising_slider(self, pos):
        move = ActionChains(self.driver)
        dx = self.denoising_slider_ribbon.size["width"] / 100

        move.move_to_element(self.denoising_slider).click_and_hold(self.denoising_slider).move_by_offset(pos * dx, 0).release().perform()

# Compression

    @Property
    def quality_high(self): return self.find_by(css="#panel2 a:contains(High)")

    @Property
    def quality_medium(self): return self.find_by(css="#panel2 a:contains(Medium)")

    @Property
    def quality_low(self): return self.find_by(css="#panel2 a:contains(Low)")

    @Property
    def encoding_jpeg(self): return self.find_by(css="#panel2 a:contains(JPEG)")

    @Property
    def encoding_h264(self): return self.find_by(css="#panel2 a:contains(H264)")

    @Property
    def encoding_h265(self): return self.find_by(css="#panel2 a:contains(H265)")

    @Property
    def quality_dd(self): return self.find_by(id="quality")

    @Property
    def encoding_dd(self): return self.find_by(id="encoding")

# Focus

    @Property
    def focus_chkb(self): return self.find_by(id="checkboxCustom2")

    @Property
    def focus_now_btn(self): return self.find_by(css="#panel3 button:contains(Focus Now)")

# Sensor

    @Property
    def focus_minus(self): return self.find_by(css="#panel4 button.btn.btn-default.bootstrap-touchspin-down:contains(-)")

    @Property
    def focus_plus(self): return self.find_by(css="#panel4 button.btn.btn-default.bootstrap-touchspin-up:contains(+)")

    @Property
    def focus_field(self): return self.find_by(id="sensorfocus")

    @Property
    def auto_focus_btn(self): return self.find_by(id="sensorAutoFocus")

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
