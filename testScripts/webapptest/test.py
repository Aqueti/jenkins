import pytest
from BaseTest import BaseTest
from AquetiPage import *
from QAdminPage import *
from BaseEnv import *
from pprint import pprint
import time
import re
import cv2
import json
import datetime as dt
import numpy as np
import subprocess
import random
import math
import os
try:
    import AQT
except ImportError:
    print('no AQT lib found')
    exit(1)


class TD:
    username = "admin"
    password = "1234"
    
    file_name = "test"
    expected_nw_usage = 200   # mb/s


class TestWebApp(BaseTest):
    browser = "chrome"

    @pytest.mark.skip(reason="")
    def test_issue_submition(self):
        aap_i = AquetiAdminPageIssue(self)
        aap_i.navigate_to()

        assert "[This field is required.]" not in aap_i.cur_page_source

        aap_i._(aap_i.title_field, "")
        aap_i._(aap_i.summary_field, "")
        aap_i._(aap_i.description_field, "")
        aap_i._(aap_i.submit_btn)

        assert "[This field is required.]" in aap_i.cur_page_source

        aap_sc = aap_i.submit_issue("title", "summary", "description")

        assert aap_sc.page_url == aap_sc.cur_page_url

    @pytest.mark.skip(reason="")
    def test_comp_name_update(self):
        aap_cc = AquetiAdminPageConfigurationCamera(self)
        aap_cc.navigate_to()

        nickname = "test"

        aap_cc.update_nickname(nickname)

        assert nickname == aap_cc.nickname.text

    @pytest.mark.skip(reason="")
    def test_internal_error(self):
        aap_sys = AquetiAdminPageStatusCamera(self)
        aap_sys.navigate_to()

        aap_sys._(aap_sys.host) # old style

        assert "Internal Server Error" == aap_sys.cur_page_source

    @pytest.mark.skip(reason="")
    def test_settings(self):
        aap_cc = AquetiAdminPageConfigurationCamera(self)
        aap_cc.navigate_to()

        aap_cc._(aap_cc.auto_gain_chkb)
        aap_cc._(aap_cc.auto_whitebalance_chkb)
        aap_cc._(aap_cc.auto_shutter_chkb)

        aap_cc._(aap_cc.gain_plus_btn)
        aap_cc._(aap_cc.whitebalance_plus_btn)
        aap_cc._(aap_cc.shutter_plus_btn)

        aap_cc._(aap_cc.gain_minus_btn)
        aap_cc._(aap_cc.whitebalance_minus_btn)
        aap_cc._(aap_cc.shutter_minus_btn)

        aap_cc.move_sharpening_slider(20)
        aap_cc.move_denoising_slider(40)

        aap_cc._(aap_cc.night_mode_chkb)
        aap_cc._(aap_cc.transport_mode_dd, "10 bit")
        aap_cc._(aap_cc.framerate_dd, "30 fps")

        assert self.api.GetParameters("sharpening") == 20

    @pytest.mark.skip(reason="")
    def test_sc_move(self):
        aap_cc = AquetiAdminPageConfigurationCamera(self)
        aap_cc.navigate_to()

        aap_cc.click_links()

        aap_cc = AquetiAdminPageConfigurationCamera(self)
        aap_cc.navigate_to()

        vs = dict()
        vs['before'] = [self.vs.PanDegrees(), self.vs.TiltDegrees(), self.vs.HorizontalFOVDegrees(), self.vs.VerticalFOVDegrees()]
        aap_cc._(aap_cc.arrow_down_btn)
        vs['up'] = vs['before'] = [self.vs.PanDegrees(), self.vs.TiltDegrees(), self.vs.HorizontalFOVDegrees(), self.vs.VerticalFOVDegrees()]
        aap_cc._(aap_cc.arrow_down_btn)
        vs['down'] = vs['before'] = [self.vs.PanDegrees(), self.vs.TiltDegrees(), self.vs.HorizontalFOVDegrees(), self.vs.VerticalFOVDegrees()]
        aap_cc._(aap_cc.arrow_left_btn)
        vs['left'] = vs['before'] = [self.vs.PanDegrees(), self.vs.TiltDegrees(), self.vs.HorizontalFOVDegrees(), self.vs.VerticalFOVDegrees()]
        aap_cc._(aap_cc.arrow_right_btn)
        vs['right'] = vs['before'] = [self.vs.PanDegrees(), self.vs.TiltDegrees(), self.vs.HorizontalFOVDegrees(), self.vs.VerticalFOVDegrees()]

        print("{0}\n{1}\n{2}\n{3}\n{4}".format(vs['before'], vs['up'], vs['down'], vs['left'], vs['right']))

        assert vs['before'] == vs['up']
        assert vs['up'] == vs['down']
        assert vs['down'] == vs['left']
        assert vs['left'] == vs['right']
        assert vs['right'] == vs['before']

    @pytest.mark.skip(reason="")
    def test_sc_zoom(self):
        aap_cc = AquetiAdminPageConfigurationCamera(self)
        aap_cc.navigate_to()

        vs = dict()
        vs['before'] = self.vs.Zoom()
        self.vs.Zoom(self.vs.Zoom() * 2)
        vs['in'] = self.vs.Zoom()
        self.vs.Zoom(self.vs.Zoom() * 0.6)
        vs['out'] = self.vs.Zoom()

        print("{0}\n{1}\n{2}".format(vs['before'], vs['in'], vs['out']))

        assert vs['before'] * 2 == vs['in']
        assert vs['in'] * 0.6 == vs['out']



    @pytest.mark.skip(reason="")
    def test_login_correct_credentials(self):
        alp = AquetiLoginPage(self)
        alp.navigate_to()

        aap_sys = alp.login(TD.username, TD.password)

        assert aap_sys.page_url == alp.cur_page_url

    @pytest.mark.skip(reason="")
    def test_login_empty_credentials(self):
        alp = AquetiLoginPage(self)
        alp.navigate_to()

        aap_sys = alp.login("", "")

        assert alp.page_url in alp.cur_page_url

    @pytest.mark.skip(reason="")
    def test_login_incorrect_login(self):
        alp = AquetiLoginPage(self)
        alp.navigate_to()

        aap_sys = alp.login("nimda", TD.password)

        assert "Username or password invalid" in alp.cur_page_source

    @pytest.mark.skip(reason="")
    def test_login_incorrect_password(self):
        alp = AquetiLoginPage(self)
        alp.navigate_to()

        aap_sys = alp.login(TD.username, "4321")

        assert "Username or password invalid" in alp.cur_page_source



    @pytest.mark.skip(reason="")
    def test_login_unauthorized_access(self):
        alp = AquetiLoginPage(self)
        alp.navigate_to()

        aap_sys = AquetiAdminPageStatusCamera(self)
        aap_sys.navigate_to()

        assert "Not Authorized to view this page" in aap_sys.cur_page_source

        aap_sys.navigate_to(AquetiAdminPage.base_url + "/log")

        assert "Not Authorized to view this page" in aap_sys.cur_page_source

    @pytest.mark.skip(reason="")
    def test_login_logout(self):
        alp = AquetiLoginPage(self)
        alp.navigate_to()

        aap_sys = alp.login(TD.username, TD.password)

        avp = aap_sys.logout()

        assert avp.page_title == avp.cur_page_title

    @pytest.mark.skip(reason="")
    def test_login_logout_timeout(self):
        alp = AquetiLoginPage(self)
        alp.navigate_to()

        aap_sys = alp.login(TD.username, TD.password)

        time.sleep(61)

        aap_sys.navigate_to()

        assert alp.page_url in aap_sys.cur_page_url

    @pytest.mark.skip(reason="")
    def test_login_correct_credentials(self):       
        alp = AquetiLoginPage(self)
        alp.navigate_to()

        aap_sys = alp.login(TD.username, TD.password)

        assert aap_sys.page_title == aap_sys.cur_page_title


class TestAPIWebApp(BaseTest):
    browser = "chrome"

    cam_id = "9"
    cam_path = "/aqt/camera/" + cam_id
    server_path = "http://10.0.0.228:5000/video/video_feed"

    urls = AQT.StringVector()
    urls.push_back("aqt://Camera9")
    #api = AQT.AquetiAPI("", AQT.U8Vector(), urls)

    env = Environment(render_ip="10.0.0.228", cam_ip="10.1.9.9")

    def vector_to_array(self, c_vector):
        return [c_vector[i].Name() for i in range(0, c_vector.size())]

    def get_image(self):
        time.sleep(0.1)

        stream = cv2.VideoCapture(self.server_path)

        cnt = 0
        success = False
        while not success:
            success, image = stream.read()
            time.sleep(0.1)
            cnt += 1
            if cnt == 10:
                return None

        return image

    def is_image_black(self):
        pass

    def get_info(self):
        return json.loads(self.api.GetParameters(self.cam_path))

    @pytest.mark.skip(reason="")
    def test_displayed_cams(self):
        avp = AquetiViewerPage(self)
        avp.navigate_to()

        list_of_cams_from_api = self.vector_to_array(self.api.GetAvailableCameras()).sort()
        list_of_cams_from_gui = avp.get_camera_list().sort()

        assert list_of_cams_from_api == list_of_cams_from_gui
        assert avp.get_play_btn_status() == 'pause'

    @pytest.mark.skip(reason="")
    def test_step_back(self):
        avp = AquetiViewerPage(self)
        avp.navigate_to()

        avp.live_btn()

        for i in range(0, 3):
            avp.step_back_btn()

            time.sleep(4)

            img1 = self.get_image()
            img2 = self.get_image()

            assert img1 is not None and np.array_equal(img1, img2)

    @pytest.mark.skip(reason="")
    def test_step_forward(self):
        avp = AquetiViewerPage(self)
        avp.navigate_to()

        avp.live_btn()

        for i in range(0, 3):
            avp.step_forward_btn()

            time.sleep(4)

            img1 = self.get_image()
            img2 = self.get_image()

            assert img1 is not None and np.array_equal(img1, img2)

    @pytest.mark.skip(reason="")
    def test_play_pause(self):
        avp = AquetiViewerPage(self)
        avp.navigate_to()

        avp.live_btn()

        for i in range(0, 4):
            avp.play_btn()

            time.sleep(4)

            img1 = self.get_image()
            img2 = self.get_image()

            if i % 2 == 0:
                assert img1 is not None and np.array_equal(img1, img2)
                pass
            else:
                assert img1 is not None and not np.array_equal(img1, img2)
                pass

    @pytest.mark.skip(reason="")
    def test_live(self):
        avp = AquetiViewerPage(self)
        avp.navigate_to()

        avp.live_btn()

        for i in range(0, 3):

            if i == 0:
                avp.play_btn()
            elif i == 1:
                avp.step_back_btn()
            else:
                avp.step_forward_btn()

            time.sleep(2)

            img1 = self.get_image()

            avp.live_btn()

            time.sleep(2)

            img2 = self.get_image()

            assert img1 is not None and not np.array_equal(img1, img2)

    @pytest.mark.skip(reason="")
    def test_ir_filter(self):
        alp = AquetiLoginPage(self)
        alp.navigate_to()

        aaps = alp.login()

        aapc = aaps.open_cam_page(self.cam_id)
        aapc.settings()

        aapc.night_mode_chkb()
        time.sleep(1)
        info = self.get_info()

        assert info['ir'] == False

        aapc.night_mode_chkb()
        time.sleep(1)
        info = self.get_info()

        assert info['ir'] == True

    @pytest.mark.skip(reason="")
    def test_sliders(self):
        alp = AquetiLoginPage(self)
        alp.navigate_to()

        aaps = alp.login()

        aapc = aaps.open_cam_page(self.cam_id)
        aapc.settings()

        for p in [i * 10 for i in range(0, 100)]:
            aapc.sharpening_slider(p)
            aapc.denoising_slider(p)
            aapc.saturation_slider(p)

            info = json.loads(self.api.GetParameters(self.cam_path))

            time.sleep(2.5)

            assert float(info['sharpening']) == float(aapc.sharpening_slider_value.text)
            assert float(info['denoising']) == float(aapc.denoising_slider_value.text)
            assert float(info['saturation']) == float(aapc.saturation_slider_value.text)

        for framerate in [i * 5 for i in range(1, 7)]:
            aapc.framerate_dd(framerate)

            time.sleep(7)

            info = self.get_info()

            assert info['framerate'] == framerate

    @pytest.mark.skip(reason="")
    def test_archive(self):
        def get_rnd_text():
            ch_arr = [chr(ch) for ch in range(ord('a'), ord('z') + 1)]

            res = [ch_arr[random.randint(1, len(ch_arr))] for i in range(random.randint(1, 32))]

            return ''.join(res)

        avp = AquetiViewerPage(self)
        avp.navigate_to()

        path = "/var/tmp/aqueti/"

        for i in range(100):
            alp = avp.click_login_lnk()

            aaps = alp.login()

            arch_name = get_rnd_text()
            summary = get_rnd_text()
            description = get_rnd_text()
            aapi = aaps.click_submit_issue_lnk()
            avp = aapi.submit_issue(arch_name, summary, description)

            out = self.exec("unzip " + path + arch_name + ".zip")

            assert "error" not in out
    
    @pytest.mark.skip(reason="")
    def test_autofocus(self):
        alp = AquetiLoginPage(self)
        alp.navigate_to()

        aaps = alp.login()

        aapc = aaps.open_cam_page(self.cam_id)
        aapc.settings()

        aapc.advanced_tab()
        aaps = aapc.adv_settings_btn()

        aaps.select_sensor(self.cam_id + '0' + str(random.randint(1,19)))

        aaps.sensor_settings()

        time.sleep(5)

        for i in range(1, 10000):
            aaps.mode_focus_btn()

            aaps.coarse_fine_focus_lnk()

            time.sleep(90)

            aaps.make_screenshot()

    @pytest.mark.skip(reason="")
    def test_autofocus1(self):
        alp = AquetiLoginPage(self)
        alp.navigate_to()

        aaps = alp.login()

        aapc = aaps.open_cam_page(str(self.cam_id))

        for i in range(1, 10):
            aapc.settings()

            aapc.focus_tab()

            time.sleep(0.2)
            aapc.ft_mode_btn()
            time.sleep(0.2)

            aapc.ft_coarse_fine_lnk()

            time.sleep(60)

            aapc.advanced_tab()

            aaps = aapc.click_settings_link()

            rnd_sensor_id = [i for i in range(1,19)]

            for sensor_id in rnd_sensor_id:
                while not aaps.sensor_list.is_displayed():
                    time.sleep(0.25)

                aaps.select_sensor(self.cam_id + '0' + str(sensor_id))

                time.sleep(3)

                aaps.make_screenshot()

                if not aaps.focus_val_input.is_displayed():
                    aaps.sensor_settings()

                while aaps.focus_val_input.get_attribute('value') != '0.00':
                    aaps.focus_val_input(value='0')
                    aaps.focus_minus_btn()
                    time.sleep(3)

            aapc = aaps.click_camera_page_lnk()


    @pytest.mark.skip(reason="")
    def test_autofocus2(self):
        alp = AquetiLoginPage(self)
        alp.navigate_to()

        aaps = alp.login()

        aapc = aaps.open_cam_page("9")

        aapc.settings()

        aapc.focus_tab()

        for i in range(1, 100):

            aapc.ft_mode_btn()

            aapc.ft_coarse_fine_lnk()

            time.sleep(90)

            aaps.make_screenshot()


    @pytest.mark.skip(reason="")
    def test_autofocus3(self):
        alp = AquetiLoginPage(self)
        alp.navigate_to()

        aaps = alp.login()

        aapc = aaps.open_cam_page(self.cam_id)

        aapc.settings()

        aapc.advanced_tab()

        aaps = aapc.click_settings_link()

        for i in range(1, 2000):             

            rnd_sensor_id = [i for i in range(1,19)]

            for sensor_id in rnd_sensor_id:
                while not aaps.sensor_list.is_displayed():
                    time.sleep(0.25)

                aaps.select_sensor(self.cam_id + '0' + str(sensor_id))

                time.sleep(2)

                #aaps.make_screenshot()


    @pytest.mark.skip(reason="")
    def test_autofocus4(self):
        alp = AquetiLoginPage(self)
        alp.navigate_to()

        aaps = alp.login()

        aapc = aaps.open_cam_page(self.cam_id)

        aapc.settings()

        aapc.advanced_tab()

        aaps = aapc.click_settings_link() 

        rnd_sensor_id = [i for i in range(1,19)]       

        for i in range(1, 500):

            for sensor_id in rnd_sensor_id:
                while not aaps.sensor_list.is_displayed():
                    time.sleep(0.25)

                aaps.select_sensor(self.cam_id + '0' + str(sensor_id))

                if not aaps.focus_val_input.is_displayed():
                    aaps.sensor_settings()           

                aapc.ft_mode_btn()

                #aapc.ft_coarse_fine_lnk()
                aapc.ft_fine_lnk()

            time.sleep(20)

            for sensor_id in rnd_sensor_id:
                aaps.select_sensor(self.cam_id + '0' + str(sensor_id))

                time.sleep(2)

                aaps.make_screenshot()


    @pytest.mark.skip(reason="")
    def test_gennewmodel(self):
        alp = AquetiLoginPage(self)
        alp.navigate_to()

        aaps = alp.login()

        aapc = aaps.open_cam_page(self.cam_id)
        aapc.settings()

        for i in range(1, 1000):
            aapc.focus_tab()

            aapc.focus_tab_mode_btn()

            aapc.focus_tab_coarse_fine_lnk()

            time.sleep(120)

            aapc.calibrate_tab()

            aapc.calibrate_btn()

            time.sleep(240)

            args = ['mkdir', '/var/tmp/aqueti/modelgen_' + str(i)]
            subprocess.Popen(args)
            args = ['cp', '-r', '/var/tmp/aqueti/modelgen/*.*', '/var/tmp/aqueti/modelgen_' + str(i)]
            subprocess.Popen(args)

            time.sleep(5)

            #aaps.make_screenshot()

    @pytest.mark.skip(reason="")
    def test_gennewmodel2(self):
        alp = AquetiLoginPage(self)
        alp.navigate_to()

        aaps = alp.login()

        aapc = aaps.open_cam_page(self.cam_id)
        aapc.settings()

        for i in range(1, 300):
            aapc.focus_tab()

            aapc.ft_mode_btn()

            aapc.ft_coarse_fine_lnk()

            time.sleep(90)

            aapc.advanced_tab()

            aaps = aapc.click_settings_link()

            rnd_sensor_id = [random.randint(1, 18) for i in range(0, random.randint(10, 20))]

            for sensor_id in set(rnd_sensor_id):
                while not aaps.sensor_list.is_displayed():
                    time.sleep(0.25)

                aaps.select_sensor(self.cam_id + '0' + str(sensor_id))

                if not aaps.focus_val_input.is_displayed():
                    aaps.sensor_settings()

                aaps.focus_val_input("1")

                aaps.focus_plus_btn()

            time.sleep(5)

            aapc = aaps.click_camera_page_lnk()

            aapc.settings()

            aapc.calibrate_tab()

            aapc.calibrate_btn()

            time.sleep(250)

            os.system('rm -rf /var/tmp/aqueti/modelgen/H26X/')           
            
            args = ['cp', '-r', '/var/tmp/aqueti/modelgen/', '/var/tmp/aqueti/modelgen_' + str(i)]
            subprocess.Popen(args)
            time.sleep(1)

            os.system('rm -rf /var/tmp/aqueti/modelgen/')

            # aaps.make_screenshot()
    

    @pytest.mark.skip(reason="")
    def test_switch_to_fovea(self):
        alp = AquetiLoginPage(self)
        alp.navigate_to()

        aaps = alp.login()

        aapc = aaps.open_cam_page("7")

        for i in range(200):
            aapc.settings_btn()

            aapc.viewer_encoding_dd()

            if i % 2 == 0:
                aapc.viewer_direct_lnk()
            else:
                aapc.viewer_webstream_lnk()

            aapc.viewer_update_btn()


            time.sleep(10)


    @pytest.mark.skip(reason="")
    def test_block_per_cont(self):
        alp = AquetiLoginPage(self)
        alp.navigate_to()

        aaps = alp.login()
        aapc = aaps

        cache_size = 9999
        while True:
            for i in range(16):
                aapst = aapc.open_storage_page()

                aapst.data_module_settings_tab(act="click")

                aapst.blocks_per_cont_txt(value=str(i))
                aapst.blocks_per_cont_plus()

                aapst.max_storage_threads_txt(value=str(i))
                aapst.max_storage_threads_plus()

                aapc = aapst.open_cam_page(self.cam_id)

                aapc.recording_btn()

                time.sleep(4*60)

                aapc.recording_btn()

                time.sleep(0.25*60)

            time.sleep(2*60)

            try:
                tc_size = cache_size * (i // 2)
                if tc_size > 99999:
                    tc_size = cache_size

                aapst.cache_size_txt(value=str(tc_size))
                aapst.cache_size_plus()
            except:
                pass


class TestQAdmin(BaseTest):
    browser = "chrome"

    env = Environment(render_ip="10.0.0.228", cam_ip="10.1.9.9")

    cam_id = '9'
    cam_name = '/aqt/camera/' + cam_id
    system_name = "Camera9"

    api = None
    qvp = None

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
        super(TestQAdmin, self).setup_method(method)

        urls = AQT.StringVector()
        urls.push_back("aqt://" + self.system_name)
        self.api = AQT.AquetiAPI("", AQT.U8Vector(), urls)

        self.qvp = QViewPage(self)
        self.qvp.navigate_to()

        self.qvp.login(system=self.system_name)

    def teardown_method(self, method):
        super(TestQAdmin, self).teardown_method(method)

        self.restore_defaults()

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

    @pytest.mark.skip(reason="")
    def test_links_on_dashboard(self):
        qad = QAdminDashboard(self)
        qad.navigate_to()

        qad.TIMEOUT = 5

        qas = qad.click_system_lnk()

        assert qas.page_url == qas.cur_page_url

        qad.navigate_to()

        time.sleep(1)

        qac = qad.click_camera_lnk()

        assert qac.page_url == qac.cur_page_url

        qad.navigate_to()

        time.sleep(1)

        qas = qad.click_storage_lnk()

        assert qas.page_url == qas.cur_page_url

        qad.navigate_to()

        time.sleep(1)

        qar = qad.click_render_lnk()

        assert qar.page_url == qar.cur_page_url

    @pytest.mark.skip(reason="")
    def test_mcams_num(self):
        qad = QAdminDashboard(self)
        qad.navigate_to()

        qad.TIMEOUT = 5

        qac = qad.click_camera_lnk()

        qac.TIMEOUT = 10

        cams = qac.get_mcams_number('77') # 0 - available, 1 - total

        assert int(cams[0]) == 20 and int(cams[1]) == 20

    @pytest.mark.skip(reason="")
    def test_mcams_recording_status(self):
        qad = QAdminDashboard(self)
        qad.navigate_to()

        qad.TIMEOUT = 5

        qac = qad.menu_camera()

        qac.TIMEOUT = 15

        qacr = qac.menu_cam_reservations()

        time.sleep(0.5)

        qacr.camera_dd()

        qacr.get_dd_elem(self.cam_id)()

        qacr.recording_chkb()

        time.sleep(0.5)

        qacr.menu_camera()

        is_streaming = qac.get_stream_status(self.cam_id)

        is_recording = qac.get_rec_status(self.cam_id)

        assert is_streaming and is_recording

    @pytest.mark.skip(reason="")
    def test_compression(self):
        qad = QAdminDashboard(self)
        qad.navigate_to()

        qacs = qad.menu_cam_settings()

        time.sleep(2)

        qacs.compression_tab()

        qacs.compression_dd()

        time.sleep(0.5)

        cmp_types = ["high","medium","low"]

        for cmp_type in cmp_types:
            qacs.get_dd_elem(cmp_type)()
            time.sleep(5)

    @pytest.mark.skip(reason="")
    def test_global_loop(self):
        qad = QAdminDashboard(self)
        qad.navigate_to()

        qacs = qad.menu_cam_settings()

        time.sleep(2)

        if qacs.global_chkb.is_selected():
            qacs.global_chkb()

        time.sleep(1)

        qacs.global_txt(value="1")

    @pytest.mark.skip(reason="")
    def test_exposure(self):
        qad = QAdminDashboard(self)
        qad.navigate_to()

        qacs = qad.menu_cam_settings()

        time.sleep(2)

        if qacs.global_chkb.is_selected():
            qacs.global_chkb()
            time.sleep(1)

        if qacs.exposure_chkb.is_selected():
            qacs.exposure_chkb()
            time.sleep(1)

        if qacs.analog_gain_chkb.is_selected():
            qacs.analog_gain_chkb()
            time.sleep(1)

        qacs.global_txt(value='2')

        qacs.exposure_txt(value='3')

        qacs.analog_gain_txt(value='3')

        qacs.digital_gain_txt(value='3')

    @pytest.mark.skip(reason="")
    def test_sharpening(self):
        qad = QAdminDashboard(self)
        qad.navigate_to()

        qacs = qad.menu_cam_settings()

        time.sleep(2)

        qacs.sharpening_txt(value='0')

        qacs.denoising_txt(value='0')

        qacs.saturation_txt(value='0')

    @pytest.mark.skip(reason="")
    def test_night_mode(self):
        qad = QAdminDashboard(self)
        qad.navigate_to()

        qacs = qad.menu_cam_settings()

        time.sleep(2)

        for i in range(0,10):
            qacs.night_mode_chkb()
            time.sleep(2)

    @pytest.mark.skip(reason="")
    def test_framerate(self):
        qad = QAdminDashboard(self)
        qad.navigate_to()

        qacs = qad.menu_cam_settings()

        time.sleep(2)

        fr_arr = ["5","10","15","20","25","30"]

        for fr_val in fr_arr:
            qacs.framerate_dd()
            while not qacs.get_dd_elem(fr_val, False).is_displayed():
                time.sleep(0.5)
            qacs.get_dd_elem(fr_val, False)(act="click")
            time.sleep(3)

    @pytest.mark.skip(reason="")
    def test_autowb(self):
        qad = QAdminDashboard(self)
        qad.navigate_to()

        qacs = qad.menu_cam_settings()

        time.sleep(2)

        if qacs.global_chkb.is_selected():
            qacs.global_chkb()

        time.sleep(1)

        wb_arr = ["AUTO","CLOUDY","FIXED","FLUORESCENT","HORIZON","INCANDESCENT","SHADE","SUNLIGHT","TUNGSTEN"]

        for wb_val in wb_arr:
            qacs.whitebalance_dd()
            while not qacs.get_dd_elem(wb_val).is_displayed():
                time.sleep(0.5)
            qacs.get_dd_elem(wb_val)(act="click")
            time.sleep(3)

        #add func to check black screen

    @pytest.mark.skip(reason="")
    def test_focum_mcam(self):
        qad = QAdminDashboard(self)
        qad.navigate_to()

        qacm = qad.menu_cam_microcameras()

        time.sleep(2)

        qacm.camera_dd()

        qacm.get_dd_elem(self.cam_id)(act="click")

        time.sleep(1)

        qacm.microcamera_dd()

        qacm.get_dd_elem(self.cam_id + '0' + str(random.randint(1,19)))(act="click")

        time.sleep(2)

        qacm.focus_txt(value="0.55")

        qacm.focus_coarse_btn()

        time.sleep(30)

    @pytest.mark.skip(reason="")
    def test_storage(self):
        qad = QAdminDashboard(self)
        qad.navigate_to()

        qass = qad.menu_storage_settings()

        qass.block_size_txt(value="4194304")

        qass.blocks_per_cont_txt(value="16")

        qass.max_storage_threads_txt(value="16")

        qass.cache_size_txt(value="10000")

        qass.garbage_collection_threshold_txt(value="90")

        qass.garbage_collection_interval_txt(value="60")

        qass.maximum_disk_usage_txt(value="99")

        time.sleep(5)

    @pytest.mark.skip(reason="")
    def test_calibration(self):
        qad = QAdminDashboard(self)
        qad.navigate_to()

        qac = qad.menu_cam_settings()

        qac.cam_select_dd("18")

        qac.calibrate_tab()

        for i in range(0, 100):
            qac.ct_calibrate_btn()

            num_of_docs = self.get_col_obj("acos", "models").count()

            time.sleep(240)

            assert self.get_col_obj("acos", "models").count() == (num_of_docs + 1)
    
    @pytest.mark.skip(reason="")
    def test_submit_issue(self):
        qad = QAdminDashboard(self)
        qad.navigate_to()

        qad.submit_issue_icon()
        qad.submit_issue(filename=TD.file_name, summary="test", description="test")

        time.sleep(5)

        assert os.path.isfile("/var/tmp/aqueti/" + TD.file_name + ".zip")

    @pytest.mark.skip(reason="")
    def test_cs_type(self):
        qvp = self.qvp

        for ctype in ['LOCALDISPLAY', 'H264']:
            try:
                qvp.settings_menu_icon()
            except:
                pass

            qvp.customize_stream_btn()
            time.sleep(1)
            qvp.type_dd()
            qvp.get_dd_elem(ctype)(act="click")

            qvp.cs_update_btn()
            time.sleep(15)

            assert True  # make screenshot, pic in web gui

    @pytest.mark.skip(reason="")
    def test_export_avi(self):
        qvp = self.qvp

        qvp.left_menu_icon()

        qvp.remove_all_avi_items()

        qvp.export_avi_chkb()
        time.sleep(5)
        qvp.export_avi_chkb()
        time.sleep(5)

        files = [f for f in os.listdir("/var/tmp/aqueti/avi/") if re.match(r'.*\.avi', f)]

        assert len(qvp.get_avi_items()) == 1

        assert len(files) == 1

        assert qvp.get_avi_items()[0].get_attribute('innerText').split()[0].strip() == files[0]

        #assert "/var/tmp/aqueti/avi/" + qvp.get_avi_items()[0].get_attribute('innerText').split()[0].strip() == files[0]

    @pytest.mark.skip(reason="")
    def test_auto_loop_on(self):
        qad = QAdminDashboard(self)
        qad.navigate_to()

        qacs = qad.menu_cam_settings()

        if qacs.auto_chkb.is_checked():
            qacs.auto_chkb()
            qacs.auto_disable_btn()
            time.sleep(2)

        qacs.auto_chkb()

        info = self.get_params()

        assert info["system_auto_enabled"] == True
        assert info["auto_exposure_enabled"] == False
        assert info["auto_analog_gain_enabled"] == False
        assert info["auto_digital_gain_enabled"] == False

    @pytest.mark.skip(reason="")
    def test_auto_loop_off(self):
        qad = QAdminDashboard(self)
        qad.navigate_to()

        qacs = qad.menu_cam_settings()

        if not qacs.auto_chkb.is_checked():
            qacs.auto_chkb()
            time.sleep(2)

        qacs.auto_chkb()
        qacs.auto_disable_btn()

        info = self.get_params()

        assert info["system_auto_enabled"] == False
        assert info["auto_exposure_enabled"] == True
        assert info["auto_analog_gain_enabled"] == False
        assert info["auto_digital_gain_enabled"] == False

    @pytest.mark.skip(reason="")
    def test_set_global_loop(self):
        qad = QAdminDashboard(self)
        qad.navigate_to()

        qacs = qad.menu_cam_settings()

        if not qacs.auto_chkb.is_checked():
            qacs.auto_chkb()

        while qacs.auto_txt.get_attribute("value") != "0":
            qacs.auto_slider(value="-" + qacs.auto_txt.get_attribute("value") + ";0.4")
            time.sleep(3)

        info = self.get_params()

        assert info['system_auto_interval'] == 0

        qacs.make_screenshot()

    @pytest.mark.skip(reason="")
    def test_set_exposure_time(self):
        qad = QAdminDashboard(self)
        qad.navigate_to()

        qacs = qad.menu_cam_settings()

        if qacs.auto_chkb.is_checked():
            qacs.auto_chkb()
            qacs.auto_disable_btn()
            time.sleep(7)

        if qacs.exposure_chkb.is_checked():
            qacs.exposure_chkb()
            time.sleep(7)

        qacs.analog_gain_slider(value="8;9")
        time.sleep(10)

        qacs.make_screenshot()

        EXPOSURE_MAX = 22 # 33

        while float(qacs.exposure_txt.get_attribute("value")) < EXPOSURE_MAX:
            qacs.exposure_slider(value="2;5")

        info = self.get_params()

        qacs.make_screenshot()

        assert info['exposure_time_milliseconds'] == EXPOSURE_MAX


    @pytest.mark.skip(reason="")
    def test_set_analog_gain(self):
        qad = QAdminDashboard(self)
        qad.navigate_to()

        qacs = qad.menu_cam_settings()

        if qacs.auto_chkb.is_checked():
            qacs.auto_chkb()
            qacs.auto_disable_btn()
            time.sleep(7)

        if qacs.exposure_chkb.is_checked():
            qacs.exposure_chkb()
            time.sleep(7)

        qacs.exposure_slider(value="8;5")
        time.sleep(10)

        qacs.make_screenshot()

        ANALOG_GAIN_MAX = 22

        while float(qacs.analog_gain_txt.get_attribute("value")) < ANALOG_GAIN_MAX:
            qacs.analog_gain_slider(value="2;5")

        info = self.get_params()

        qacs.make_screenshot()

        assert info['analog_gain'] == ANALOG_GAIN_MAX

    @pytest.mark.skip(reason="")
    def test_set_digital_gain(self):
        qad = QAdminDashboard(self)
        qad.navigate_to()

        qacs = qad.menu_cam_settings()

        if qacs.auto_chkb.is_checked():
            qacs.auto_chkb()
            qacs.auto_disable_btn()
            time.sleep(7)

        if qacs.exposure_chkb.is_checked():
            qacs.exposure_chkb()
            time.sleep(7)

        qacs.exposure_slider(value="8;5")
        time.sleep(10)

        qacs.make_screenshot()

        DIGITAL_GAIN_MAX = 10

        qacs.move_digital_gain_slider(10)

        info = self.get_params()

        qacs.make_screenshot()

        assert info['digital_gain'] == DIGITAL_GAIN_MAX

    def test_focus_after_tegras_reboot(self):
        qad = QAdminDashboard(self)
        qad.navigate_to()

        qadcc = qad.menu_cam_microcameras()

        while True:
            while self.env.cam.get_status() != "active":                
                time.sleep(5)

            # qadcc.camera_dd()
            # qadcc.get_dd_elem(self.cam_id)(act="click")

            for i in range(1, 19): #self.env.cam.num_of_tegras
                qadcc.microcamera_dd()
                time.sleep(0.5)
                qadcc.get_dd_elem(self.cam_id + '0' + str(i))(act="click")
                time.sleep(3)
                qadcc.make_screenshot()
            
            self.env.cam.reboot()

            #time.sleep(150)

            while self.env.cam.get_status() == "active":
                time.sleep(5)

        time.sleep(5)


class TestState(BaseTest):
    browser = None

    env = Environment(render_ip="10.0.0.204", cam_ip="10.1.77.10")

    @pytest.mark.skip(reason="")
    def clear_state(self, render_path, tegra_path):
        self.env.cam.copy_remote_file(path_to=render_path, path_from=tegra_path, from_tegra=[1])

        with open(render_path) as f:
            try:
                data = json.load(f)
            except:
                exit(1)

        root_e = list(data.keys())[0]

        for e in data[root_e]:
            if re.match("\d+", e):
                data[root_e][e]['focus_count'] = 0
                data[root_e][e]['focus_position'] = 0
                data[root_e][e]['ir_count'] = 0
                data[root_e][e]['ir_status'] = False
            elif e == "cumulative_run_time":
                data[root_e][e] = 0
            elif e == "current_run_time":
                data[root_e][e] = 0

        with open(render_path, 'w') as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True)

        self.env.cam.copy_remote_file(path_from=render_path, path_to=tegra_path, to_tegra=[1])

    @pytest.mark.skip(reason="")
    def test_state(self):
        render_path = "/home/astepenko/state.json"
        tegra_path = "/etc/aqueti/state.json"

        self.clear_state(render_path, tegra_path)

        sleep_time = 60
        cumrt_next = 0
        for i in range(2 * 60):
            self.env.cam.restart(tegra=[1])

            time.sleep(sleep_time)

            res = json.loads(self.env.cam.read(f_name=tegra_path, tegra=[1]))

            cumrt = res[list(res.keys())[0]]['cumulative_run_time']
            currt = res[list(res.keys())[0]]['current_run_time']

            print('\n%s' % i)
            print('cumulative_run_time: %s' % cumrt)
            print('current_run_time: %s' % currt)


            assert (sleep_time - math.ceil(currt / 1e6)) < 15 and cumrt_next == cumrt

            cumrt_next = cumrt + currt
