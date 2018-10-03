from BasePage import *
from selenium.webdriver.common.action_chains import ActionChains


class QAdminSidebar:
    @property
    def dashboard_lnk(self): return self.find_by(xpath="(//aside//div[contains(.,'Dashboard')])[last()]")

    @property
    def camera_lnk(self): return self.find_by(id="camera_page")

    @property
    def cam_reservations_lnk(self): return self.find_by(id="camera_reservations_page")

    @property
    def cam_settings_lnk(self): return self.find_by(id="camera_settings_page")

    @property
    def cam_microcameras_lnk(self): return self.find_by(id="camera_microcamera_page")

    @property
    def storage_lnk(self): return self.find_by(id="storage_page")

    @property
    def storage_settings_lnk(self): return self.find_by(id="storage_settings_page")

    @property
    def render_lnk(self): return self.find_by(id="render_page")

    @property
    def render_settings_lnk(self): return self.find_by(id="render_settings_page")

    @property
    def render_streams_lnk(self): return self.find_by(id="render_streams_page")

    @property
    def system_lnk(self): return self.find_by(id="system_page")

    @property
    def system_device_lnk(self): return self.find_by(id="device_page")

    @property
    def reservations_lnk(self): return self.find_by(id="reservations_page")

    @property
    def logs_lnk(self): return self.find_by(id="logs_page")

    def menu_dashboard(self):
        self.dashboard_lnk()

        return QAdminDashboard(self.test)

    def menu_camera(self):
        self.camera_lnk()

        while not self.cam_reservations_lnk.is_displayed():
            time.sleep(0.5)

        return QAdminCamera(self.test)

    def menu_cam_reservations(self):
        self.camera_lnk()

        while not self.cam_reservations_lnk.is_displayed():
            time.sleep(0.5)

        self.cam_reservations_lnk()

        return QAdminCameraReservations(self.test)

    def menu_cam_settings(self):
        if not self.cam_settings_lnk.is_displayed():
            self.menu_camera()
            time.sleep(0.5)

        self.cam_settings_lnk()

        return QAdminCameraSettings(self.test)

    def menu_cam_microcameras(self):
        self.cam_microcameras_lnk()

        return QAdminCameraMicrocameras(self.test)


class QAdminPage(BasePage, QAdminSidebar):
    @property
    def side_icon(self): return self.find_by(css="button.v-toolbar__side-icon.v-btn.v-btn--icon div.v-btn__content")

    @property
    def q_lnk(self): return self.find_by(css="a.d-flex.router-link-active")

    @property
    def version_fld(self): return self.find_by(css="span.v-chip__content")

    @property
    def toggle_sidebar_icon(self): return self.find_by(css="span.v-tooltip.v-tooltip--bottom:nth-child(2n)")

    @property
    def ping_time_fld(self): return self.find_by(css="span.v-tooltip.v-tooltip--bottom:nth-child(3n)")

    @property
    def submit_issue_icon(self): return self.find_by(css="div.v-dialog__activator div.v-btn__content")

    @property
    def locale_dd(self): return self.find_by(css="input[aria-label='Locale']")

    @property
    def aqueti_lnk(self): return self.find_by(css="a[href='http://www.aqueti.com']")

    base_url = "http://10.0.0.232:5000/#/"

    def __init__(self, *args):
        BasePage.__init__(self, *args)

        def __call__(self, text):
            super(BasePage, self).__call__()


class QAdminDashboard(QAdminPage):
    @property
    def d_system_lnk(self): return self.find_by(xpath="//div[contains(@class,'container')]//a[contains(.,'System')]")

    @property
    def d_camera_lnk(self): return self.find_by(xpath="//div[contains(@class,'container')]//a[contains(.,'Camera')]")

    @property
    def d_storage_lnk(self): return self.find_by(xpath="//div[contains(@class,'container')]//a[contains(.,'Storage')]")

    @property
    def d_render_lnk(self): return self.find_by(xpath="//div[contains(@class,'container')]//a[contains(.,'Render')]")

    @property
    def system_status_pic(self): return self.find_by(xpath="//div[contains(@class,'container')]//a[contains(.,'System')]/../div//span")

    @property
    def camera_status_pic(self): return self.find_by(xpath="//div[contains(@class,'container')]//a[contains(.,'Camera')]/../div//span")

    @property
    def storage_status_pic(self): return self.find_by(xpath="//div[contains(@class,'container')]//a[contains(.,'Storage')]/../div//span")

    @property
    def render_status_pic(self): return self.find_by(xpath="//div[contains(@class,'container')]//a[contains(.,'Render')]/../div//span")

    @property
    def system_devices(self): return self.find_by(xpath="(//div[contains(@class,'container')]//a[contains(.,'System')]/../span)[1]")

    @property
    def system_version(self): return self.find_by(xpath="(//div[contains(@class,'container')]//a[contains(.,'System')]/../span)[2]")

    @property
    def camera_devices(self): return self.find_by(xpath="//div[contains(@class,'container')]//a[contains(.,'Camera')]/../span)[1]")

    @property
    def camera_version(self): return self.find_by(xpath="//div[contains(@class,'container')]//a[contains(.,'Camera')]/../span)[2]")

    @property
    def storage_devices(self): return self.find_by(xpath="//div[contains(@class,'container')]//a[contains(.,'Storage')]/../span)[1]")

    @property
    def storage_version(self): return self.find_by(xpath="//div[contains(@class,'container')]//a[contains(.,'Storage')]/../span)[2]")

    @property
    def render_devices(self): return self.find_by(xpath="//div[contains(@class,'container')]//a[contains(.,'Render')]/../span)[1]")

    @property
    def render_version(self): return self.find_by(xpath="//div[contains(@class,'container')]//a[contains(.,'Render')]/../span)[2]")

    def click_system_lnk(self):
        self.system_lnk()

        return QAdminSystem(self.test)

    def click_camera_lnk(self):
        self.camera_lnk()

        return QAdminCamera(self.test)

    def click_storage_lnk(self):
        self.storage_lnk()

        return QAdminStorage(self.test)

    def click_render_lnk(self):
        self.render_lnk()

        return QAdminRender(self.test)

    page_url = QAdminPage.base_url
    page_title = "qadmin"

    def __init__(self, *args):
        QAdminPage.__init__(self, *args)


class QAdminCamera(QAdminPage):
    def get_status_indicator(self, cam_id):
        return self.find_by(xpath="//li[@class='v-expansion-panel__container']//div[contains(@class, 'headline') and contains(.,'/aqt/camera/" + cam_id + "')]")

    def get_expand_icon(self, cam_id):
        return self.find_by(xpath="//li[@class='v-expansion-panel__container']//*[contains(.,'/aqt/camera/" + cam_id + "')]//div[@class='v-expansion-panel__header__icon']")

    def get_steaming_icon(self, cam_id):
        return self.find_by(xpath="(//li[@class='v-expansion-panel__container']//div[contains(@class, 'v-expansion-panel__header') and contains(.,'/aqt/camera/" + cam_id + "')]//i[contains(@class,'pr-2')])[1]")

    def get_recording_icon(self, cam_id):
        return self.find_by(xpath="(//li[@class='v-expansion-panel__container']//div[contains(@class, 'v-expansion-panel__header') and contains(.,'/aqt/camera/" + cam_id + "')]//i[contains(@class,'pr-2')])[2]")

    def get_mcams_label(self, cam_id):
        return self.find_by(xpath="//li[@class ='v-expansion-panel__container']//div[contains(@class ,'v-expansion-panel__header') and contains(., '/aqt/camera/" + cam_id + "')]//div[contains(@class,'text-xs-right')]")


    def get_mcams_number(self, cam_id):
        e = self.get_mcams_label(cam_id)
        if e is not None:
            arr = e.text.split("\n")
            if len(arr) > 0:
                return arr[len(arr) - 1].strip().split("/")
        else:
            return ""

    def get_stream_status(self, cam_id):
        e = self.get_steaming_icon(cam_id)
        cls = e.get_attribute("class")
        if "green--text" in cls:
            return True
        else:
            return False

    def get_rec_status(self, cam_id):
        e = self.get_recording_icon(cam_id)
        cls = e.get_attribute("class")
        if "red--text" in cls:
            return True
        else:
            return False

    page_url = QAdminPage.base_url + "camera"
    page_title = "qadmin"

    def __init__(self, *args):
        QAdminPage.__init__(self, *args)


class QAdminStreamBox:
    @property
    def video_box(self): return self.find_by(id="playerCanvas")

    @property
    def cam_select_dd(self): return self.find_by(id="camera_select")

    @property
    def camera_dd(self): return self.find_by(xpath="//div[@role='combobox']//label[contains(.,'Camera')]/..")

    def get_dd_value(self, val_id):
        return self.find_by(xpath="//div[contains(@class,'v-list__tile__title') and contains(.,'" + val_id + "')]")


class QAdminCameraReservations(QAdminPage, QAdminStreamBox):
    @property
    def reserv_panel(self): return self.find_by(xpath="//nav[contains(@class,'v-toolbar grey darken-4')]//button[contains(@class,'v-toolbar__side-icon v-btn v-btn--icon')]")

    @property
    def recording_chkb(self): return self.find_by(xpath="//input[@aria-label='Recording']/../div[contains(@class,'v-input--selection-controls__ripple')]")

    @property
    def track_chkb(self): return self.find_by(xpath="//input[@aria-label='Track']/../div[contains(@class,'v-input--selection-controls__ripple')]")

    @property
    def play_pause_btn(self): return self.find_by(id="play_pause")

    @property
    def step_frame_back_chkb(self): return self.find_by(id="skip_previous")

    @property
    def step_frame_forward_chkb(self): return self.find_by(id="skip_next")

    @property
    def live_btn(self): return self.find_by(id="live")

    @property
    def speed_dd(self): return self.find_by(xpath="//div[@role='combobox']//label[contains(.,'Speed')]/..")

    page_url = QAdminPage.base_url + "camera_reservations/none"
    page_title = "qadmin"

    def __init__(self, *args):
        QAdminPage.__init__(self, *args)


class QAdminCameraSettings(QAdminPage, QAdminStreamBox):
    @property
    def image_tab(self): return self.find_by(xpath="//nav//a[contains(.,'Image')]")

    @property
    def compression_tab(self): return self.find_by(xpath="//nav//a[contains(.,'Compression')]")

    @property
    def calibrate_tab(self): return self.find_by(xpath="//nav//a[contains(.,'Calibrate')]")

    @property
    def focus_tab(self): return self.find_by(xpath="//nav//a[contains(.,'Focus')]")

# Image

    @property
    def compression_dd(self): return self.find_by(id="quality_select")

# Compression

    @property
    def ct_calibrate_btn(self): return self.find_by(id="calibrate_now_btn")

# Calibrate

    @property
    def ct_calibrate_btn(self): return self.find_by(id="calibrate_now_btn")

    @property
    def ct_save_geom_btn(self): return self.find_by(id="save_geometry_btn")

    @property
    def ct_set_geom_btn(self): return self.find_by(id="set_geometry_btn")

    @property
    def ct_reset_geom_btn(self): return self.find_by(id="reset_geometry_btn")

# Focus

    @property
    def ft_coarse_btn(self): return self.find_by(id="focus_coarse_btn")

    @property
    def ft_fine_btn(self): return self.find_by(id="focus_fine_btn")


    page_url = QAdminPage.base_url + "camera_settings/none"
    page_title = "qadmin"

    def __init__(self, *args):
        QAdminPage.__init__(self, *args)


class QAdminCameraMicrocameras(QAdminPage):
    page_url = QAdminPage.base_url + "camera_microcameras/none"
    page_title = "qadmin"

    def __init__(self, *args):
        QAdminPage.__init__(self, *args)


class QAdminStorage(QAdminPage):
    page_url = QAdminPage.base_url + "storage"
    page_title = "qadmin"

    def __init__(self, *args):
        QAdminPage.__init__(self, *args)


class QAdminStorageSettings(QAdminPage):
    page_url = QAdminPage.base_url + "storage_settings/none"
    page_title = "qadmin"

    def __init__(self, *args):
        QAdminPage.__init__(self, *args)


class QAdminRender(QAdminPage):
    page_url = QAdminPage.base_url + "render"
    page_title = "qadmin"

    def __init__(self, *args):
        QAdminPage.__init__(self, *args)


class QAdminRenderSettings(QAdminPage):
    page_url = QAdminPage.base_url + "render_settings/none"
    page_title = "qadmin"

    def __init__(self, *args):
        QAdminPage.__init__(self, *args)


class QAdminRenderStreams(QAdminPage):
    page_url = QAdminPage.base_url + "render_streams/none"
    page_title = "qadmin"

    def __init__(self, *args):
        QAdminPage.__init__(self, *args)


class QAdminSystem(QAdminPage):
    page_url = QAdminPage.base_url + "system"
    page_title = "qadmin"

    def __init__(self, *args):
        QAdminPage.__init__(self, *args)


class QAdminSystemDevice(QAdminPage):
    page_url = QAdminPage.base_url + "device/none"
    page_title = "qadmin"

    def __init__(self, *args):
        QAdminPage.__init__(self, *args)


class QAdminReservations(QAdminPage):
    page_url = QAdminPage.base_url + "reservations"
    page_title = "qadmin"

    def __init__(self, *args):
        QAdminPage.__init__(self, *args)


class QAdminLogs(QAdminPage):
    page_url = QAdminPage.base_url + "logs"
    page_title = "qadmin"

    def __init__(self, *args):
        QAdminPage.__init__(self, *args)
