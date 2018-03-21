import unittest
from BaseTest import BaseTest
from AquetiAdminPage import *
import time


class Test(BaseTest):
    browser = "chrome"

    @unittest.SkipTest
    def test_0(self):
        aap_sc = AquetiAdminPageStatusCamera(self.driver)
        self.navigate_to(aap_sc.page_url)
        comps = aap_sc.components

        print(aap_sc.system_current_time.text)
        print(aap_sc.system_current_date.text)

        self.assertEqual(len(comps), 2)

        for comp in comps:
            self.assertIn("aqt:Camera:", comp.text)

        comps[0].click()

        self.assertEqual(aap_sc.prop_status.text, "online")
        self.assertEqual(aap_sc.prop_recording.text, "false")
        self.assertEqual(aap_sc.prop_serialid.text, "undefined")
        self.assertEqual(aap_sc.prop_software.text, "undefined")
        self.assertEqual(aap_sc.prop_kernel.text, "undefined")
        self.assertEqual(aap_sc.prop_host.text, "undefined")

        self.assertEqual(aap_sc.prop_sensor_model.text, "imx274")
        self.assertEqual(aap_sc.prop_sensor_host.text, "87878")

    @unittest.SkipTest
    def test_1(self):
        aap_ss = AquetiAdminPageStatusStorage(self.driver)
        self.navigate_to(aap_ss.page_url)
        comps = aap_ss.components

        self.assertEqual(len(comps), 2)

        for comp in comps:
            self.assertIn("aqt:Storage:", comp.text)

        comps[0].click()

        self.assertEqual(aap_ss.prop_status.text, "online")
        self.assertEqual(aap_ss.prop_serialid.text, "aqt:Storage:1")
        self.assertEqual(aap_ss.prop_software.text, "undefined")
        self.assertEqual(aap_ss.prop_kernel.text, "undefined")
        self.assertEqual(aap_ss.prop_host.text, "undefined")

    @unittest.SkipTest
    def test_2(self):
        aap_sr = AquetiAdminPageStatusRender(self.driver)
        self.navigate_to(aap_sr.page_url)
        comps = aap_sr.components

        self.assertIsNone(comps)

        self.assertEqual(aap_sr.prop_serialid.text, "")
        self.assertEqual(aap_sr.prop_software.text, "undefined")
        self.assertEqual(aap_sr.prop_kernel.text, "undefined")
        self.assertEqual(aap_sr.prop_host.text, "undefined")

    @unittest.SkipTest
    def test_11(self):
        aap_i = AquetiAdminPageIssue(self.driver)
        self.navigate_to(aap_i.page_url)

        aap_sc = aap_i.submit_issue("title", "summary", "description")

        self.assertEqual(aap_sc.page_url, aap_sc.cur_page_url)
    
    @unittest.SkipTest
    def test_12(self):
        aap_cc = AquetiAdminPageConfigurationCamera(self.driver)
        self.navigate_to(aap_cc.page_url)

        aap_cc._(aap_cc.auto_gain)
        aap_cc._(aap_cc.auto_whitebalance)
        aap_cc._(aap_cc.auto_shutter)

        aap_cc._(aap_cc.gain_plus)
        aap_cc._(aap_cc.whitebalance_plus)
        aap_cc._(aap_cc.shutter_plus)

        aap_cc._(aap_cc.gain_minus)
        aap_cc._(aap_cc.whitebalance_minus)
        aap_cc._(aap_cc.shutter_minus)

        aap_cc.move_sharpening_slider(20)
        aap_cc.move_denoising_slider(40)

        aap_cc._(aap_cc.night_mode_chkb)
        aap_cc._(aap_cc.transport_mode_dd, "10 bit")
        aap_cc._(aap_cc.framerate_dd, "30 fps")
    
    @unittest.SkipTest
    def test_sc_move(self):
        aap_cc = AquetiAdminPageConfigurationCameraImage(self)
        self.navigate_to(aap_cc.page_url)

        aap_cc.click_links()

        aap_cc = AquetiAdminPageConfigurationCameraImage(self)
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
        aap_cc = AquetiAdminPageConfigurationCameraImage(self)
        self.navigate_to(aap_cc.page_url)

        aap_cc.click_links()

        aap_cc = AquetiAdminPageConfigurationCameraImage(self)
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
    #unittest.main()

    suite = unittest.TestLoader().loadTestsFromTestCase(APITest)
    unittest.TextTestRunner().run(suite)
