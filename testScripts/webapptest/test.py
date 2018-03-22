import unittest
from selenium.webdriver.common.keys import Keys
from BaseTest import BaseTest
from AquetiAdminPage import *
import AQT


class TD:
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


class APITest(BaseTest):
    browser = "chrome"

    api = AQT.AquetiAPI()

    vs = AQT.ViewState(api)
    ts = AQT.TimeState(api)
    iss = AQT.ImageSubsetState(api)
    ps = AQT.PoseState(api)
    sp = AQT.StreamProperties()
    rapi = AQT.RenderStream(api, vs, ts, iss, ps, sp)

    @unittest.SkipTest
    def test_cam_properties(self):
        aap_sc = AquetiAdminPageStatusCamera(self)
        self.navigate_to(aap_sc.page_url)
        comps = aap_sc.components

        print(aap_sc.system_current_time.text)
        print(aap_sc.system_current_date.text)

        self.assertEqual(len(comps), 2)

        #for comp in comps:
        #    self.assertIn("ferg", comp.text)

        comps[0].click()

        self.assertEqual(aap_sc.prop_status.text, TD.cam_props["status"])
        self.assertEqual(aap_sc.prop_recording.text, TD.cam_props["recording"])
        self.assertEqual(aap_sc.prop_serialid.text, TD.cam_props["serialid"])
        self.assertEqual(aap_sc.prop_software.text, TD.cam_props["software"])
        self.assertEqual(aap_sc.prop_kernel.text, TD.cam_props["kernel"])
        self.assertEqual(aap_sc.prop_host.text, TD.cam_props["host"])

        self.assertEqual(aap_sc.prop_sensor_model.text, TD.sensor_props["model"])
        self.assertEqual(aap_sc.prop_sensor_host.text, TD.sensor_props["host"])

    @unittest.SkipTest
    def test_stor_properties(self):
        aap_ss = AquetiAdminPageStatusStorage(self)
        self.navigate_to(aap_ss.page_url)
        comps = aap_ss.components

        self.assertEqual(len(comps), 2)

        #for comp in comps:
        #    self.assertIn("aqt:Storage:", comp.text)

        comps[0].click()

        self.assertEqual(aap_ss.prop_status.text, TD.storage_props["status"])
        self.assertEqual(aap_ss.prop_serialid.text, TD.storage_props["serialid"])
        self.assertEqual(aap_ss.prop_software.text, TD.storage_props["software"])
        self.assertEqual(aap_ss.prop_kernel.text, TD.storage_props["kernel"])
        self.assertEqual(aap_ss.prop_host.text, TD.storage_props["host"])

    @unittest.SkipTest
    def test_render_properties(self):
        aap_sr = AquetiAdminPageStatusRender(self)
        self.navigate_to(aap_sr.page_url)
        comps = aap_sr.components

        self.assertIsNone(comps)

        self.assertEqual(aap_sr.prop_serialid.text, TD.render_props["serialid"])
        self.assertEqual(aap_sr.prop_software.text, TD.render_props["software"])
        self.assertEqual(aap_sr.prop_kernel.text, TD.render_props["kernel"])
        self.assertEqual(aap_sr.prop_host.text, TD.render_props["host"])

    @unittest.SkipTest
    def test_title(self):
        aap_i = AquetiAdminPageIssue(self)
        self.navigate_to(aap_i.page_url)

        aap_sc = aap_i.submit_issue("title", "summary", "description")

        self.assertEqual(aap_sc.page_url, aap_sc.cur_page_url)

    @unittest.SkipTest
    def test_comp_name_update(self):
        aap_cc = AquetiAdminPageConfigurationCamera(self)
        self.navigate_to(aap_cc.page_url)

        nickname = "test"

        aap_cc.update_nickname(nickname)

        self.assertEqual(nickname, aap_cc.nickname.text)

    @unittest.SkipTest
    def test_internal_error(self):
        aap_sc = AquetiAdminPageStatusCamera(self)
        self.navigate_to(aap_sc.page_url)

        aap_sc._(aap_sc.host)

        self.assertIn("Internal Server Error", aap_sc.cur_page_source)

    @unittest.SkipTest
    def test_settings(self):
        aap_cc = AquetiAdminPageConfigurationCamera(self)
        self.navigate_to(aap_cc.page_url)

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

        self.assertEquals(self.api.GetParameters("sharpening"), 20)

    @unittest.SkipTest
    def test_sc_move(self):
        aap_cc = AquetiAdminPageConfigurationCamera(self)
        self.navigate_to(aap_cc.page_url)

        aap_cc.click_links()

        aap_cc = AquetiAdminPageConfigurationCamera(self)
        self.navigate_to(aap_cc.page_url)

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

        self.assertNotEquals(vs['before'], vs['up'])
        self.assertNotEquals(vs['up'], vs['down'])
        self.assertNotEquals(vs['down'], vs['left'])
        self.assertNotEquals(vs['left'], vs['right'])
        self.assertNotEquals(vs['right'], vs['before'])

    @unittest.SkipTest
    def test_sc_zoom(self):
        aap_cc = AquetiAdminPageConfigurationCamera(self)
        self.navigate_to(aap_cc.page_url)

        vs = dict()
        vs['before'] = self.vs.Zoom()
        self.vs.Zoom(self.vs.Zoom() * 2)
        vs['in'] = self.vs.Zoom()
        self.vs.Zoom(self.vs.Zoom() * 0.6)
        vs['out'] = self.vs.Zoom()

        print("{0}\n{1}\n{2}".format(vs['before'], vs['in'], vs['out']))

        self.assertEquals(vs['before'] * 2, vs['in'])
        self.assertEquals(vs['in'] * 0.6, vs['out'])


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(APITest)
    unittest.TextTestRunner().run(suite)
