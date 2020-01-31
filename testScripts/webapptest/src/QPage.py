import math
import time
import datetime as dt

from src.BasePage import *


class BaseCont:
    @property
    def active_panel(self): return self.find_by(xpath="//div[contains(@class, 'menuable__content__active')][last()]")

    @property
    def active_dialog(self): return self.find_by(xpath="//div[contains(@class, 'v-dialog--active')][last()]")

    @property
    def failed_dialog(self): return self.find_by(xpath="//div[contains(@class, 'v-dialog--active') and contains(., 'RenderStream Creation')]", param="invisible")

    @property
    def active_elem(self):
        if self.active_dialog is not None:
            return self.active_dialog
        elif self.active_panel is not None:
            return self.active_panel
        else:
            return None

    def get_dialog_btn(self, title):
        return self.find_by(xpath="//button[contains(., '" + title + "')]", elem=self.active_elem)

    def close_dialog(self):
        e = self.active_panel

        #self.exec_js("arguments[0].setAttribute('style', 'display: none;');", e)
        #self.exec_js("arguments[0].classList.remove('menuable__content__active');", e)

        ActionChains(self.driver).move_by_offset(25, 25).double_click().perform()

    def get_dd(self, title):
        if title == "Camera":
            time.sleep(0.5)

        return self.find_by(xpath="//div[@role='combobox']//div[.//label[text()='" + str(title) + "']]//input")

    def get_dd_elems(self):
        return self.find_by(xpath="//div[@class='v-list__tile__title']/ancestor::div[@role='listitem']", elem=self.active_panel)

    def get_dd_elem(self, *args, **kwargs):
        if len(args) > 0:
            title = args[0]
            return self.find_by(xpath="//div[@class='v-list__tile__title' and text()='" + str(title) + "']/ancestor::div[@role='listitem']", elem=self.active_panel)
        else:
            dds = self.get_dd_elems()

            if len(kwargs) > 0:
                if "index" in kwargs.keys():
                    if len(dds) > kwargs["index"]:
                        return dds[kwargs["index"]]
                elif "value" in kwargs.keys():
                    for dd in dds:
                        if dd.text == kwargs["value"]:
                            return dd
            else:
                for dd in dds:
                    a = self.find_by(xpath="//a", elem=dd)
                    if a is not None:
                        if "active" in a.get_attribute("class"):
                            return dd

    def get_list_elems(self, elem=None):
        if elem is None:
            elem = self.active_panel

        return self.find_by(xpath="//div[@role='listitem']", elem=elem)

    def get_list_elem(self, title, elem=None):
        if elem is None:
            elem = self.active_panel

        return self.find_by(xpath="//div[contains(., '" + str(title) + "') and @role='listitem']", elem=elem)

    def get_dialog_warning_elem(self):
        return self.find_by(xpath="//i[text()='warning']/parent::div", elem=self.active_dialog)

    def get_dialog_warning(self):
        e = self.get_dialog_warning_elem()

        if e is not None:
            txt = e.get_attribute('innerText')
            return txt.replace("warning", "").strip()
        else:
            return ""

    def get_dialog_btn(self, title):
        return self.find_by(xpath="//button[contains(., '" + title + "')]", elem=self.active_dialog)

    def get_slider(self, val):
        return self.find_by("//input[@aria-label='" + val + "']//ancestor::input[@role='slider']/parent::div[contains(@class,'v-slider__thumb-container')]")

    def get_rows(self, tbl):
        rows = self.find_by(xpath="//tr", elem=tbl)

        if rows is not None:
            if isinstance(rows, list):
                return rows
            else:
                return [rows]
        else:
            return []

    def get_tbl_tds(self, tbl):
        tbl_ths = {}
        tbl_tds = {}

        ths = self.find_by(xpath="/thead/tr/th", elem=tbl)
        trs = self.find_by(xpath="/tbody/tr", elem=tbl)

        if not isinstance(trs, list):
            trs = [trs]

        if ths is not None:
            for i in range(len(ths)):
                key = ths[i].text if 'arrow' not in ths[i].text else ths[i].text[: ths[i].text.index('arrow')]

                tbl_ths.update({i: key})
        else:
            tbl_ths = {k: str(k) for k in range(len(self.find_by(xpath="/td", elem=trs[0])))}

        for tr in trs:
            tds = self.find_by(xpath="/td", elem=tr)
            for i in range(len(tds)):
                tbl_tds.setdefault(tbl_ths[i], []).append(tds[i])

        return tbl_tds

    def get_last_col(self, tbl):
        rows = self.get_rows(tbl)

        if len(rows) > 0:
            columns = self.find_by(xpath="//td", elem=rows[-1])

            return columns[0]

    def get_calendar_elem(self, title):
        if title == "first":
            return self.find_by(xpath="(//tbody//tr//td)[1]//button", elem=self.active_panel)
        elif title == "last":
            return self.find_by(xpath="(//tbody//tr//td)[last()]//button", elem=self.active_panel)
        else:
            return self.find_by(xpath="//tbody//div[text()='" + title + "']//ancestor::button", elem=self.active_panel)


class LoginForm(BaseCont):
    @property
    def username_txt(self): return self.find_by(css="input[aria-label='Username']", elem=self.active_dialog)

    @property
    def password_txt(self): return self.find_by(css="input[aria-label='Password']", elem=self.active_dialog)

    @property
    def system_dd(self): return self.find_by(css="input[aria-label='System']", elem=self.active_dialog)

    def login(self, *args, **kwargs):
        self.username_txt(value=kwargs['username'])
        self.password_txt(value=kwargs['password'])
        #self.system_txt(value=kwargs['system'] + Keys.ESCAPE)

        if 'language' in kwargs.keys():
            self.get_dd("Language")(act="click")
            if kwargs['language'] == 'cn':
                self.get_dd_elem("中文")(act="click")
                self.find_by(xpath="//button[contains(., '提交')]", elem=self.active_dialog)(act="click")
            else:
                self.get_dd_elem("English")(act="click")
                self.find_by(xpath="//button[contains(., 'Submit')]", elem=self.active_dialog)(act="click")
        else:
            self.get_dialog_btn("Submit")(act="click")

            self.system_dd(act="click")

            self.get_dd_elem(value=kwargs['system'])(act="click")

            self.close_dialog()


class QStreamBox(BaseCont):
    @property
    def video_area(self): return self.find_by(xpath="(//video)[1]/ancestor::div[contains(@class, 'container')][last()]")

    @property
    def video_box(self): return self.find_by(xpath="(//video)[1]", elem=self.video_area)

    @property
    def video_controls_panel(self): return self.find_by(xpath="//nav[contains(@class, 'v-toolbar--dense')]", elem=self.video_area)

# Right-click menu

    @property
    def customize_stream_btn(self): return self.get_list_elem("Customize Stream")

    @property
    def calibrate_stream_btn(self): return self.get_list_elem("Calibrate Stream")

    @property
    def change_camera_btn(self): return self.get_list_elem("Change Camera")

    @property
    def refresh_stream_btn(self): return self.get_list_elem("Refresh Stream")

    @property
    def delete_stream_btn(self): return self.get_list_elem("Delete Stream")

    @property
    def change_camera_btn(self): return self.get_list_elem("Change Camera")

    @property
    def video_controls_btn(self): return self.find_by(xpath="//button", elem=self.get_list_elem("Video Controls"))

# customize_stream_btn

    @property
    def type_dd(self): return self.find_by(xpath="//div[@class='v-select__slot' and contains(., 'Type')]",
                                           elem=self.active_dialog)

    @property
    def display_dd(self): return self.find_by(xpath="//div[@class='v-select__slot' and contains(., 'Display')]",
                                              elem=self.active_dialog)

    @property
    def framerate_dd(self): return self.find_by(id="//div[@class='v-select__slot' and contains(., 'Framerate')]", elem=self.active_dialog)

    @property
    def projection_dd(self): return self.find_by(xpath="//div[@class='v-select__slot' and contains(., 'Projection')]",
                                                 elem=self.active_dialog)

    @property
    def letterbox_chkb(self): return self.find_by(xpath="//input[@aria-label='Letterbox']/parent::div", elem=self.active_dialog)

# calibrate_stream_btn

    @property
    def geometry_progress_bar(self): return self.find_by(xpath="//div[contains(@class, 'v-list__tile__action') and contains(., ' / 4')]", elem=self.active_panel)

    @property
    def calibrate_geometry_btn(self): return self.get_list_elem("Calibrate Geometry Now")

    @property
    def save_geometry_btn(self): return self.get_list_elem("Save Current Geometry")

    @property
    def set_to_saved_geometry_btn(self): return self.get_list_elem("Set to Saved Geometry")

    @property
    def reset_geometry_btn(self): return self.get_list_elem("Reset Geometry to Factory Default")

# video_controls_btn

    @property
    def contain_rd(self): return self.find_by(xpath="//input[@aria-label='contain']/parent::div", elem=self.active_dialog)

    @property
    def fill_rd(self): return self.find_by(xpath="//input[@aria-label='fill']/parent::div", elem=self.active_dialog)

    @property
    def cover_rd(self): return self.find_by(xpath="//input[@aria-label='cover']/parent::div", elem=self.active_dialog)

    @property
    def display_controls_chkb(self): return self.find_by(xpath="//input[@aria-label='Display Video Controls']/parent::div", elem=self.active_dialog)


# controls

    @property
    def recording_btn(self): return self.find_by(xpath="//i[text()='adjust']/ancestor::button", elem=self.video_controls_panel)

    @property
    def play_btn(self): return self.find_by(xpath="//i[text()='play_arrow']/ancestor::button", elem=self.video_controls_panel)

    @property
    def pause_btn(self): return self.find_by(xpath="//i[text()='pause']/ancestor::button", elem=self.video_controls_panel)

    @property
    def fast_rewind_btn(self): return self.find_by(xpath="//i[text()='fast_rewind']/ancestor::button", elem=self.video_controls_panel)

    @property
    def fast_forward_btn(self): return self.find_by(xpath="//i[text()='fast_forward']/ancestor::button", elem=self.video_controls_panel)

    @property
    def step_rewind_btn(self): return self.find_by(xpath="//i[text()='skip_previous']/ancestor::button", elem=self.video_controls_panel)

    @property
    def step_forward_btn(self): return self.find_by(xpath="//i[text()='skip_next']/ancestor::button", elem=self.video_controls_panel)

    @property
    def speed_dd(self): return self.find_by(xpath="//input[@aria-label='speed']", elem=self.video_controls_panel)

    @property
    def live_btn(self): return self.find_by(xpath="//button[@id='live']/parent::span", elem=self.video_controls_panel)

    @property
    def single_stream_btn(self): return self.find_by(xpath="//i[text()='crop_landscape']/ancestor::button", elem=self.video_controls_panel)

    @property
    def multi_stream_btn(self): return self.find_by(xpath="//i[text()='view_column']/ancestor::button", elem=self.video_controls_panel)

# create_tag_btn

    @property
    def create_tag_btn(self): return self.find_by(xpath="//i[text()='loyalty']/ancestor::button", elem=self.video_controls_panel)

    @property
    def description_txt(self): return self.find_by(xpath="//input[@aria-label='Description']", elem=self.active_panel)

# stream_settings_btn

    @property
    def stream_settings_btn(self): return self.find_by(xpath="//i[text()='tune']/ancestor::button", elem=self.video_controls_panel)

    @property
    def brightness_txt(self): return self.find_by(id="brightness_text_field", elem=self.active_panel)

    @property
    def contrast_txt(self): return self.find_by(id="contrast_text_field", elem=self.active_panel)

    @property
    def dark_level_txt(self): return self.find_by(id="dark_level_text_field", elem=self.active_panel)

    @property
    def pixel_width_txt(self): return self.find_by(id="pixel_width_text_field", elem=self.active_panel)

    @property
    def set_btn(self): return self.find_by(id="set_parameters_btn", elem=self.active_panel)

    @property
    def remove_btn(self): return self.find_by(id="remove_parameters_btn", elem=self.active_panel)

# go_to_time_btn

    @property
    def go_to_time_btn(self): return self.find_by(xpath="//i[text()='access_time']/ancestor::button", elem=self.video_controls_panel)

# timeline_settings_btn

    @property
    def timeline_settings_btn(self): return self.find_by(xpath="//i[text()='more_vert']/ancestor::button", elem=self.video_controls_panel)

# show_timeline_btn

    @property
    def show_timeline_btn(self): return self.find_by(xpath="//i[text()='keyboard_arrow_up']/ancestor::button", elem=self.video_controls_panel)

    @property
    def panning_panel(self): return self.find_by(xpath="//div[@class='layout column' and .//button]", elem=self.video_area)

    @property
    def zoom_in_btn(self): return self.find_by(xpath="//i[text()='zoom_in']/ancestor::button", elem=self.panning_panel)

    @property
    def zoom_out_btn(self): return self.find_by(xpath="//i[text()='zoom_out']/ancestor::button", elem=self.panning_panel)

    @property
    def arrow_up_btn(self): return self.find_by(xpath="//i[text()='arrow_upward']/ancestor::button", elem=self.panning_panel)

    @property
    def arrow_down_btn(self): return self.find_by(xpath="//i[text()='arrow_downward']/ancestor::button", elem=self.panning_panel)

    @property
    def arrow_left_btn(self): return self.find_by(xpath="//i[text()='arrow_back']/ancestor::button", elem=self.panning_panel)

    @property
    def arrow_right_btn(self): return self.find_by(xpath="//i[text()='arrow_forward']/ancestor::button", elem=self.panning_panel)


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
    def device_lnk(self): return self.find_by(id="device_page")

    @property
    def reservations_lnk(self): return self.find_by(id="reservations_page")

    @property
    def logs_lnk(self): return self.find_by(id="logs_page")

    @property
    def users_lnk(self): return self.find_by(id="users_page")


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

    def menu_users(self):
        self.users_lnk()

        return QAdminUsers(self.test)

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


class QPage(BasePage, LoginForm):
    @property
    def top_panel(self): return self.find_by(xpath="//nav[.//img]")

    @property
    def left_sidebar_btn(self): return self.find_by(xpath="(//button[contains(., 'menu')][1]", elem=self.top_panel)

    @property
    def dots_icon(self): return self.find_by(xpath="//button[contains(., 'more_vert')]", elem=self.top_panel)

    @property
    def versions_icon(self): return self.find_by(xpath="//span[contains(@class, 'v-chip__content')]", elem=self.top_panel)

    @property
    def ping_time_fld(self): return self.find_by(xpath="//span[contains(@class, 'v-tooltip')]", elem=self.top_panel)

    @property
    def user_icon(self): return self.find_by(xpath="//i[contains(., 'account_circle')]/parent::div", elem=self.top_panel)

# left_sidebar_btn

    @property
    def left_sidebar(self): return self.find_by(xpath="//aside[1]")

# user_icon

    @property
    def change_password_btn(self): return self.find_by(xpath="//i[contains(., 'autorenew')]//ancestor::button", elem=self.active_panel)

    @property
    def user_settings_btn(self): return self.find_by(xpath="//i[contains(., 'settings')]//ancestor::button", elem=self.active_panel)

    @property
    def logout_btn(self): return self.find_by(xpath="//p[contains(., 'Logout')]/parent::div")   # ="//i[contains(., 'input')]//ancestor::button", elem=self.active_panel

## user_settings_btn

    @property
    def stream_on_page_load_chkb(self): return self.find_by(xpath="//input[@aria-label='Create a render stream on page load']/parent::div", elem=self.active_dialog)

    @property
    def corner_rd(self): return self.find_by(xpath="//input[@aria-label='Corner']/parent::div", elem=self.active_dialog)

    @property
    def middle_rd(self): return self.find_by(xpath="//input[@aria-label='Middle']/parent::div", elem=self.active_dialog)

    @property
    def live_latency_slider(self): return self.find_by(xpath="//input[@aria-label='Live Latency']", elem=self.active_dialog)

    @property
    def live_latency_bounce(self): return self.find_by(xpath="//input[@aria-label='Live Latency']/parent::div//div[@class='v-slider__thumb primary']", elem=self.active_dialog)

    @property
    def live_latency_txt(self): return self.find_by(xpath="//input[@id='live_setback_text_field']", elem=self.active_dialog)

# dots_icon

    @property
    def stream_keybindings_btn(self): return self.find_by(xpath="//button", elem=self.get_list_elem("Stream Keybindings"))

    @property
    def submit_issue_btn(self): return self.find_by(xpath="//i[text()='report_problem']/ancestor::button", elem=self.active_panel)

    @property
    def qadmin_btn(self): return self.find_by(xpath="//i[text()='person']/ancestor::a", elem=self.active_panel)

    @property
    def help_manual_btn(self): return self.find_by(xpath="//button", elem=self.get_list_elem("Help Manual"))

    @property
    def language_dd(self): return self.find_by(xpath="//i[text()='language']//ancestor::div[@role='listitem']//div[contains(@class, 'v-select__slot')]", elem=self.active_panel)

## submit_issue_btn

    @property
    def si_filename_txt(self):
        return self.find_by(css="input[aria-label='Filename']", elem=self.active_dialog)

    @property
    def si_summary_txt(self):
        return self.find_by(css="textarea[aria-label='Summary']", elem=self.active_dialog)

    @property
    def si_description_txt(self):
        return self.find_by(css="textarea[aria-label='Description']", elem=self.active_dialog)

# change_password_btn

    @property
    def current_password_txt(self): return self.find_by(xpath="//input[@aria-label='Current Password']", elem=self.active_dialog)

    @property
    def new_password_txt(self): return self.find_by(xpath="//input[@aria-label='New Password']", elem=self.active_dialog)

    @property
    def confirm_password_txt(self): return self.find_by(xpath="//input[@aria-label='Confirm Password']", elem=self.active_dialog)


    def submit_issue(self, *args, **kwargs):
        self.si_filename_txt(value=kwargs["filename"])
        self.si_summary_txt(value=kwargs["summary"])
        self.si_description_txt(value=kwargs["description"])

        self.get_dialog_btn("Submit")()

    def logout(self):
        self.user_icon()
        self.logout_btn()

        self.get_dialog_btn("Logout")()

    def __init__(self, *args):
        BasePage.__init__(self, *args)

        if len(args) > 0:
            self.page_url = "http://" + args[0].env.render.ip

        def __call__(self, text):
            BasePage.__call__()


class QViewPage(QPage, QStreamBox):
    @property
    def right_sidebar_btn(self): return self.find_by(xpath="//button[contains(., 'menu')][2]", elem=self.top_panel)

# right_sidebar_btn

    @property
    def right_sidebar(self):
        return self.find_by(xpath="//aside[last()]")

    @property
    def rside_avi_lnk(self):
        return self.find_by(xpath="//a[text()='AVI']", elem=self.right_sidebar)

    @property
    def rside_reservations_lnk(self):
        return self.find_by(xpath="//a[text()='Reservations']", elem=self.right_sidebar)

    @property
    def avi_tab(self):
        return self.find_by(id="avi-tab")

    @property
    def reservations_tab(self):
        return self.find_by(id="reservation_tab")

    @property
    def export_avi_chkb(self):
        return self.find_by(xpath="//input[@aria-label='Export AVI']/parent::div", elem=self.right_sidebar)

    @property
    def avi_tbl(self):
        return self.find_by(xpath="//table/tbody", elem=self.avi_tab)

    @property
    def reservations_tbl(self):
        return self.find_by(xpath="//table/tbody", elem=self.reservations_tab)

    @property
    def avi_delete_btn(self):
        return self.find_by(xpath="//i[text()='delete']", elem=self.avi_tab)

    @property
    def avi_download_btn(self):
        return self.find_by(xpath="//i[text()='cloud_download']", elem=self.avi_tab)

    @property
    def reservations_edit_btn(self):
        return self.find_by(xpath="//i[text()='create']", elem=self.reservations_tab)

    @property
    def reservations_remove_btn(self):
        return self.find_by(xpath="//i[text()='delete']", elem=self.reservations_tab)

    @property
    def avi_arrow_dd(self):
        return self.find_by(xpath="//i[text()='arrow_drop_down']/parent::div", elem=self.avi_tab)

    @property
    def reservations_arrow_dd(self):
        return self.find_by(xpath="//i[text()='arrow_drop_down']/parent::div", elem=self.reservations_tab)

# create_reservation_btn

    @property
    def create_reservation_btn(self):
        return self.find_by(xpath="//i[text()='add_circle']/ancestor::button", elem=self.reservations_tab)

    @property
    def description_txt(self):
        return self.find_by(xpath="//input[@aria-label='Description']", elem=self.active_dialog)

    @property
    def start_date_txt(self):
        return self.find_by(xpath="//input[@aria-label='Start Date']", elem=self.active_dialog)

    @property
    def start_time_txt(self):
        return self.find_by(xpath="//input[@aria-label='Start Time']", elem=self.active_dialog)

    @property
    def end_date_txt(self):
        return self.find_by(xpath="//input[@aria-label='End Date']", elem=self.active_dialog)

    @property
    def end_time_txt(self):
        return self.find_by(xpath="//input[@aria-label='End Time']", elem=self.active_dialog)

    @property
    def expiration_date_txt(self):
        return self.find_by(xpath="//input[@aria-label='Expiration Date']", elem=self.active_dialog)

    @property
    def expiration_time_txt(self):
        return self.find_by(xpath="//input[@aria-label='Expiration Time']", elem=self.active_dialog)


    def get_avi_elems(self):
        items = self.avi_tbl.find_elements_by_tag_name("tr")

        for i in range(len(items)):
            if 'No data available' in items[i].get_attribute('innerHTML'):
                del items[i]

        return items

    def get_lside_scops(self):
        scops = self.find_by(xpath="//div[@class='v-list__group' or @class='v-list__group v-list__group--active']", elem=self.left_sidebar)

        if scops is not None:
            if not isinstance(scops, list):
                scops = [scops]

        return scops

    def get_lside_scops_names(self):
        return [scop.get_attribute("innerText").split()[0].strip() for scop in self.get_lside_scops()]

    def get_lside_scop(self, scop_name=""):
        scops = self.get_lside_scops()

        if scops is None:
            return None

        for scop in scops:
            if scop_name != "":
                if scop.get_attribute("innerText").split()[0].strip() == scop_name.lower():
                    return scop
            else:
                if 'darken-2' not in self.find_by(xpath="//div[contains(@class, 'v-list__group__header')]//button", elem=scop).get_attribute('class'):
                    return scop

        return scops[0]

    def get_lside_add_cam_btn(self, scop_name=""):
        return self.find_by(xpath="//i[text()='cast']/ancestor::button", elem=self.get_lside_scop(scop_name))

    def get_lside_selected_scop_name(self):
        return self.get_lside_scop().get_attribute("innerText")

    def get_lside_recording_btn(self, scop_name=""):
        return self.find_by(xpath="//i[text()='adjust']/ancestor::button", elem=self.get_lside_scop(scop_name))

    def get_lside_fine_focus_btn(self, scop_name=""):
        return self.find_by(xpath="//i[text()='center_focus_strong']/ancestor::button", elem=self.get_lside_scop(scop_name))

    def get_lside_coarse_focus_btn(self, scop_name=""):
        return self.find_by(xpath="//i[text()='center_focus_weak']/ancestor::button", elem=self.get_lside_scop(scop_name))

    def get_lside_advanced_btn(self, scop_name=""):
        return self.find_by(xpath="//i[text()='tune']/ancestor::a", elem=self.get_lside_scop(scop_name))

    def get_avi_download_btn(self, row):
        return self.find_by(xpath="//i[text()='cloud_download']", elem=row)

    def get_avi_delete_btn(self, row):
        return self.find_by(xpath="//i[text()='delete']", elem=row)

    def __init__(self, *args):
        QPage.__init__(self, *args)

        if len(args) > 0:
            self.base_url = "http://" + args[0].env.render.ip

        self.page_url = self.base_url

        def __call__(self, text):
            QPage.__call__()

class QAdminPage(QPage, QAdminSidebar):
    def __init__(self, *args):
        QPage.__init__(self, *args)

        if len(args) > 0:
            self.page_url = "http://" + args[0].env.render.ip + "/admin/#/"

        def __call__(self, text):
            QPage.__call__()


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
    page_url = QAdminPage.base_url + "camera_reservations/none"
    page_title = "qadmin"

    def __init__(self, *args):
        QAdminPage.__init__(self, *args)


class QAdminCameraSettings(QAdminPage, QStreamBox):
    @property
    def capture_tab(self): return self.find_by(xpath="//div[@id='capture_tab']//a")

    @property
    def image_tab(self): return self.find_by(xpath="//div[@id='image_tab']//a")

    @property
    def compression_tab(self): return self.find_by(xpath="//div[@id='compression_tab']//a")

    @property
    def focus_tab(self): return self.find_by(xpath="//div[@id='focus_tab']//a")

# Capture
    @property
    def global_auto_chkb(self): return self.find_by(id="global_switch")

    @property
    def auto_stream_settings_btn(self): return self.find_by(xpath="//label[contains(., 'Global Auto')]/ancestor::div[contains(@class, 'row')][1]//button")

# ---Popup
    @property
    def auto_disable_btn(self):
        return self.find_by(id="auto_warning_ok")

    @property
    def auto_cancel_btn(self):
        return self.find_by(id="auto_warning_cancel")
# ---

# Auto Stream Settings
    @property
    def day_night_mode_chkb(self): return self.find_by(xpath="//input[@id='auto_night_mode_switch']", elem=self.active_panel)

    @property
    def day_night_ir_chkb(self): return self.find_by(xpath="//input[@id='auto_night_mode_ir_switch']", elem=self.active_panel)

    @property
    def day_threshold_txt(self): return self.find_by(xpath="//input[@id='day_night_threshold_text_field']", elem=self.active_panel)

    @property
    def night_threshold_txt(self): return self.find_by(xpath="//input[@id='night_mode_threshold_text_field']", elem=self.active_panel)

    @property
    def day_threshold_slider(self): return self.find_by(xpath="(//input[@id='day_night_threshold_text_field'])[1]", elem=self.active_panel)

    @property
    def night_threshold_slider(self): return self.find_by(xpath="(//input[@id='day_night_threshold_text_field'])[last()]", elem=self.active_panel)

    @property
    def day_sharpening_txt(self): return self.find_by(xpath="(//input[@id='sharpening_threshold_text_field'])[1]", elem=self.active_panel)

    @property
    def night_sharpening_txt(self): return self.find_by(xpath="(//input[@id='sharpening_threshold_text_field'])[last()]", elem=self.active_panel)

    @property
    def day_sharpening_slider(self): return self.find_by(xpath="(//input[@id='sharpening_threshold_slider'])[1]", elem=self.active_panel)

    @property
    def night_sharpening_slider(self): return self.find_by(xpath="(//input[@id='sharpening_threshold_slider'])[last()]", elem=self.active_panel)

    @property
    def day_denoising_txt(self): return self.find_by(xpath="(//input[@id='denoising_threshold_text_field'])[1]", elem=self.active_panel)

    @property
    def night_denoising_txt(self): return self.find_by(xpath="(//input[@id='denoising_threshold_text_field'])[last()]", elem=self.active_panel)

    @property
    def day_denoising_slider(self): return self.find_by(xpath="(//input[@id='denoising_threshold_slider'])[1]", elem=self.active_panel)

    @property
    def night_denoising_slider(self): return self.find_by(xpath="(//input[@id='denoising_threshold_slider'])[last()]", elem=self.active_panel)

    @property
    def day_saturation_txt(self): return self.find_by(xpath="(//input[@id='saturation_threshold_text_field'])[1]", elem=self.active_panel)

    @property
    def night_saturation_txt(self): return self.find_by(xpath="(//input[@id='saturation_threshold_text_field'])[last()]", elem=self.active_panel)

    @property
    def day_saturation_slider(self): return self.find_by(xpath="(//input[@id='saturation_threshold_slider'])[1]", elem=self.active_panel)

    @property
    def night_saturation_slider(self): return self.find_by(xpath="(//input[@id='saturation_threshold_slider'])[last()]", elem=self.active_panel)

    @property
    def day_fps_dd(self): return self.find_by(xpath="(//input[@id='framerate_select'])[1]", elem=self.active_panel)

    @property
    def night_fps_dd(self): return self.find_by(xpath="(//input[@id='framerate_select'])[last()]", elem=self.active_panel)
# ----

    @property
    def exposure_time_chkb(self): return self.find_by(id="exposure_time_switch")

    @property
    def exposure_time_slider(self): return self.find_by(id="exposure_time_slider")

    @property
    def exposure_time_txt(self): return self.find_by(id="exposure_time_text_field")

    @property
    def analog_gain_chkb(self): return self.find_by(id="analog_gain_switch")

    @property
    def analog_gain_slider(self): return self.find_by(id="analog_gain_slider")

    @property
    def analog_gain_txt(self): return self.find_by(id="analog_gain_text_field")

    @property
    def digital_gain_slider(self): return self.find_by(id="digital_gain_slider")

    @property
    def digital_gain_txt(self): return self.find_by(id="digital_gain_text_field")

    @property
    def fps_dd(self): return self.find_by(xpath="(//input[@id='framerate_select'])[last()]")

    @property
    def whitebalance_dd(self): return self.find_by(id="whitebalance_select")

    @property
    def whitebalance_slider(self): return self.find_by(id="global_slider")

    @property
    def whitebalance_txt(self): return self.find_by(id="global_text_field")

    @property
    def ir_filter_chkb(self): return self.find_by(id="ir_filter_switch")

# Image

    @property
    def sharpening_slider(self): return self.find_by(id="sharpening_slider")

    @property
    def sharpening_txt(self): return self.find_by(id="sharpening_text_field")

    @property
    def denoising_slider(self): return self.find_by(id="denoising_slider")

    @property
    def denoising_txt(self): return self.find_by(id="denoising_text_field")

    @property
    def saturation_slider(self): return self.find_by(id="saturation_slider")

    @property
    def saturation_txt(self): return self.find_by(id="saturation_text_field")


# Compression

    @property
    def compression_quality_dd(self): return self.find_by(xpath="id='quality_select")

# Focus

    @property
    def coarse_focus_btn(self): return self.find_by(id="focus_coarse_btn")

    @property
    def fine_focus_btn(self): return self.find_by(id="focus_fine_btn")

    @property
    def focus_dd(self): return self.find_by(id="focus_select")


    page_title = "qadmin"

    def move_digital_gain_slider(self, value):
        while True:
            c_value = float(self.digital_gain_txt.get_attribute("value"))
            diff = math.fabs(c_value - value)
            if diff >= 0.1:
                if c_value - value:
                    self.digital_gain_slider(value="1;4")
                else:
                    self.digital_gain_slider(value="-1;4")

    def __init__(self, *args):
        QAdminPage.__init__(self, *args)

        self.page_url = self.base_url + "camera_settings/none"


class QAdminCameraMicrocameras(QAdminPage, QStreamBox):
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

    @property
    def mcam_camera_dd(self): return self.find_by(id="camera_select")

    @property
    def mcam_microcamera_dd(self): return self.find_by(id="microcamera_select")

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


class QAdminUsers(QAdminPage):
    @property
    def users_cont(self): return self.find_by(xpath="//i[contains(., 'add_circle')]//ancestor::div[@class='container fluid']")

    @property
    def create_btn(self): return self.find_by(xpath="//i[contains(., 'add_circle')]//ancestor::button")

    @property
    def users_tbl(self): return self.find_by(xpath="//table", elem=self.users_cont)

    @property
    def users_tbl(self): return self.find_by(xpath="//input[@aria-label='Search']")


    def get_users(self):
        users = []

        pass


    def get_access_level(self, username):
        pass

    def get_delete_btn(self, username):
        pass


    page_url = QAdminPage.base_url + "users"
    page_title = "qadmin"

    def __init__(self, *args):
        QAdminPage.__init__(self, *args)