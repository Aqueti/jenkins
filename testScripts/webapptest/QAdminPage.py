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
    def device_lnk(self): return self.find_by(id="device_page")

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

    def menu_storage(self):
        self.storage_lnk()

        while not self.storage_settings_lnk.is_displayed():
            time.sleep(0.5)

        return QAdminStorage(self.test)

    def menu_render(self):
        self.render_lnk()

        while not self.render_settings_lnk.is_displayed():
            time.sleep(0.5)

        return QAdminRender(self.test)

    def menu_device(self):
        self.device_lnk()

        return QAdminDevice(self.test)

    def menu_reservations(self):
        self.reservations_lnk()

        return QAdminReservations(self.test)

    def menu_logs(self):
        self.logs_lnk()

        return QAdminLogs(self.test)

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
        if not self.cam_microcameras_lnk.is_displayed():
            self.menu_camera()
            time.sleep(0.5)

        self.cam_microcameras_lnk()

        return QAdminCameraMicrocameras(self.test)

    def menu_storage_settings(self):
        if not self.storage_settings_lnk.is_displayed():
            self.menu_storage()
            time.sleep(0.5)

        self.storage_settings_lnk()

        return QAdminStorageSettings(self.test)

    def menu_render_settings(self):
        if not self.render_settings_lnk.is_displayed():
            self.menu_render()
            time.sleep(0.5)

        self.render_settings_lnk()

        return QAdminRenderSettings(self.test)

    def menu_render_streams(self):
        if not self.render_streams_lnk.is_displayed():
            self.menu_render()
            time.sleep(0.5)

        self.render_streams_lnk()

        return QAdminRenderStreams(self.test)

    def menu_system_device(self):
        if not self.system_device_lnk.is_displayed():
            self.menu_system()
            time.sleep(0.5)

        self.render_streams_lnk()

        return QAdminRenderStreams(self.test)


class QPage:
    def get_dd_elem(self, val, is_contain=True):
        if is_contain:
            return self.find_by(xpath="//a[contains(@class, 'v-list__tile--link')]//div[contains(., '" + val + "')]//parent::a")
        else:
            return self.find_by(xpath="//a[contains(@class, 'v-list__tile--link')]//div[text()='" + val + "']//parent::a")


class QStreamBox(QPage):
    @property
    def video_box(self): return self.find_by(id="playerCanvas")

    @property
    def cam_select_dd(self): return self.find_by(id="camera_select")

    @property
    def camera_dd(self): return self.find_by(xpath="//div[@role='combobox']//label[contains(.,'Camera')]/..")

    def get_slider(self, val):
        return self.find_by("//input[@aria-label='" + val + "']/../../../../..//input[@role='slider']/../div[contains(@class,'v-slider__thumb-container')]")


class QViewPage(BasePage, QStreamBox):
    pass


class QAdminPage(BasePage, QPage, QAdminSidebar):
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
    def submit_issue_icon(self): return self.find_by(xpath="//i[contains(., 'report_problem')]")

# Submit Issue

    @property
    def si_filename_txt(self): return self.find_by(css="input[aria-label='Filename']")

    @property
    def si_summary_txt(self): return self.find_by(css="textarea[aria-label='Summary']")

    @property
    def si_description_txt(self): return self.find_by(css="textarea[aria-label='Description']")

    @property
    def si_submit_btn(self): return self.find_by(xpath="//div[contains(@class, 'v-dialog--active')]//button[contains(., 'Submit')]")

    @property
    def si_close_btn(self): return self.find_by(xpath="//div[contains(@class, 'v-dialog--active')]//button[contains(., 'Close')]")

# Settings

    @property
    def settings_icon(self): return self.find_by(css="div.v-menu__activator button")

    @property
    def customize_stream_btn(self): return self.find_by(xpath="//div[@class = 'v-list__tile' and contains(., 'Customize Stream')]//div[@class = 'v-list__tile__action']//i")

    @property
    def refresh_stream_btn(self): return self.find_by(xpath="//div[@class = 'v-list__tile' and contains(., 'Refresh Stream')]//div[@class = 'v-list__tile__action']//i")

    @property
    def cs_update_btn(self): return self.find_by(xpath="//button/div[contains(., 'Update')]")

    @property
    def cs_cancel_btn(self): return self.find_by(xpath="//button/div[contains(., 'Cancel')]")

    @property
    def type_dd(self): return self.find_by(xpath="//div[contains(@class, 'v-dialog--active')]//label[contains(., 'Type')]/..")

    @property
    def display_dd(self): return self.find_by(xpath="//div[contains(@class, 'v-dialog--active')]//label[contains(., 'Display')]/..")

    @property
    def framerate_dd(self): return self.find_by(xpath="//div[contains(@class, 'v-dialog--active')]//label[contains(., 'Framerate')]/..")

    @property
    def projection_dd(self): return self.find_by(xpath="//div[contains(@class, 'v-dialog--active')]//label[contains(., 'Projection')]/..")


    @property
    def locale_dd(self): return self.find_by(css="input[aria-label='Locale']")

    @property
    def aqueti_lnk(self): return self.find_by(css="a[href='http://www.aqueti.com']")

    base_url = ""

    def submit_issue(self, *args, **kwargs):
        self.si_filename_txt(value=kwargs["filename"])
        self.si_summary_txt(value=kwargs["summary"])
        self.si_description_txt(value=kwargs["description"])

        self.si_submit_btn()

    def __init__(self, *args):
        BasePage.__init__(self, *args)

        if len(args) > 0:
            self.base_url = "http://" + args[0].env.render.ip + "/admin/#/"

        print(self.base_url)
        print()

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


class QAdminCameraReservations(QAdminPage, QStreamBox):
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


class QAdminCameraSettings(QAdminPage, QStreamBox):
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
    def global_chkb(self): return self.find_by(xpath="//input[@id='global_switch']/../div[contains(@class,'v-input--selection-controls__ripple')]")

    @property
    def global_txt(self): return self.find_by(id="global_text_field")

    @property
    def exposure_chkb(self): return self.find_by(xpath="//input[@id='exposure_time_switch']/../div[contains(@class,'v-input--selection-controls__ripple')]")

    @property
    def exposure_txt(self): return self.find_by(id="exposure_time_text_field")

    @property
    def analog_gain_chkb(self): return self.find_by(xpath="//input[@id='analog_gain_switch']/../div[contains(@class,'v-input--selection-controls__ripple')]")

    @property
    def analog_gain_txt(self): return self.find_by(id="analog_gain_text_field")

    @property
    def digital_gain_txt(self): return self.find_by(id="digital_gain_text_field")

    @property
    def sharpening_txt(self): return self.find_by(id="sharpening_text_field")

    @property
    def denoising_txt(self): return self.find_by(id="denoising_text_field")

    @property
    def denoising_txt(self): return self.find_by(id="denoising_text_field")

    @property
    def saturation_txt(self): return self.find_by(id="saturation_text_field")

    @property
    def night_mode_chkb(self): return self.find_by(xpath="//input[@id='night_mode_switch']/../div[contains(@class,'v-input--selection-controls__ripple')]")

    @property
    def framerate_dd(self): return self.find_by(xpath="//input[@id='framerate_select']/../../div[@class='v-input__append-inner']")

    @property
    def whitebalance_dd(self): return self.find_by(xpath="//input[@id='whitebalance_select']/../../div[@class='v-input__append-inner']")

# Compression

    @property
    def compression_dd(self): return self.find_by(xpath="//input[@id='quality_select']/../../div[@class='v-input__append-inner']")

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


class QAdminCameraMicrocameras(QAdminPage, QStreamBox):
    @property
    def microcamera_dd(self): return self.find_by(xpath="//input[@id='microcamera_select']/../../div[@class='v-input__append-inner']")

    @property
    def microcamera_device_lnk(self): return self.find_by(id="microcamera_device")

    @property
    def model_value(self): return self.find_by(xpath="//span[@class='v-chip grey lighten-1']//span[contains(.,'Model')]")

    @property
    def gain_value(self): return self.find_by(xpath="//span[@class='v-chip grey lighten-1']//span[contains(.,'Gain')]")

    @property
    def gain_value(self): return self.find_by(xpath="//span[@class='v-chip grey lighten-1']//span[contains(.,'Exposure Time')]")

    @property
    def focus_txt(self): return self.find_by(id="focus_text_field")

    @property
    def focus_coarse_btn(self): return self.find_by(id="focus_coarse_btn")

    @property
    def focus_fine_btn(self): return self.find_by(id="focus_fine_btn")

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
    @property
    def storage_dd(self): return self.find_by(xpath="//input[@id='storage_select']/../../div[@class='v-input__append-inner']")

    @property
    def block_size_txt(self): return self.find_by(id="block_size_text_field")

    @property
    def blocks_per_cont_txt(self): return self.find_by(id="blocks_per_container_text_field")

    @property
    def max_storage_threads_txt(self): return self.find_by(id="max_storage_threads_text_field")

    @property
    def cache_size_txt(self): return self.find_by(id="cache_size_text_field")

    @property
    def garbage_collection_threshold_txt(self): return self.find_by(id="garbage_collection_threshold_text_field")

    @property
    def garbage_collection_interval_txt(self): return self.find_by(id="garbage_collection_interval_text_field")

    @property
    def maximum_disk_usage_txt(self): return self.find_by(id="maximum_disk_usage_text_field")

    page_url = QAdminPage.base_url + "storage_settings/none"
    page_title = "qadmin"

    def __init__(self, *args):
        QAdminPage.__init__(self, *args)


class QAdminRender(QAdminPage):
    def get_expand_icon(self, render_id):
        return self.find_by(xpath="//li[contains(@class,'v-expansion-panel__container')]//*[contains(.,'/aqt/render/" + render_id + "')]//div[@class='v-expansion-panel__header__icon']")

    def get_render_id_value(self, render_id):
        return self.find_by(xpath="//li[contains(@class,'v-expansion-panel__container')]//*[contains(.,'/aqt/render/" + render_id + "')]//div[contains(@class,'v-card__title v-card__title--primary')]/span[contains(.,'ID')]")

    def get_render_version_value(self, render_id):
        return self.find_by(xpath="//li[contains(@class,'v-expansion-panel__container')]//*[contains(.,'/aqt/render/" + render_id + "')]//div[contains(@class,'v-card__title v-card__title--primary')]/span[contains(.,'Version')]")

    def render_streams_lnk(self, render_id):
        return self.find_by(xpath="//li[contains(@class,'v-expansion-panel__container')]//*[contains(.,'/aqt/render/" + render_id + "')]//div[contains(@class,'v-card__title v-card__title--primary')]//a[contains(@id,'render_streams')]")

    def render_settings_lnk(self, render_id):
        return self.find_by(xpath="//li[contains(@class,'v-expansion-panel__container')]//*[contains(.,'/aqt/render/" + render_id + "')]//div[contains(@class,'v-card__title v-card__title--primary')]//a[contains(@id,'render_settings')]")

    def device_lnk(self, render_id):
        return self.find_by(xpath="//li[contains(@class,'v-expansion-panel__container')]//*[contains(.,'/aqt/render/" + render_id + "')]//div[contains(@class,'v-card__title v-card__title--primary')]//a[contains(@id,'device')]")

    page_url = QAdminPage.base_url + "render"
    page_title = "qadmin"

    def __init__(self, *args):
        QAdminPage.__init__(self, *args)


class QAdminRenderSettings(QAdminPage):
    @property
    def render_dd(self): return self.find_by(xpath="//input[@aria-label='Render']/..")

    @property
    def streams_per_gpu_txt(self): return self.find_by(id="streams_per_gpu_text_field")

    @property
    def jpeg_decompressors_txt(self): return self.find_by(id="jpeg_decompressor_text_field")

    @property
    def h26x_decompressors_txt(self): return self.find_by(id="h264_decompressor_text_field")

    @property
    def prefetch_queue_size_txt(self): return self.find_by(id="prefetch_queue_text_field")

    @property
    def tight_prefetch_chkb(self): return self.find_by(xpath="//input[@id='tight_prefetch_switch']/../div[contains(@class,'v-input--selection-controls__ripple')]")

    page_url = QAdminPage.base_url + "render_settings/none"
    page_title = "qadmin"

    def __init__(self, *args):
        QAdminPage.__init__(self, *args)


class QAdminRenderStreams(QAdminPage):
    @property
    def render_dd(self): return self.find_by(xpath="//input[@id='render_select']/..")

    def get_expand_icon(self, render_id):
        return self.find_by(xpath="//li[contains(@class,'v-expansion-panel__container')]//*[contains(.,'/aqt/render/" + render_id + "')]//div[@class='v-expansion-panel__header__icon']")

    def get_streams_id_value(self, render_id):
        return self.find_by(xpath="//li[contains(@class,'v-expansion-panel__container') and contains(.,'/aqt/render/" + render_id + "')]//div[contains(@class,'v-card__title v-card__title--primary')]/span[contains(.,'ID')]")

    def get_streams_gpu_value(self, render_id):
        return self.find_by(xpath="//li[contains(@class,'v-expansion-panel__container') and contains(.,'/aqt/render/" + render_id + "')]//div[contains(@class,'v-card__title v-card__title--primary')]/span[contains(.,'GPU')]")

    def get_streams_encoder_value(self, render_id):
        return self.find_by(xpath="//li[contains(@class,'v-expansion-panel__container') and contains(.,'/aqt/render/" + render_id + "')]//div[contains(@class,'v-card__title v-card__title--primary')]/span[contains(.,'Encoder')]")

    def get_streams_framerate_value(self, render_id):
        return self.find_by(xpath="//li[contains(@class,'v-expansion-panel__container') and contains(.,'/aqt/render/" + render_id + "')]//div[contains(@class,'v-card__title v-card__title--primary')]/span[contains(.,'Framerate')]")

    def get_streams_width_value(self, render_id):
        return self.find_by(xpath="//li[contains(@class,'v-expansion-panel__container') and contains(.,'/aqt/render/" + render_id + "')]//div[contains(@class,'v-card__title v-card__title--primary')]/span[contains(.,'Width')]")

    def get_streams_height_value(self, render_id):
        return self.find_by(xpath="//li[contains(@class,'v-expansion-panel__container') and contains(.,'/aqt/render/" + render_id + "')]//div[contains(@class,'v-card__title v-card__title--primary')]/span[contains(.,'Height')]")

    def delete_render_stream_btn(self):
        return self.find_by(id="render_stream_delete")

    page_url = QAdminPage.base_url + "render_streams/none"
    page_title = "qadmin"

    def __init__(self, *args):
        QAdminPage.__init__(self, *args)


class QAdminDevice(QAdminPage):
    @property
    def device_dd(self): return self.find_by(xpath="//input[@id='device_select']/..")

    @property
    def device_id_value(self): return self.find_by(xpath="//div[contains(@class,'v-card__title v-card__title--primary')]/span[contains(.,'ID')]")

    @property
    def version_value(self): return self.find_by(xpath="//div[contains(@class,'v-card__title v-card__title--primary')]/span[contains(.,'Version')]")

    @property
    def type_value(self): return self.find_by(xpath="//div[contains(@class,'v-card__title v-card__title--primary')]/span[contains(.,'Type')]")

    @property
    def system_value(self): return self.find_by(xpath="//div[contains(@class,'v-card__title v-card__title--primary')]/span[contains(.,'System')]")

    @property
    def ntp_tab(self): return self.find_by(xpath="//div[contains(@class,'v-list__tile__title') and contains(.,'NTP')]")

    @property
    def ntp_offset_value(self): return self.find_by(xpath="//div[contains(@class,'v-list__tile')]//span[contains(@class,'lighten-1') and contains(.,'Offset')]")

    @property
    def ntp_server_value(self): return self.find_by(xpath="//div[contains(@class,'v-list__tile')]//span[contains(@class,'lighten-1') and contains(.,'Server')]")

    @property
    def submodules_tab(self): return self.find_by(xpath="//div[contains(@class,'v-list__tile__title') and contains(.,'Submodules')]")

    @property
    def device_settings_btn(self): return self.find_by(id="device_settings")

    @property
    def restart_daemon_lnk(self): return self.find_by(id="restart_daemon_dialog")

    @property
    def restart_device_lnk(self): return self.find_by(id="restart_device_dialog")

    @property
    def device_settings_lnk(self): return self.find_by(id="device_settings")

    @property
    def daemon_restart_ok_btn(self): return self.find_by(id="daemon_restart_ok")

    @property
    def daemon_restart_cancel_btn(self): return self.find_by(id="daemon_restart_cancel")

    @property
    def device_restart_ok_btn(self): return self.find_by(id="device_restart_ok")

    @property
    def device_restart_cancel_btn(self): return self.find_by(id="device_restart_cancel")

    @property
    def device_shutdown_ok_btn(self): return self.find_by(id="device_shutdown_ok")

    @property
    def device_shutdown_cancel_btn(self): return self.find_by(id="device_shutdown_cancel")

    page_url = QAdminPage.base_url + "system"
    page_title = "qadmin"

    def __init__(self, *args):
        QAdminPage.__init__(self, *args)


class QAdminReservations(QAdminPage):
    page_url = QAdminPage.base_url + "reservations"
    page_title = "qadmin"

    def __init__(self, *args):
        QAdminPage.__init__(self, *args)


class QAdminLogs(QAdminPage):
    @property
    def search_txt(self): return self.find_by(xpath="//input[@aria-label='Search']")

    def get_column(self, col_name):
        return self.find_by(xpath="//th[@role='columnheader' and contains(.,'" + col_name + "')]")

    page_url = QAdminPage.base_url + "logs"
    page_title = "qadmin"

    def __init__(self, *args):
        QAdminPage.__init__(self, *args)
