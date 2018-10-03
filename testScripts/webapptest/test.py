import pytest
from selenium.webdriver.common.keys import Keys
from BaseTest import BaseTest
from AquetiPage import *
from QAdminPage import *
import time
import cv2
import json
import numpy as np
import subprocess
import os
try:
    import AQT
except ImportError:
    print('no AQT lib found')
    exit(1)


class TD:
    username = "admin"
    password = "1234"

    cam_props = {"status": "online",
                 "recording": "false",
                 "serialid": "undefined",
                 "software": "undefined",
                 "kernel": "undefined",
                 "host": "undefined"}

    sensor_props = {"model": "imx274",
                    "host": "87878"}

    storage_props = {"status": "online",
                     "serialid": "aqt:Storage:1",
                     "software": "undefined",
                     "kernel": "undefined",
                     "host": "undefined"}

    render_props = {"serialid": "",
                    "software": "undefined",
                    "kernel": "undefined",
                    "host": "undefined"}


class TestWebApp(BaseTest):
    browser = "chrome"

    @pytest.mark.skip(reason="")
    def test_cam_properties(self):
        aap_sys = AquetiAdminPageSystem(self)
        aap_sys.navigate_to()
        comps = aap_sys.components

        print(aap_sys.system_current_time.text)
        print(aap_sys.system_current_date.text)

        assert len(comps) == 2

        #for comp in comps:
        #    self.assertIn("ferg", comp.text)

        comps[0].click()

        assert aap_sys.prop_status.text == TD.cam_props["status"]
        assert aap_sys.prop_recording.text == TD.cam_props["recording"]
        assert aap_sys.prop_serialid.text == TD.cam_props["serialid"]
        assert aap_sys.prop_software.text == TD.cam_props["software"]
        assert aap_sys.prop_kernel.text == TD.cam_props["kernel"]
        assert aap_sys.prop_host.text == TD.cam_props["host"]

        assert aap_sys.prop_sensor_model.text == TD.sensor_props["model"]
        assert aap_sys.prop_sensor_host.text == TD.sensor_props["host"]

    @pytest.mark.skip(reason="")
    def test_stor_properties(self):
        aap_ss = AquetiAdminPageStatusStorage(self)
        aap_ss.navigate_to()
        comps = aap_ss.components

        assert len(comps) == 2

        #for comp in comps:
        #    self.assertIn("aqt:Storage:", comp.text)

        comps[0].click()

        assert aap_ss.prop_status.text == TD.storage_props["status"]
        assert aap_ss.prop_serialid.text == TD.storage_props["serialid"]
        assert aap_ss.prop_software.text == TD.storage_props["software"]
        assert aap_ss.prop_kernel.text == TD.storage_props["kernel"]
        assert aap_ss.prop_host.text == TD.storage_props["host"]

    @pytest.mark.skip(reason="")
    def test_render_properties(self):
        aap_sr = AquetiAdminPageStatusRender(self)
        aap_sr.navigate_to()
        comps = aap_sr.components

        assert comps is None

        assert aap_sr.prop_serialid.text == TD.render_props["serialid"]
        assert aap_sr.prop_software.text == TD.render_props["software"]
        assert aap_sr.prop_kernel.text == TD.render_props["kernel"]
        assert aap_sr.prop_host.text == TD.render_props["host"]

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

    cam_id = "12"
    cam_path = "/aqt/camera" + cam_id
    server_path = "http://10.0.0.232:5000/video/video_feed"

    urls = AQT.StringVector()
    urls.push_back("aqt://Camera12")
    api = AQT.AquetiAPI("", AQT.U8Vector(), urls)

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

        # info['digital_gain']
        # info['analog_gain']
        #
        # info['whitebalance_mode']
        # info['auto_digtial_gain_enabled']
        # info['system_auto_interval']
        # info['operating_mode']
        # info['quality']
        # info['auto_whitebalance']
        # info['ir']
        # info['auto_model_generation_interval_seconds']
        # info['auto_exposure_enabled']
        #
        # info['auto_whitebalance_interval_seconds']
        # info['auto_model_generation_enabled']
        #
        # info['system_auto_enabled']
        # info['auto_analog_gain_enabled']
        # info['data_routing_policy']
        #
        # info['exposure_time_milliseconds']

        for framerate in [i * 5 for i in range(1, 7)]:
            aapc.framerate_dd(framerate)

            time.sleep(7)

            info = self.get_info()

            assert info['framerate'] == framerate

    @pytest.mark.skip(reason="")
    def test_autofocus(self):
        alp = AquetiLoginPage(self)
        alp.navigate_to()

        aaps = alp.login()

        aapc = aaps.open_cam_page("12")
        aapc.settings()

        aapc.advanced_tab()
        aaps = aapc.adv_settings_btn()

        aaps.select_sensor('1209')

        aaps.sensor_settings()

        time.sleep(5)

        for i in range(1, 10000):
            aaps.mode_focus_btn()

            aaps.coarse_fine_focus_lnk()

            time.sleep(60)

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
    def test_gennewmodel(self):
        alp = AquetiLoginPage(self)
        alp.navigate_to()

        aaps = alp.login()

        aapc = aaps.open_cam_page(self.cam_id)
        aapc.settings()

        for i in range(1, 1000):
            aapc.focus_tab()

            aapc.ft_mode_btn()

            aapc.ft_coarse_fine_lnk()

            time.sleep(120)

            aapc.advanced_tab()

            aaps = aapc.click_settings_link()

            rnd_sensor_id = [random.randint(1, 18) for i in range(0, random.randint(1, 9))]

            for sensor_id in set(rnd_sensor_id):
                while not aaps.sensor_list.is_displayed():
                    time.sleep(0.25)

                aaps.select_sensor(str(self.cam_id) + '0' + str(sensor_id))

                if not aaps.focus_val_input.is_displayed():
                    aaps.sensor_settings()

                aaps.focus_val_input("1")

                aaps.focus_plus_btn()

            time.sleep(5)

            aapc = aaps.click_camera_page_lnk()

            aapc.settings()

            aapc.calibrate_tab()

            aapc.calibrate_btn()

            time.sleep(240)

            args = ['mkdir', '/var/tmp/aqueti/modelgen_' + str(i)]
            subprocess.Popen(args).wait()
            args = ['cp', '-r', '/var/tmp/aqueti/modelgen/*.*', '/var/tmp/aqueti/modelgen_' + str(i)]
            subprocess.Popen(args).wait()

            aaps.make_screenshot()

class TestQAdmin(BaseTest):
    browser = "chrome"

    cam_id = '12'

    @pytest.mark.skip(reason="")
    def test_qadmin(self):
        qad = QAdminDashboard(self)
        qad.navigate_to()

        #qad.camera_lnk()
        time.sleep(1)
        qad.storage_lnk()
        time.sleep(1)
        qad.render_lnk()
        time.sleep(1)
        qad.system_lnk()
        time.sleep(1)
        qad.logs_lnk()
        time.sleep(1)
        qad.dashboard_lnk()
        time.sleep(1)

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

        cams = qac.get_mcams_number('12') # 0 - available, 1 - total

        assert int(cams[0]) == 19 and int(cams[1]) == 19

    @pytest.mark.skip(reason="")
    def test_mcams_num2(self):
        qad = QAdminDashboard(self)
        qad.navigate_to()

        qad.TIMEOUT = 5

        qac = qad.click_camera_lnk()

        qac.TIMEOUT = 10

        cams = qac.get_mcams_number('12') # 0 - available, 1 - total

        assert int(cams[0]) == 19 and int(cams[1]) == 19

    @pytest.mark.skip(reason="")
    def test_mcams_num3(self):
        qad = QAdminDashboard(self)
        qad.navigate_to()

        qad.TIMEOUT = 5

        qac = qad.click_camera_lnk()

        qac.TIMEOUT = 10

        cams = qac.get_mcams_number('12') # 0 - available, 1 - total

        assert int(cams[0]) == 19 and int(cams[1]) == 19

    @pytest.mark.skip(reason="")
    def test_mcams_recording_status(self):
        qad = QAdminDashboard(self)
        qad.navigate_to()

        qad.TIMEOUT = 5

        qac = qad.menu_camera()

        qac.TIMEOUT = 15

        qacr = qac.menu_reservations()

        qacr.camera_dd()

        qacr.get_dd_value(self.cam_id)()

        qacr.recording_chkb()

        time.sleep(0.5)

        qacr.menu_camera()

        is_streaming = qac.get_stream_status(self.cam_id)

        is_recording = qac.get_rec_status(self.cam_id)

        assert is_streaming and  is_recording

    #@pytest.mark.skip(reason="")
    def test_mcams_recording_status2(self):
        qad = QAdminDashboard(self)
        qad.navigate_to()

        qacs = qad.menu_cam_settings()

        time.sleep(2)

        qacs.compression_tab()

        qacs.compression_dd()

        time.sleep(0.5)

        qacs.get_dd_value("high")()

        time.sleep(1)