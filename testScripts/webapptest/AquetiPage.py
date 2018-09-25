from BasePage import *
from selenium.webdriver.common.action_chains import ActionChains


class AquetiPage(BasePage):
    @property
    def aqueti_lnk(self): return self.find_by(css="a[href='http://www.aqueti.com']")

    base_url = "http://10.0.0.232:5000"

    def __init__(self, *args):
        BasePage.__init__(self, *args)

        def __call__(self, text):
            super(BasePage, self).__call__()


class AquetiViewerPanel:
    @property
    def image(self): return self.find_by(id="video")

    @property
    def play_btn(self): return self.find_by(id="button_play")

    @property
    def step_back_btn(self): return self.find_by(id="button_step_back")

    @property
    def step_forward_btn(self): return self.find_by(id="button_step_forward")

    @property
    def live_btn(self): return self.find_by(id="button_live")

    @property
    def speed_dd(self): return self.find_by(css="button[data-id='speed']")

    @property
    def zoom_in_btn(self): return self.find_by(id="button_zoom_in")

    @property
    def zoom_out_btn(self): return self.find_by(id="button_zoom_out")

    @property
    def arrow_left_btn(self): return self.find_by(id="button_arrow_left")

    @property
    def arrow_right_btn(self): return self.find_by(id="button_arrow_right")

    @property
    def arrow_up_btn(self): return self.find_by(id="button_arrow_up")

    @property
    def arrow_down_btn(self): return self.find_by(id="button_arrow_up")

    @property
    def timeline(self): return self.find_by(id="visualization")

    def get_play_btn_status(self):
        return self.play_btn.find_element_by_tag_name('i').get_attribute("class").split(" ")[1][len('fa-'):]


class AquetiViewerPage(AquetiPage, AquetiViewerPanel):
    @property
    def cams_dd(self): return self.find_by(id="camera")

    @property
    def login_lnk(self): return self.find_by(id="login")

    @property
    def logo_pic(self): return self.find_by(id="logo")

    def get_camera_list(self):
        cams_names = ['/aqt/camera/' + i.text for i in self.cams_dd.find_elements_by_tag_name("option")]
        return cams_names

    def login(self):
        if self.cur_page_url == (self.base_url + "/login"):
            return AquetiLoginPage(self.test)

    page_url = AquetiPage.base_url
    page_title = "Aqueti View"

    def __init__(self, *args):
        AquetiPage.__init__(self, *args)


class AquetiLoginPage(AquetiPage):
    @property
    def username_field(self): return self.find_by(id="login-username")

    @property
    def password_field(self): return self.find_by(id="login-password")

    @property
    def login_btn(self): return self.find_by(css="form#login-form button[type='submit']")

    def login(self, username='admin', password='1234'):
        self.username_field(value=username)
        self.password_field(value=password)
        self.login_btn()
        if self.driver.current_url == AquetiAdminPageSystem.page_url:
            return AquetiAdminPageSystem(self.test)

    page_title = "Aqueti Admin"
    page_url = AquetiPage.base_url + "/login"

    def __init__(self, *args):
        AquetiPage.__init__(self, *args)


class AquetiAdminPage(AquetiPage):
    @property
    def sidebar_system_lnk(self): return self.find_by(partial_link_text="System")

    @property
    def sidebar_cameras_lnk(self): return self.find_by(partial_link_text="Cameras")

    @property
    def camera_list(self): return self.find_by(id="cameraDropdown")

    @property
    def sidebar_data_lnk(self): return self.find_by(partial_link_text="Data")

    @property
    def storage_list(self): return self.find_by(id="storageDropdown")

    @property
    def sidebar_render_lnk(self): return self.find_by(partial_link_text="Render")

    @property
    def render_list(self): return self.find_by(id="renderDropdown")

    @property
    def sidebar_logs_lnk(self): return self.find_by(partial_link_text="Logs")

    @property
    def system_current_time(self): return self.find_by(id="system-current-time")

    @property
    def thumbnail_btn(self): return self.find_by(css="button.sidebar-toggle")

    @property
    def submit_issue_lnk(self): return self.find_by(css="#navbarSupportedContent a:contains(Submit Issue)")

    @property
    def logout_lnk(self): return self.find_by(id="logout")

    @property
    def logo_pic(self): return self.find_by(id="logo")

    @property
    def settings_btn(self): return self.find_by(css='#navbarSupportedContent button')

# Web Server Settings
    
    @property
    def viewer_chkb(self): return self.find_by(id="viewer_enabled")

    @property
    def viewer_encoding_dd(self): return self.find_by(id="viewer_encoding")
    
    @property
    def viewer_width_field(self): return self.find_by(id="viewer_width")

    @property
    def viewer_width_minus(self): return self.find_by(xpath="//input[@id='viewer_width']/..//button[contains(.,'-')]")

    @property
    def viewer_width_plus(self): return self.find_by(xpath="//input[@id='viewer_width']/..//button[contains(.,'+')]")

    @property
    def viewer_height_field(self): return self.find_by(id="viewer_height")

    @property
    def viewer_height_minus(self): return self.find_by(xpath="//input[@id='viewer_height']/..//button[contains(.,'-')]")

    @property
    def viewer_height_plus(self): return self.find_by(xpath="//input[@id='viewer_height']/..//button[contains(.,'+')]")

    @property
    def viewer_framerate_field(self): return self.find_by(id="viewer_framerate")

    @property
    def viewer_framerate_minus(self): return self.find_by(xpath="//input[@id='viewer_framerate']/..//button[contains(.,'-')]")

    @property
    def viewer_framerate_plus(self): return self.find_by(xpath="//input[@id='viewer_framerate']/..//button[contains(.,'+')]")

    @property
    def viewer_close_btn(self): return self.find_by(css="button:contains(Close)")

    @property
    def viewer_update_btn(self): return self.find_by(css="button:contains(Update)")

    def __init__(self, *args):
        AquetiPage.__init__(self, *args)

        self.page_title = "Aqueti Admin"

    def logout(self):
        self.logout_lnk()

        return AquetiViewerPage(self.test)

    def click_links(self):
        self.sidebar_cameras()
        self.sidebar_data()
        self.sidebar_render()
        self.sidebar_logs()
        self.sidebar_system()

    def open_cam_page(self, cam_id):
        cam_links = [lnk for lnk in self.camera_list.find_elements_by_tag_name('a')]

        for lnk in cam_links:
            href = lnk.get_attribute("href")
            if href[href.rindex('/') + 1:] == cam_id:
                lnk.click()
                return AquetiAdminPageCamera(self.test)


class AquetiAdminPageSystem(AquetiAdminPage):
    @property
    def camera_list(self): return self.find_by(id="cameras")

    @property
    def storage_list(self): return self.find_by(id="storage")

    @property
    def render_list(self): return self.find_by(id="render")

    page_url = AquetiAdminPage.base_url + "/system"

    def __init__(self, *args):
        AquetiAdminPage.__init__(self, *args)


class AquetiAdminPageConfiguration(AquetiAdminPage):
    @property
    def topbar_system(self): return self.find_by(xpath="//*[@id='topbar']//a[contains(.,'System')]")

    @property
    def topbar_camera(self): return self.find_by(xpath="//*[@id='topbar']//a[contains(.,'Camera')]")

    @property
    def topbar_storage(self): return self.find_by(xpath="//*[@id='topbar']//a[contains(.,'Storage')]")

    @property
    def topbar_render(self): return self.find_by(xpath="//*[@id='topbar']//a[contains(.,'Render')]")

    def __init__(self, *args):
        AquetiAdminPage.__init__(self, *args)


class AquetiAdminPageMaintenance(AquetiAdminPage):
    @property
    def topbar_camera(self): return self.find_by(xpath="//*[@id='topbar']//a[contains(.,'Camera')]")

    @property
    def topbar_storage(self): return self.find_by(xpath="//*[@id='topbar']//a[contains(.,'Storage')]")

    @property
    def topbar_render(self): return self.find_by(xpath="//*[@id='topbar']//a[contains(.,'Render')]")

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

    @property
    def search_field(self): return self.find_by(css="input.form-control[type='search']")

    @property
    def show_entries_dd(self): return self.find_by(css="select[name='example_length']")

    @property
    def previous(self): return self.find_by(partial_link_text="Previous")

    @property
    def next(self): return self.find_by(partial_link_text="Next")

    @property
    def time_sort(self): return self.find_by(xpath="//table[@id='example']//th[contains(.,'Time')]")

    @property
    def type_sort(self): return self.find_by(xpath="//table[@id='example']//th[contains(.,'Type')]")

    @property
    def location_sort(self): return self.find_by(xpath="//table[@id='example']//th[contains(.,'Location')]")

    @property
    def message_sort(self): return self.find_by(xpath="//table[@id='example']//th[contains(.,'Message')]")

    @property
    def entries_info(self): return self.find_by(id="example_info")

# Update Software

    @property
    def us_upload_form(self): return self.find_by(id="upload")

    @property
    def us_checksum_field(self): return self.find_by(id="checksum")

    @property
    def us_upload_btn(self): return self.find_by(id="uploadButton")

# Time - Set Host Time

    @property
    def sht_datetime_field(self): return self.find_by(css="div#set_host_time div.modal-body input.form_datetime")

    @property
    def sht_update_btn(self): return self.find_by(css="div#set_host_time div.modal-footer button.btn-primary")

    @property
    def sht_close_btn(self): return self.find_by(css="div#set_host_time div.modal-footer button.btn-secondary")

# Time - Specify Host NTP

    @property
    def shn_ipv4_field(self): return self.find_by(css="div#set_host_NTP div.modal-body input.form-control")

    @property
    def shn_update_btn(self): return self.find_by(css="div#set_host_NTP div.modal-footer button.btn-primary")

    @property
    def shn_close_btn(self): return self.find_by(css="div#set_host_NTP div.modal-footer button.btn-secondary")

# System - Reboot Host Device

    @property
    def rhd_reboot_btn(self): return self.find_by(css="div#reboot_host div.modal-footer button.btn-primary")

    @property
    def rhd_close_btn(self): return self.find_by(css="div#reboot_host div.modal-footer button.btn-secondary")

# System - Shutdown Host Device

    @property
    def shd_shutdown_btn(self): return self.find_by(css="div#shutdown_host div.modal-footer button.btn-primary")

    @property
    def shd_close_btn(self): return self.find_by(css="div#shutdown_host div.modal-footer button.btn-secondary")

# System - Set Host IP

    @property
    def shi_ipv4_field(self): return self.find_by(css="div#set_host_ip div.modal-body input.form-control")

    @property
    def shi_update_btn(self): return self.find_by(css="div#set_host_ip div.modal-footer button.btn-primary")

    @property
    def shi_close_btn(self): return self.find_by(css="div#set_host_ip div.modal-footer button.btn-secondary")

    def __init__(self, *args):
        AquetiAdminPage.__init__(self, *args)


class AquetiAdminPageRecordings(AquetiAdminPage, AquetiViewerPanel):
    @property
    def components(self): return self.find_by(css="nav#combar li")

    @property
    def update_nickname_pic(self): return self.find_by(css="a[data-target='#change_nickname']")

    @property
    def show_entries_dd(self): return self.find_by(css="div#example_length select")

    @property
    def search_field(self): return self.find_by(css="div#example_filter input")

    @property
    def start_time_sort(self): return self.find_by(xpath="//table[@id='example']//th[contains(.,'Start Time')]")

    @property
    def start_end_sort(self): return self.find_by(xpath="//table[@id='example']//th[contains(.,'End Time')]")

    @property
    def entries(self): return self.find_by(css="table#example tr")

    @property
    def entries_info(self): return self.find_by(id="example_info")

    @property
    def previous(self): return self.find_by(id="example_previous")

    @property
    def next(self): return self.find_by(id="example_next")

    # Edit Component

    @property
    def ec_nickname_field(self): return self.find_by(css="div.modal-content input.form-control")

    @property
    def ec_close_btn(self): return self.find_by(xpath="//button[contains(.,'Close')]")

    @property
    def ec_update_btn(self): return self.find_by(xpath="//button[contains(.,'Update')]")

    def update_nickname(self, name):
        self.update_nickname_pic()
        self.ec_nickname_field(value=name)
        self.ec_update_btn()

    def __init__(self, *args):
        AquetiAdminPage.__init__(self, *args)

        self.page_url += "/system_recordings"


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
    def host(self): return self.find_by(css="#host a")

    @property
    def components(self): return self.find_by(css="nav#combar li")

    @property
    def prop_cam_nickname(self): return self.find_by(id="nickname")

    @property
    def prop_cam_model(self): return self.find_by(id="model")

    @property
    def prop_cam_label(self): return self.find_by(id="label")

    @property
    def nickname(self): return self.find_by(css="div.card>h1")

    @property
    def update_nickname_pic(self): return self.find_by(css="a[data-target='#change_nickname']")

    @property
    def settings(self): return self.find_by(id="headingSettings")

# Settings

    @property
    def auto_gain_chkb(self): return self.find_by(id="auto_gain")

    @property
    def auto_exposure_chkb(self): return self.find_by(id="auto_exposure_time")

    @property
    def auto_analog_gain_chkb(self): return self.find_by(id="auto_analog_gain")

    @property
    def whitebalance_mode_dd(self): return self.find_by(id="whitebalance_mode")

    @property
    def night_mode_chkb(self): return self.find_by(id="night_mode")

    @property
    def framerate_dd(self): return self.find_by(id="framerate")

    @property
    def sharpening_slider(self): return self.find_by(css="div#sharpening_slider div[role='slider']")

    @property
    def sharpening_slider_ribbon(self): return self.find_by(css="div#sharpening_slider div.noUi-base")

    @property
    def sharpening_slider_value(self): return self.find_by(css="div#sharpening_slider div[role='slider'] div.noUi-tooltip")

    @property
    def denoising_slider(self): return self.find_by(css="div#denoising_slider div[role='slider']")

    @property
    def denoising_slider_ribbon(self): return self.find_by(css="div#denoising_slider div.noUi-base")

    @property
    def denoising_slider_value(self): return self.find_by(css="div#denoising_slider div[role='slider'] div.noUi-tooltip")

    @property
    def saturation_slider(self): return self.find_by(css="div#saturation_slider div[role='slider']")

    @property
    def saturation_slider_ribbon(self): return self.find_by(css="div#saturation_slider div.noUi-base")

    @property
    def saturation_slider_value(self): return self.find_by(css="div#saturation_slider div[role='slider'] div.noUi-tooltip")

    @property
    def image_tab(self): return self.find_by(xpath="//a[contains(@class, 'nav-link') and contains(.,'Image')]")

    @property
    def compression_tab(self): return self.find_by(xpath="//a[contains(@class, 'nav-link') and contains(.,'Compression')]")

    @property
    def calibrate_tab(self): return self.find_by(xpath="//a[contains(@class, 'nav-link') and contains(.,'Calibrate')]")

    @property
    def focus_tab(self): return self.find_by(xpath="//a[contains(@class, 'nav-link') and contains(.,'Focus')]")

    @property
    def advanced_tab(self): return self.find_by(xpath="//a[contains(@class, 'nav-link') and contains(.,'Advanced')]")

# Calibrate tab

    @property
    def calibrate_btn(self): return self.find_by(id="modelGeneration")

    @property
    def set_model_btn(self): return self.find_by(id="setModel")

    @property
    def get_model_btn(self): return self.find_by(id="getModel")

    @property
    def reset_model_btn(self): return self.find_by(id="resetMod")

# Focus tab

    @property
    def ft_mode_btn(self): return self.find_by(xpath="//div[@id='panel4']//button[contains(.,'Mode')]")

    @property
    def ft_coarse_fine_lnk(self): return self.find_by(xpath="//a[contains(.,'Coarse + Fine')]")

# Advanced tab

    @property
    def settings_lnk(self): return self.find_by(xpath="//a[contains(@class, 'btn-primary') and contains(.,'Settings')]")

    def click_settings_link(self):
        self.settings_lnk()
        return AquetiAdminPageSensors(self.test)

# Edit Component

    @property
    def ec_close_btn(self): return self.find_by(xpath="//button[contains(.,'Close')]")

    @property
    def ec_update_btn(self): return self.find_by(xpath="//button[contains(.,'Update')]")

    def update_nickname(self, name):
        self.update_nickname_pic()
        self.ec_nickname_field(value=name)
        self.ec_update_btn()


    def __init__(self, *args):
        AquetiAdminPage.__init__(self, *args)


class AquetiAdminPageSensors(AquetiAdminPage):
    @property
    def sensor_list(self): return self.find_by(id="sensorList")

    @property
    def coarse_fine_focus_lnk(self): return self.find_by(xpath="//a[contains(., 'Coarse + Fine')]")

    #@property
    #def mode_focus_btn(self): return self.find_by(css="button.btn.btn-primary.dropdown-toggle[data-toggle='dropdown']")

    @property
    def sensor_settings(self): return self.find_by(xpath="//div[contains(@class,'card-header') and contains(., 'Sensor Settings')]")

    @property
    def focus_val_input(self): return self.find_by(id="sensorfocus")

    @property
    def camera_page_lnk(self): return self.find_by(xpath="//div[contains(@class,'container-fluid')]//a[contains(@href, '/camera/')]")

    @property
    def focus_plus_btn(self): return self.find_by(xpath="//div[contains(@class, 'card-header') and contains(., 'Sensor Settings')]/..//button[contains(.,'+')]")

    def select_sensor(self, sensor_name):
        self.find_by(xpath="//ul[@id='sensorList']/li[contains(.,'" + str(sensor_name) + "')]")()

    def click_camera_page_lnk(self):
        self.camera_page_lnk()
        return AquetiAdminPageCamera(self.test)



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

    @property
    def update_nickname_pic(self): return self.find_by(css="a[data-target='#change_nickname']")

# Edit Component

    @property
    def ec_nickname_field(self): return self.find_by(css="div.modal-content input.form-control")

    @property
    def ec_close_btn(self): return self.find_by(xpath="//button[contains(.,'Close')]")

    @property
    def ec_update_btn(self): return self.find_by(xpath="//button[contains(.,'Update')]")

    def __init__(self, *args):
        AquetiAdminPage.__init__(self, *args)


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

    @property
    def update_nickname_pic(self): return self.find_by(css="a[data-target='#change_nickname']")

# Edit Component

    @property
    def ec_nickname_field(self): return self.find_by(css="div.modal-content input.form-control")

    @property
    def ec_close_btn(self): return self.find_by(xpath="//button[contains(.,'Close')]")

    @property
    def ec_update_btn(self): return self.find_by(xpath="//button[contains(.,'Update')]")

    def __init__(self, *args):
        AquetiAdminPage.__init__(self, *args)


class AquetiAdminPageIssue(AquetiAdminPage):
    @property
    def title_field(self): return self.find_by(id="title")  # Title

    @property
    def summary_field(self): return self.find_by(id="summary")  # Summary

    @property
    def description_field(self): return self.find_by(id="description")  # Description

    @property
    def submit_btn(self): return self.find_by(id="submit")

    def __init__(self, *args):
        AquetiAdminPage.__init__(self, *args)

        self.page_url += "/submit_issue"

    def submit_issue(self, title, summary, description):
        self.title_field(value=title)
        self.summary_field(value=summary)
        self.description_field(value=description)
        self.submit_btn()

        return AquetiAdminPageStatusCamera(self.test)


class AquetiAdminPageStatusCamera(AquetiAdminPageCamera):
    @property
    def prop_sensor_model(self): return self.find_by(id="sensor_model")

    @property
    def prop_sensor_host(self): return self.find_by(id="sensor_host")

    @property
    def prop_sensors(self): return self.find_by(id="sensor-svg")

    def __init__(self, *args):
        AquetiAdminPage.__init__(self, *args)

        self.page_url += "/scop_status"


class AquetiAdminPageStatusStorage(AquetiAdminPageStorage):
    def __init__(self, *args):
        AquetiAdminPage.__init__(self, *args)

        self.page_url += "/storage_status"


class AquetiAdminPageStatusRender(AquetiAdminPageRender):
    def __init__(self, *args):
        AquetiAdminPage.__init__(self, *args)

        self.page_url += "/render_status"


class AquetiAdminPageConfigurationSystem(AquetiAdminPageConfiguration, AquetiAdminPageSystem):
    @property
    def node_graph(self): return self.find_by(id="node-graph")

    def __init__(self, *args):
        AquetiAdminPage.__init__(self, *args)

        self.page_url += "/pipeline_configuration"


class AquetiAdminPageConfigurationCamera(AquetiAdminPageConfiguration, AquetiAdminPageCamera, AquetiViewerPanel):
    @property
    def prop_sensors(self): return self.find_by(id="sensor-svg")

    @property
    def image_tab(self): return self.find_by(partial_link_text="Image")

    @property
    def compression_tab(self): return self.find_by(partial_link_text="Compression")

    @property
    def focus_tab(self): return self.find_by(partial_link_text="Focus")

    @property
    def sensor_tab(self): return self.find_by(partial_link_text="Sensor")

# Image

    @property
    def auto_gain_chkb(self): return self.find_by(id="auto_gain")

    @property
    def gain_minus_btn(self): return self.find_by(
        xpath="//*[@id='panel1']//input[@id='auto_gain']/../..//button[contains(.,'-')]")

    @property
    def gain_plus_btn(self): return self.find_by(
        xpath="//*[@id='panel1']//input[@id='auto_gain']/../..//button[contains(.,'+')]")

    @property
    def gain_field(self): return self.find_by(id="gain")

    @property
    def auto_whitebalance_chkb(self): return self.find_by(id="auto_whitebalance")

    @property
    def whitebalance_minus_btn(self): return self.find_by(
        xpath="//*[@id='panel1']//input[@id='auto_whitebalance']/../..//button[contains(.,'-')]")

    @property
    def whitebalance_plus_btn(self): return self.find_by(
        xpath="//*[@id='panel1']//input[@id='auto_whitebalance']/../..//button[contains(.,'+')]")

    @property
    def whitebalance_field(self): return self.find_by(id="whitebalance")

    @property
    def auto_shutter_chkb(self): return self.find_by(id="auto_shutter")

    @property
    def shutter_minus_btn(self): return self.find_by(
        xpath="//*[@id='panel1']//input[@id='auto_shutter']/../..//button[contains(.,'-')]")

    @property
    def shutter_plus_btn(self): return self.find_by(
        xpath="//*[@id='panel1']//input[@id='auto_shutter']/../..//button[contains(.,'+')]")

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
    def transport_mode_dd(self): return self.find_by(id="transport_mode")

    @property
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
    def focus_chkb(self): return self.find_by(id="checkboxCustom2")

    @property
    def focus_now_btn(self): return self.find_by(css="#panel3 button:contains(Focus Now)")

# Sensor

    @property
    def focus_minus(self): return self.find_by(css="#panel4 button.btn.btn-default.bootstrap-touchspin-down:contains(-)")

    @property
    def focus_plus(self): return self.find_by(css="#panel4 button.btn.btn-default.bootstrap-touchspin-up:contains(+)")

    @property
    def focus_field(self): return self.find_by(id="sensorfocus")

    @property
    def auto_focus_btn(self): return self.find_by(id="sensorAutoFocus")

    def __init__(self, *args):
        AquetiAdminPage.__init__(self, *args)

        self.page_url += "/scop_configuration"


class AquetiAdminPageConfigurationStorage(AquetiAdminPageConfiguration, AquetiAdminPageStorage):
    def __init__(self, *args):
        AquetiAdminPage.__init__(self, *args)

        self.page_url += "/storage_configuration"


class AquetiAdminPageConfigurationRender(AquetiAdminPageConfiguration, AquetiAdminPageRender):

    def __init__(self, *args):
        AquetiAdminPage.__init__(self, *args)

        self.page_url += "/render_configuration"


class AquetiAdminPageMaintenanceCamera(AquetiAdminPageMaintenance, AquetiAdminPageCamera):

    def __init__(self, *args):
        AquetiAdminPage.__init__(self, *args)

        self.page_url += "/scop_maintenance"


class AquetiAdminPageMaintenanceStorage(AquetiAdminPageMaintenance, AquetiAdminPageStorage):

    def __init__(self, *args):
        AquetiAdminPage.__init__(self, *args)

        self.page_url += "/storage_maintenance"


class AquetiAdminPageMaintenanceRender(AquetiAdminPageMaintenance, AquetiAdminPageRender):

    def __init__(self, *args):
        AquetiAdminPage.__init__(self, *args)

        self.page_url += "/render_maintenance"
