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
            self.assertIn("aqt:Camera:", comp.get_attribute("innerText"))

        comps[0].click()

        self.assertEqual(aap_sc.prop_status.get_attribute('innerText'), "online")
        self.assertEqual(aap_sc.prop_recording.get_attribute('innerText'), "false")
        self.assertEqual(aap_sc.prop_serial.get_attribute('innerText'), "undefined")
        self.assertEqual(aap_sc.prop_software.get_attribute('innerText'), "undefined")
        self.assertEqual(aap_sc.prop_kernel.get_attribute('innerText'), "undefined")
        self.assertEqual(aap_sc.prop_host.get_attribute('innerText'), "undefined")

        self.assertEqual(aap_sc.prop_sensor_module.get_attribute('innerText'), "imx274")
        self.assertEqual(aap_sc.prop_sensor_host.get_attribute('innerText'), "87878")

    @unittest.SkipTest
    def test_1(self):
        aap_ss = AquetiAdminPageStatusStorage(self.driver)
        self.navigate_to(aap_ss.page_url)
        comps = aap_ss.components

        self.assertEqual(len(comps), 2)

        for comp in comps:
            self.assertIn("aqt:Storage:", comp.get_attribute("innerText"))

        comps[0].click()

        self.assertEqual(aap_ss.prop_status.get_attribute('innerText'), "online")
        self.assertEqual(aap_ss.prop_serial.get_attribute('innerText'), "aqt:Storage:1")
        self.assertEqual(aap_ss.prop_software.get_attribute('innerText'), "undefined")
        self.assertEqual(aap_ss.prop_kernel.get_attribute('innerText'), "undefined")
        self.assertEqual(aap_ss.prop_host.get_attribute('innerText'), "undefined")

    @unittest.SkipTest
    def test_2(self):
        aap_sr = AquetiAdminPageStatusRender(self.driver)
        self.navigate_to(aap_sr.page_url)
        comps = aap_sr.components

        self.assertIsNone(comps)

        self.assertEqual(aap_sr.prop_serial.get_attribute('innerText'), "")
        self.assertEqual(aap_sr.prop_software.get_attribute('innerText'), "undefined")
        self.assertEqual(aap_sr.prop_kernel.get_attribute('innerText'), "undefined")
        self.assertEqual(aap_sr.prop_host.get_attribute('innerText'), "undefined")


if __name__ == "__main__":
    unittest.main()
