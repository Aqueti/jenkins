import unittest
from BaseTest import BaseTest
from AquetiAdminPage import *


class Test(BaseTest):
    browser = "chrome"

    def test_0(self):
        aap_sc = AquetiAdminPageStatusCamera(self.driver)
        self.navigate_to(aap_sc.page_url)
        comps = aap_sc.components

        self.assertEqual(len(comps), 2)

        for comp in comps:
            self.assertIn("aqt:Camera:", comp.text)

        comps[0].click()

        self.assertEqual(aap_sc.prop_status.text, "online")
        self.assertEqual(aap_sc.prop_recording.text, "false")
        self.assertEqual(aap_sc.prop_serial.text, "undefined")
        self.assertEqual(aap_sc.prop_software.text, "undefined")
        self.assertEqual(aap_sc.prop_kernel.text, "undefined")
        self.assertEqual(aap_sc.prop_host.text, "undefined")

        self.assertEqual(aap_sc.prop_sensor_module.text, "imx274")
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
        self.assertEqual(aap_ss.prop_serial.text, "aqt:Storage:1")
        self.assertEqual(aap_ss.prop_software.text, "undefined")
        self.assertEqual(aap_ss.prop_kernel.text, "undefined")
        self.assertEqual(aap_ss.prop_host.text, "undefined")

    @unittest.SkipTest
    def test_2(self):
        aap_sr = AquetiAdminPageStatusRender(self.driver)
        self.navigate_to(aap_sr.page_url)
        comps = aap_sr.components

        self.assertIsNone(comps)

        self.assertEqual(aap_sr.prop_serial.text, "")
        self.assertEqual(aap_sr.prop_software.text, "undefined")
        self.assertEqual(aap_sr.prop_kernel.text, "undefined")
        self.assertEqual(aap_sr.prop_host.text, "undefined")


if __name__ == "__main__":
    unittest.main()
