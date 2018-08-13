import pytest
from selenium.webdriver.common.keys import Keys
from BaseTest import BaseTest
from AquetiPage import *
import AQT
import time
import cv2


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
        aap_sys = AquetiAdminPageStatusCamera(self)
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

        aap_sys = alp.login("admin", "1234")

        assert aap_sys.page_url == alp.cur_page_url

    @pytest.mark.skip(reason="")
    def test_login_empty_credentials(self):
        alp = AquetiLoginPage(self)
        alp.navigate_to()

        aap_sys = alp.login("", "")

        assert alp.page_url in aap_sys.cur_page_url

    @pytest.mark.skip(reason="")
    def test_login_incorrect_login(self):
        alp = AquetiLoginPage(self)
        alp.navigate_to()

        aap_sys = alp.login("nimda", "1234")

        assert "Not Authorized to view this page" in alp.cur_page_source

    @pytest.mark.skip(reason="")
    def test_login_incorrect_password(self):
        alp = AquetiLoginPage(self)
        alp.navigate_to()

        aap_sys = alp.login("admin", "4321")

        assert "Not Authorized to view this page" in alp.cur_page_source

    @pytest.mark.skip(reason="")
    def test_login_unauthorized_access(self):
        alp = AquetiLoginPage(self)
        alp.navigate_to()

        aap_sys = AquetiAdminPageStatusCamera(self)
        aap_sys.navigate_to()

        assert "Not Authorized to view this page" in aap_sys.cur_page_source

        aap_ss = AquetiAdminPageStatusStorage(self)
        aap_ss.navigate_to()

        assert "Not Authorized to view this page" in aap_ss.cur_page_source

        aap_sr = AquetiAdminPageStatusRender(self)
        aap_sr.navigate_to()

        assert "Not Authorized to view this page" in aap_sr.cur_page_source

        aap_cs = AquetiAdminPageConfigurationSystem(self)
        aap_cs.navigate_to()

        assert "Not Authorized to view this page" in aap_cs.cur_page_source

        aap_cc = AquetiAdminPageConfigurationCamera(self)
        aap_cc.navigate_to()

        assert "Not Authorized to view this page" in aap_cc.cur_page_source

        aap_cst = AquetiAdminPageConfigurationStorage(self)
        aap_cst.navigate_to()

        assert "Not Authorized to view this page" in aap_cst.cur_page_source

        aap_cr = AquetiAdminPageConfigurationRender(self)
        aap_cr.navigate_to()

        assert "Not Authorized to view this page" in aap_cr.cur_page_source

        aap_mc = AquetiAdminPageMaintenanceCamera(self)
        aap_mc.navigate_to()

        assert "Not Authorized to view this page" in aap_mc.cur_page_source

        aap_ms = AquetiAdminPageMaintenanceStorage(self)
        aap_ms.navigate_to()

        assert "Not Authorized to view this page" in aap_ms.cur_page_source

        aap_mr = AquetiAdminPageMaintenanceRender(self)
        aap_mr.navigate_to()

        assert "Not Authorized to view this page" in aap_mr.cur_page_source

        aap_r = AquetiAdminPageRecordings(self)
        aap_r.navigate_to()

        assert "Not Authorized to view this page" in aap_r.cur_page_source

        aap_i = AquetiAdminPageIssue(self)
        aap_i.navigate_to()

        assert "Not Authorized to view this page" in aap_i.cur_page_source

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
