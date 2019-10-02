import datetime as dt
import json
import math
import os
import random
import re
import subprocess
import time
import cv2
import numpy as np
import pytest

from src.AquetiPage import *
from src.BaseEnv import *
from src.QPage import *
from src.BaseTest import BaseTest
from src.decorators import *

try:
    import AQT
except ImportError:
    print('no AQT lib found')
    exit(1)


class GO:
    cams = None
    renderers = None

    def __init__(self, *args, **kwargs):
        self.api = args[0]
        self.__call__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        self.cams = self.api.GetAvailableCameras()
        self.renderers = self.api.GetAvailableRenderers()

    def get_stream_info(self, r_index, s_index):
        if self.renderers is not None:
            renderer_info = json.loads(self.api.GetDetailedStatus(self.renderers[r_index].Name()))

            if len(renderer_info["render_streams"]) > s_index:
                stream_info = json.loads(self.api.GetDetailedStatus("/aqt/render/" + renderer_info["id"] + '/' + renderer_info["render_streams"][s_index]))

                return stream_info

    def get_renderer_info(self, r_index):
        if self.renderers is not None:
            renderer_info = json.loads(self.api.GetDetailedStatus(self.renderers[r_index].Name()))

            return renderer_info


class TestQApp(BaseTest):
    browser = "chrome"

    env = Environment(render_ip="10.0.0.189", cam_ip="10.1.11.10")

    cam_id = '11'
    cam_name = '/aqt/camera/' + cam_id
    system_name = "camera11"

    api = None
    cam = None
    cpage = None

    def get_params(self):
        time.sleep(7)
        return json.loads(self.api.GetParameters(self.cam_name))

    def set_params(self, json_str):
        self.api.SetParameters(self.cam_name, json_str)
        time.sleep(3)

    def restore_defaults(self):
        json_str = '''
        {
        	"auto_analog_gain_enabled": false,
        	"auto_night_mode_enabled": true,
        	"auto_digital_gain_enabled": false,
        	"auto_whitebalance": true,
        	"saturation": 0,
        	"auto_whitebalance_interval_seconds": 300,
        	"auto_night_mode_enable_threshold": 22,
        	"whitebalance_mode": "AUTO",
        	"auto_night_mode_disable_threshold": 1,
        	"exposure_time_milliseconds": 0,
        	"auto_exposure_enabled": false,
        	"denoising": 0.5,
        	"auto_ir_filter_enabled": true,
        	"quality": "medium",
        	"data_routing_policy": "",
        	"operating_mode": {
        		"framerate": 30,
        		"tiling_policy": 2,
        		"compression": 2
        	},
        	"digital_gain": 1,
        	"system_auto_interval": 300,
        	"ir_filter": false,
        	"framerate": 30,
        	"system_auto_enabled": false,
        	"auto_model_generation_enabled": false,
        	"analog_gain": 1,
        	"auto_model_generation_interval_seconds": 0,
        	"sharpening": 0.5
        }
        '''

        self.set_params(json_str)


    def setup_method(self, method):
        super(TestQApp, self).setup_method(method)

    def teardown_method(self, method):
        super(TestQApp, self).teardown_method(method)

    @pytest.fixture
    def login(self, caplog):
        self.cpage.login(username="user", password="12345678", system=self.system_name)

        time.sleep(5)

        max = 5
        for i in range(max):
            if self.cpage.failed_dialog is None:
                break
            else:
                if i == (max - 1):
                    self.failure_exception("Failed to create render stream")
                    exit(1)

            time.sleep(1)

    @pytest.fixture()
    def qview(self):
        self.cpage = QViewPage(self)
        self.cpage.navigate_to()

    @pytest.fixture()
    def qadmin(self):
        self.cpage = QAdminPage(self)
        self.cpage.navigate_to()

    @pytest.fixture()
    def api(self):
        self.api = AQT.AquetiAPI("test_api", AQT.U8Vector(), AQT.StringVector(["aqt://" + self.system_name]))
        self.cam = AQT.Camera(self.api, self.cam_name)
        self.go = GO(self.api)

        yield

        self.restore_defaults()

    @pytest.fixture()
    def avi(self):
        self.cpage.get_lside_add_cam_btn()(act="click")

        WebDriverWait(self.driver, self.cpage.TIMEOUT).until(
            EC.visibility_of_any_elements_located((By.XPATH, "//i[text()='cast']/ancestor::button[@style]")))

        self.cpage.right_sidebar_btn()
        self.cpage.rside_avi_lnk()

        self.cpage.export_avi_chkb()

        yield

        self.cpage.export_avi_chkb()

    @pytest.fixture()
    def db(self):
        pass


    def find_diff(self, path):
        db_name = "acos"
        col_name = "files"
        col = self.get_col_obj(db_name, col_name)

        res = []

        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".hc"):
                    fpath = os.path.join(root, file)
                    if col.find({"filename": fpath}).count() != 1:
                        res.append()

        return res

#QView

    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qview", "login", "db")
    @storeresult
    def test_case_111(self):
        web_scops = self.cpage.get_lside_scops_names()
        db_scops = self.db.query({"type": "mantis"})

        assert len(web_scops) == len(db_scops)

        for db_scop in db_scops:
            assert ("/aqt/camera/" + db_scop['id']) in web_scops

    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qview", "login", "api")
    @storeresult
    def test_case_112(self):
        cam_names = self.cpage.get_lside_scops_names()

        for cam_name in sorted(cam_names, reverse=True):
            self.cpage.get_lside_add_cam_btn(cam_name)(act="click")
            time.sleep(7)

            renders = self.api.GetAvailableRenderers()
            render = renders[0]

            render_info = json.loads(self.api.GetDetailedStatus(render.Name()))
            streams = render_info["render_streams"]

            assert len(streams) > 0

            stream = streams[0]
            stream_info = json.loads(self.api.GetDetailedStatus(render.Name() + '/' + stream))

            scop_list = stream_info["SCOP_list"]

            for scop_name in scop_list:
                assert cam_name == "/aqt/camera/" + scop_name

    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qview", "login", "api")
    @storeresult
    def test_case_113(self):
        self.cpage.get_lside_scop()(act='click')

        if not self.cam.IsRecording():
            self.cpage.get_lside_recording_btn()(act='click')
            time.sleep(1)
            assert self.cam.IsRecording()

        if self.cam.IsRecording():
            self.cpage.get_lside_recording_btn()(act='click')
            time.sleep(1)
            assert not self.cam.IsRecording()

    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qview", "login", "api")
    @storeresult
    def test_case_114(self):
        self.cpage.get_lside_scop()(act='click')
        # self.api.SetParameters(self.cam_name, json.dumps({"fineAutofocus": True}))

        status_arr = []
        s_time = dt.datetime.now()
        while (dt.datetime.now() - s_time).total_seconds() < 3:
            status = json.loads(self.api.GetDetailedStatus(self.cam_name))
            status_arr.append(status["focus_status"])

            time.sleep(0.25)

        assert "BUSY" not in status_arr

        self.cpage.get_lside_fine_focus_btn()(act='click')

        status_arr = []
        s_time = dt.datetime.now()
        while (dt.datetime.now() - s_time).total_seconds() < 3:
            status = json.loads(self.api.GetDetailedStatus(self.cam_name))
            status_arr.append(status["focus_status"])

            time.sleep(0.25)

        assert "BUSY" in status_arr

    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qview", "login", "api")
    @storeresult
    def test_case_115(self):
        self.cpage.get_lside_scop()(act='click')

        status_arr = []
        s_time = dt.datetime.now()
        while (dt.datetime.now() - s_time).total_seconds() < 3:
            status = json.loads(self.api.GetDetailedStatus(self.cam_name))
            status_arr.append(status["focus_status"])

            time.sleep(0.25)

        assert "BUSY" not in status_arr

        self.cpage.get_lside_coarse_focus_btn()(act='click')

        status_arr = []
        s_time = dt.datetime.now()
        while (dt.datetime.now() - s_time).total_seconds() < 3:
            status = json.loads(self.api.GetDetailedStatus(self.cam_name))
            status_arr.append(status["focus_status"])

            time.sleep(0.25)

        assert "BUSY" in status_arr

    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qview", "login")
    @storeresult
    def test_case_116(self):
        scop_name = self.cpage.get_lside_scops_names()[-1]
        self.cpage.get_lside_scop(scop_name=scop_name)(act='click')

        time.sleep(0.5)

        self.cpage.get_lside_advanced_btn(scop_name=scop_name)(act='click')

        time.sleep(2)

        assert len(self.driver.window_handles) == 2

        self.driver.switch_to_window(self.driver.window_handles[1])

        qacm = QAdminCameraMicrocameras(self)

        scop_name2 = qacm.cam_select_div.text

        assert scop_name == scop_name2

    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qview")
    @pytest.mark.parametrize("username, password, expected", [("test",  "1111",     True),
                                                              ("test",  "12345678", True),
                                                              ("",      "",         True),
                                                              ("user",  "",         True),
                                                              ("",      "12345678", True),
                                                              ("user",  "1234",     True),
                                                              ("user",  "12345678", False)])
    @storeresult
    def test_case_120(self, username, password, expected):
        self.cpage.login(username=username, password=password, system=self.system_name)
        time.sleep(3)

        assert isinstance(self.cpage.active_dialog, WebElement) == expected


    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qview", "login")
    @storeresult
    def test_case_121(self): #logout
        self.cpage.user_icon()

        self.cpage.logout_btn()
        self.cpage.get_dialog_btn("Close")()

        assert not isinstance(self.cpage.active_dialog, WebElement)

        self.cpage.logout_btn()
        self.cpage.get_dialog_btn("Logout")()

        assert isinstance(self.cpage.form, WebElement)


    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qview")
    @storeresult
    def test_case_122(self): #relogin after logout
        self.cpage.login(username="user", password="12345678", system=self.system_name)
        self.cpage.logout()

        while not isinstance(self.cpage.form, WebElement):
            time.sleep(1)

        self.cpage.login(username="user", password="12345678", system=self.system_name)

        time.sleep(2)

        assert not isinstance(self.cpage.active_dialog, WebElement)


    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qview", "login")
    @storeresult
    def test_case_123(self):
        def is_opened(e):
            if e is None:
                return False

            tag_name = e.get_attribute('tagName').lower()
            if tag_name == "aside":
                className = e.get_attribute('class')
                if "v-navigation-drawer--open" in className:
                    return True
                return False
            return False

        if is_opened(self.cpage.left_sidebar):
            self.cpage.left_sidebar_btn()
            assert not is_opened(self.cpage.left_sidebar)
        else:
            self.cpage.left_sidebar_btn()
            assert is_opened(self.cpage.left_sidebar)

        if is_opened(self.cpage.right_sidebar):
            self.cpage.right_sidebar_btn()
            assert not is_opened(self.cpage.right_sidebar)
        else:
            self.cpage.right_sidebar_btn()
            assert is_opened(self.cpage.right_sidebar)


    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qview", "login")
    @storeresult
    def test_case_201(self):
        def get_models():
            return list(self.db.query({"scop": self.cam_id}, "acos", "models"))

        s_cnt = len(get_models())

        self.cpage.stream_calibration_btn()
        self.cpage.gen_new_geometry_btn()

        time.sleep(2)

        while isinstance(self.cpage.geometry_progress_bar, WebElement):
            time.sleep(15)

        e_cnt = len(get_models())

        assert (e_cnt - s_cnt) == 1


    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qview", "login")
    @storeresult
    def test_case_202(self):
        s_res = self.env.cam.exec_cmd(cmd="ls -la /etc/aqueti/config.json")

        self.cpage.stream_calibration_btn()
        self.cpage.save_cur_geometry_btn()

        time.sleep(10)

        e_res = self.env.cam.exec_cmd(cmd="ls -la /etc/aqueti/config.json")

        for i in range(self.env.cam.num_of_tegras):
            assert s_res != e_res


    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qview", "login")
    @storeresult
    def test_case_203(self):
        def get_models():
            return list(self.db.query({"scop": self.cam_id}, "acos", "models"))

        s_cnt = len(get_models())

        self.cpage.stream_calibration_btn()
        self.cpage.set_to_saved_geometry_btn()

        time.sleep(3)

        e_cnt = len(get_models())

        assert (e_cnt - s_cnt) == 1


    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qview", "login")
    @storeresult
    def test_case_204(self):
        def get_models():
            return list(self.db.query({"scop": self.cam_id}, "acos", "models"))

        s_cnt = len(get_models())

        time.sleep(1)
        self.cpage.stream_calibration_btn()
        #self.cpage.reset_geometry_btn()

        time.sleep(3)

        e_cnt = len(get_models())

        assert (e_cnt - s_cnt) == 1


    #@pytest.mark.skip(reason="")
    @pytest.mark.regression
    @pytest.mark.usefixtures("qview", "login", "avi")
    @storeresult
    def test_case_1000(self):
        pass


    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qview", "login")
    @storeresult
    def test_case_1001(self):
        self.cpage.dots_icon()

        self.cpage.stream_keybindings_btn()

        assert self.cpage.active_dialog is not None


    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qview", "login")
    @storeresult
    def test_case_1002(self):
        self.cpage.dots_icon()

        self.cpage.submit_issue_btn()

        f_name = "test_" + str(dt.datetime.now().strftime('%s'))

        self.cpage.si_filename_txt(value=f_name)
        self.cpage.si_summary_txt(value="test")
        self.cpage.si_description_txt(value="test")
        self.cpage.get_dialog_btn("Submit")()

        time.sleep(30)

        assert os.path.exists("/var/tmp/aqueti/" + f_name + ".zip")
        assert os.path.exists(os.path.expanduser("~") + "/Downloads/" + f_name + ".zip")


    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qview", "login")
    @storeresult
    def test_case_1003(self):
        self.cpage.dots_icon()

        self.cpage.qadmin_btn(self)

        qap = QAdminPage(self)

        assert qap.url == self.cpage.url


    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qview", "login")
    @storeresult
    def test_case_1004(self):
        self.cpage.dots_icon()

        self.cpage.help_manual_btn()

        time.sleep(5)

        assert os.path.exists(os.path.expanduser("~") + "/Downloads/qview.pdf")


    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qview", "login")
    @storeresult
    def test_case_1005(self):
        self.cpage.dots_icon()

        self.cpage.language_dd()

        self.cpage.get_dd_elem("中文")(act="click")

        assert "实时" in self.cpage.live_btn.text

        self.cpage.language_dd()

        self.cpage.get_dd_elem("English")(act="click")

        assert "LIVE" in self.cpage.live_btn.text


    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qview")
    @storeresult
    def test_case_1006(self):
        self.cpage.login(username="user", password="12345678", language="cn", system="camera11")

        assert "实时" in self.cpage.live_btn.text


    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qadmin", "login")
    @pytest.mark.parametrize("cur_passwd, new_passwd, new_passwd2, err_msg, expected",
                                                             [("", "", "", "Password too short", False),
                                                              ("12345678", "", "",  "Password too short", False),
                                                              ("", "87654321", "87654321", "", False),
                                                              ("11111111", "87654321", "87654321", "", False),
                                                              ("12345678", "4321", "4321", "Password too short", False),
                                                              ("12345678", "4321", "321", "Passwords do not match.", False),
                                                              ("12345678", "87654321", "987654321", "Passwords do not match.", False),
                                                              ("12345678", "12345678", "12345678", "", True)
                                                              ])
    @storeresult
    def test_case_1007(self, cur_passwd, new_passwd, new_passwd2, err_msg, expected):
        self.cpage.user_icon()
        self.cpage.change_password_btn()

        self.cpage.current_password_txt(value=cur_passwd)
        self.cpage.new_password_txt(value=new_passwd)
        self.cpage.confirm_password_txt(value=new_passwd2)

        self.cpage.get_dialog_btn("Submit")()

        assert self.cpage.get_dialog_warning() == err_msg

        if expected:
            time.sleep(3)

        assert (self.cpage.active_dialog is None) == expected


    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qadmin")
    @pytest.mark.parametrize("cur_pwd, new_pwd, expected",
                                                        [("12345678", "987654321", True),
                                                         ("987654321", "12345678", True)])
    @storeresult
    def test_case_1008(self, cur_pwd, new_pwd, expected):
        self.cpage.login(username="user", password=cur_pwd, system=self.system_name)

        time.sleep(3)

        self.cpage.user_icon()
        self.cpage.change_password_btn()

        self.cpage.current_password_txt(value=cur_pwd)
        self.cpage.new_password_txt(value=new_pwd)
        self.cpage.confirm_password_txt(value=new_pwd)

        self.cpage.get_dialog_btn("Submit")()

        if expected:
            time.sleep(3)

        assert (self.cpage.active_dialog is None) == expected


    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qview", "login")
    @storeresult
    def test_case_1009(self):
        self.cpage.right_sidebar_btn()
        self.cpage.rside_avi_lnk()

        self.cpage.avi_arrow_dd()
        self.cpage.get_dd_elem("All")(act="click")

        s_cnt = len(self.cpage.get_rows(self.cpage.avi_tbl))

        time.sleep(5)
        self.cpage.export_avi_chkb()
        time.sleep(10)
        self.cpage.export_avi_chkb()
        time.sleep(5)

        m_cnt = len(self.cpage.get_rows(self.cpage.avi_tbl))

        assert (m_cnt - s_cnt) == 1

        f_name = self.cpage.get_last_col(self.cpage.avi_tbl).text.strip().replace(":", "_")

        #assert os.path.exists("/var/tmp/aqueti/avi/" + f_name)
        assert os.path.exists(os.path.expanduser('~') + "/Downloads/" + f_name)

        self.cpage.get_avi_download_btn(self.cpage.get_rows(self.cpage.avi_tbl)[-1])(act="click")
        time.sleep(5)

        assert os.path.exists(os.path.expanduser('~') + "/Downloads/" + f_name[:f_name.rindex(".")] + " (1)" + f_name[f_name.rindex("."):])

        self.cpage.get_avi_delete_btn(self.cpage.get_rows(self.cpage.avi_tbl)[-1])(act="click")
        time.sleep(10)

        # assert not os.path.exists("/var/tmp/aqueti/avi/" + f_name)

        e_cnt = len(self.cpage.get_rows(self.cpage.avi_tbl))

        assert (m_cnt - e_cnt) == 1


    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qview", "login")
    @storeresult
    def test_case_1010(self):
        self.cpage.right_sidebar_btn()
        time.sleep(1)
        self.cpage.rside_reservations_lnk()

        self.cpage.reservations_arrow_dd()
        self.cpage.get_dd_elem("All")(act="click")

        rows = self.cpage.get_rows(self.cpage.reservations_tbl)
        s_cnt = 0 if 'No data available' in rows[-1].text else len(rows)

        self.cpage.recording_btn()
        time.sleep(10)
        self.cpage.recording_btn()
        time.sleep(5)

        rows = self.cpage.get_rows(self.cpage.reservations_tbl)
        m_cnt = 0 if 'No data available' in rows[-1].text else len(rows)

        assert (m_cnt - s_cnt) == 1


    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qview", "login")
    @storeresult
    def test_case_1011(self):
        time.sleep(5)
        self.cpage.right_sidebar_btn()
        time.sleep(1)
        self.cpage.rside_reservations_lnk()

        rows = self.cpage.get_rows(self.cpage.reservations_tbl)
        s_cnt = 0 if 'No data available' in rows[-1].text else len(rows)

        self.cpage.create_reservation_btn()

        self.cpage.description_txt(value="test")
        self.cpage.start_date_txt(act="click")
        self.cpage.get_calendar_elem("first")(act="click")
        #self.cpage.start_time_txt()
        self.cpage.end_date_txt(act="click")
        self.cpage.get_calendar_elem("last")(act="click")
        #self.cpage.end_time_txt()
        self.cpage.expiration_date_txt(act="click")
        self.cpage.get_calendar_elem("last")(act="click")
        #self.cpage.expiration_time_txt()

        self.cpage.get_dialog_btn("Create")()

        rows = self.cpage.get_rows(self.cpage.reservations_tbl)
        m_cnt = 0 if 'No data available' in rows[-1].text else len(rows)

        assert (m_cnt - s_cnt) == 1


    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qview", "login", "api")
    @storeresult
    def test_case_1012(self):
        types = {"H264": "H264", "LOCALDISPLAY": "Window"}
        resolutions = {"480p": (640, 480), "720p": (1280, 720), "1080p": (1920, 1080), "4k": (3840, 2160)}
        framerates = [5, 10, 15, 20, 25, 30]
        projections = ["PLANE", "CYLINDER"]

        for type, vtype in types.items():
            for resolution, img_wh in resolutions.items():
                for framerate in framerates:
                    self.cpage.video_box(act="rightclick")
                    self.cpage.customize_stream_btn()

                    time.sleep(1)

                    self.cpage.type_dd()
                    self.cpage.get_dd_elem(type)(act="click")

                    self.cpage.display_dd()
                    self.cpage.get_dd_elem(resolution)(act="click")

                    self.cpage.framerate_dd()
                    self.cpage.get_dd_elem(framerate)(act="click")

                    self.cpage.projection_dd()
                    self.cpage.get_dd_elem(projections[random.randint(0, 1)])(act="click")

                    self.cpage.letterbox_chkb()

                    self.cpage.get_dialog_btn("Update")()

                    time.sleep(5)

                    stream_info = self.go.get_stream_info(0, 0)

                    assert stream_info["encoder"] == vtype
                    assert stream_info["width"] == img_wh[0] and stream_info["height"] == img_wh[1]
                    assert stream_info["framerate"] == framerate


    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qview", "login", "api")
    @storeresult
    def test_case_1013(self):
        self.cpage.video_box(act="rightclick")
        self.cpage.change_camera_btn()

        time.sleep(0.5)
        self.cpage.get_dd("Camera")(act="click")
        dds = self.cpage.get_dd_elems()

        cur_scop = self.cpage.get_dd("Camera").text
        cur_scop = cur_scop[cur_scop.rindex("/") + 1: cur_scop.rindex("\n")]

        assert self.go.get_stream_info(0, 0)["SCOP_list"][0] == cur_scop

        for dd in dds:
            dd_scop = dd.text.replace("/aqt/camera/", "")
            if cur_scop not in dd_scop:
                cur_scop = dd_scop
                self.cpage.get_dd_elem(dd.text)(act="click")

        self.cpage.dialog__btn("Update")()

        time.sleep(5)

        assert self.go.get_stream_info(0, 0)["SCOP_list"][0] == cur_scop


    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qview", "login", "api")
    @storeresult
    def test_case_1014(self):
        self.cpage.video_box(act="rightclick")

        s_stream = self.go.get_renderer_info(0)["render_streams"]

        time.sleep(1)
        self.cpage.refresh_stream_btn()
        time.sleep(3)

        l_stream = self.go.get_renderer_info(0)["render_streams"]

        assert l_stream == s_stream


    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qview", "login", "api")
    @storeresult
    def test_case_1015(self):
        self.cpage.video_box(act="rightclick")

        s_stream = self.go.get_renderer_info(0)["render_streams"]

        time.sleep(1)
        self.cpage.delete_stream_btn()
        self.cpage.get_dialog_btn("yes")()
        time.sleep(3)

        l_stream = self.go.get_renderer_info(0)["render_streams"]

        assert len(s_stream) > 0
        assert len(l_stream) == 0


    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qview", "login")
    @storeresult
    def test_case_1016(self):
        self.cpage.video_box(act="rightclick")

        time.sleep(1)
        self.cpage.video_controls_btn()

        self.cpage.contain_rd()
        self.cpage.fill_rd()
        self.cpage.cover_rd()

        self.cpage.display_controls_chkb()

        self.cpage.get_dialog_btn("Close")()

        assert self.cpage.display_controls_chkb is None


    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qview", "login")
    @storeresult
    def test_case_1017(self):
        lst_scops = self.cpage.get_lside_scops_names()

        self.cpage.user_icon()
        self.cpage.user_settings_btn()

        self.cpage.get_dd("Camera")(act="click")

        dd_scops = [dd.text for dd in self.cpage.get_dd_elems()]

        assert lst_scops == dd_scops


    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qview", "login")
    @storeresult
    def test_case_1018(self):
        self.cpage.user_icon()
        self.cpage.user_settings_btn()

        self.cpage.get_dd("Camera")(act="click")

        cur_dd = self.cpage.get_dd_elem().text
        for dd in self.cpage.get_dd_elems():
            if dd.text != cur_dd:
                self.cpage.get_dd_elem(dd.text)(act="click")
                break

        self.cpage.reload()

        time.sleep(2)

        selected_dd = self.cpage.get_lside_scop()

        assert selected_dd is not None
        assert selected_dd.text.split()[0].strip() == cur_dd


    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qview", "login")
    @storeresult
    def test_case_1019(self):
        state = {}

        self.cpage.user_icon()
        self.cpage.user_settings_btn()

        self.cpage.stream_on_page_load_chkb()
        time.sleep(1)

        state.update({"chkb": self.cpage.stream_on_page_load_chkb.is_checked()})

        if self.cpage.middle_rd.is_checked():
            self.cpage.corner_rd()
            state.update({"radio":"corner"})
        else:
            self.cpage.middle_rd()
            state.update({"radio": "middle"})

        self.cpage.get_dd("Camera")(act="click")

        state.update({"dd": self.cpage.get_dd_elem().text})

        self.cpage.get_dd_elem(index=-1)(act="click")

        self.cpage.live_latency_bounce(value="50;2")

        state.update({"slider": self.cpage.live_latency_slider.get_attribute("value")})

        self.cpage.get_dialog_btn("Close")()

        self.cpage.live_btn()

        self.cpage.reload()

        self.cpage.user_icon()
        self.cpage.user_settings_btn()

        assert state["chkb"] == self.cpage.stream_on_page_load_chkb.is_checked()
        if state["radio"] == "middle":
            assert state["chkb"] == self.cpage.middle_rd.is_checked()
        else:
            assert state["chkb"] == self.cpage.corner_rd.is_checked()
        assert state["dd"] == self.cpage.get_dd_elem().text
        assert state["slider"] == self.cpage.live_latency_slider.get_attribute("value")


    @pytest.mark.skip(reason="")
    @pytest.mark.usefixtures("qview", "login")
    @storeresult
    def test_case_1020(self):
        assert self.cpage.speed_dd.get_attribute("value") == "1"

        self.cpage.fast_rewind_btn()

        assert self.cpage.speed_dd.get_attribute("value") == "0.75"

        self.cpage.fast_forward_btn()

        assert self.cpage.speed_dd.get_attribute("value") == "1"

        for i in range(5):
            self.cpage.fast_rewind_btn()

        assert self.cpage.speed_dd.get_attribute("value") == "0.25"

        for i in range(5):
            self.cpage.fast_forward_btn()

        assert self.cpage.speed_dd.get_attribute("value") == "1"


    @pytest.mark.skip(reason="")
    @pytest.mark.regression
    @pytest.mark.usefixtures("qview", "login")
    @storeresult
    def test_case_1021(self):
        assert self.cpage.pause_btn is not None
        assert self.cpage.fast_rewind_btn is not None
        assert self.cpage.fast_forward_btn is not None
        assert self.cpage.speed_dd.get_attribute("value") == "1"

        self.cpage.pause_btn()

        assert self.cpage.play_btn is not None
        assert self.cpage.step_rewind_btn is not None
        assert self.cpage.step_forward_btn is not None
        assert self.cpage.speed_dd.get_attribute("value") == ""

        self.cpage.live_btn()

        assert self.cpage.pause_btn is not None
        assert self.cpage.fast_rewind_btn is not None
        assert self.cpage.fast_forward_btn is not None
        assert self.cpage.speed_dd.get_attribute("value") == "1"


    @pytest.mark.skip(reason="")
    @pytest.mark.regression
    @pytest.mark.usefixtures("qview", "login", "avi")
    @storeresult
    def test_case_1022(self):
        self.cpage.zoom_in_btn(act="click", times=5)
        time.sleep(2)
        self.cpage.zoom_out_btn(act="click", times=5)
        time.sleep(2)
        self.cpage.arrow_up_btn(act="click", times=5)
        time.sleep(2)
        self.cpage.arrow_down_btn(act="click", times=5)
        time.sleep(2)
        self.cpage.arrow_left_btn(act="click", times=5)
        time.sleep(2)
        self.cpage.arrow_right_btn(act="click", times=5)
        time.sleep(2)

        assert True