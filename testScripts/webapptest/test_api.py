from datetime import datetime, timedelta
import unittest
import time
import json
import AQT


class APITest(unittest.TestCase):
    api = AQT.AquetiAPI()

    vs = AQT.ViewState(api)
    ts = AQT.TimeState(api)
    iss = AQT.ImageSubsetState(api)
    ps = AQT.PoseState(api)
    sp = AQT.StreamProperties()
    rapi = AQT.RenderStream(api, vs, ts, iss, ps, sp)

    def isStatusOK(self, api):
        if api.GetStatus() != AQT.aqt_STATUS_OKAY:
            self.fail()

    @unittest.SkipTest
    def test_stream_types(self):
        self.sp.Width(1920)
        self.sp.Height(1080)
        self.sp.FrameRate(30)

        cams = self.api.GetAvailableCameras()

        self.isStatusOK(self.rapi)

        self.rapi.AddCamera(cams[0].Name())

        self.isStatusOK(self.rapi)

        self.rapi.SetStreamingState(True)

        self.isStatusOK(self.rapi)

        self.ts.PlaySpeed(1.0)

        self.isStatusOK(self.rapi)

        aqt_types = [AQT.aqt_STREAM_TYPE_JPEG, AQT.aqt_STREAM_TYPE_H264, AQT.aqt_STREAM_TYPE_H265]

        for aqt_type in aqt_types:
            self.sp.Type(aqt_type)

            for i in range(60):
                time.sleep(1 / 60)

                frame = self.rapi.GetNextFrame()
                status = self.rapi.GetStatus()

                if status == AQT.aqt_STATUS_OKAY:
                    if frame.Type() == AQT.aqt_JPEG_IMAGE:
                        self.assertEqual(aqt_type, AQT.aqt_STREAM_TYPE_JPEG)
                    elif frame.Type() in (AQT.aqt_H264_P_FRAME, AQT.aqt_H264_I_FRAME):
                        self.assertIn(aqt_type, [AQT.aqt_H264_P_FRAME, AQT.aqt_H264_I_FRAME])
                    elif frame.Type() in (AQT.aqt_H265_P_FRAME, AQT.aqt_H265_I_FRAME):
                        self.assertIn(aqt_type, [AQT.aqt_H265_P_FRAME, AQT.aqt_H265_I_FRAME])

    @unittest.SkipTest
    def test_status(self):
        cams = self.api.GetAvailableCameras()

        self.isStatusOK(self.api)

        cam = AQT.Camera(self.api, cams[0].Name())

        self.isStatusOK(self.api)

        canStream = cam.GetCanStreamLiveNow()

        self.isStatusOK(self.api)

        cam.Recording(True)

        self.isStatusOK(self.api)

        intervals = cam.GetStoredDataRanges()

        self.isStatusOK(self.api)

        modes = cam.GetStreamingModes()

        self.isStatusOK(self.api)

        modes = cam.Parameters()

        # self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_001(self):
        name = "test"
        credentials = "credentials"
        urls = AQT.StringVector(["http://localhost", "https://localhost"])
        api = AQT.AquetiAPI(name, credentials, urls)

        self.isStatusOK(api)

        stores = api.GetAvailableStorage()
        for store in stores:
            sapi = AQT.Storage(api, store.Name())
            print("store " + store.Name())

        rends = api.GetAvailableRenderers()
        for rend in rends:
            rapi = AQT.RenderStream(api, self.vs, self.ts, self.iss, self.ps, self.sp, rend.Name())
            print("rends " + rend.Name())

    @unittest.SkipTest
    def test_api_getavailablecameras(self):
        cams = self.api.GetAvailableCameras()

        self.isStatusOK(self.api)

        self.assertEqual(len(cams), 2)

    @unittest.SkipTest
    def test_api_getavailablerenderers(self):
        renderers = self.api.GetAvailableRenderers()

        self.isStatusOK(self.api)

        self.assertEqual(len(renderers), 2)

    @unittest.SkipTest
    def test_api_getavailablestorage(self):
        storages = self.api.GetAvailableStorage()

        self.isStatusOK(self.api)

        self.assertEqual(len(storages), 2)

    @unittest.SkipTest
    def test_api_getdetailedstatus(self):
        info = json.loads(self.api.GetDetailedStatus("/aqt/render/" + ""))  # id

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_api_getcurrentsystemtime(self):
        cur_time = self.api.GetCurrentSystemTime()

        self.isStatusOK(self.api)

        self.assertAlmostEqual((cur_time.tv_sec + cur_time.tv_usec * 1e-6), time.time(), 3)

        # dt = datetime(1970, 1, 1) + timedelta(microseconds=(time.tv_sec * 1e6 + time.tv_usec))

    @unittest.SkipTest
    def test_api_getparameters(self):
        self.api.GetParameters("entityName")

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_api_setparameters(self):
        self.api.SetParameters("entityName", "{}")

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_api_createissuereport(self):
        self.api.CreateIssueReport("test.txt", "summary", "description")

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_api_externalntpservername(self):
        name = self.api.ExternalNTPServerName()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_api_userdata(self):
        self.api.UserData("id", "test")

        self.isStatusOK(self.api)

        udata = self.api.UserData("id")

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_vs_pandegrees(self):
        self.vs.PanDegrees()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_vs_minpandegrees(self):
        self.vs.MinPanDegrees()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_vs_maxpandegrees(self):
        self.vs.MaxPanDegrees()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_vs_panspeeddegrees(self):
        self.vs.PanSpeedDegrees()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_vs_tiltdegrees(self):
        self.vs.TiltDegrees()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_vs_mintiltdegrees(self):
        self.vs.MinTiltDegrees()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_vs_maxtiltdegrees(self):
        self.vs.MaxTiltDegrees()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_vs_tiltspeeddegrees(self):
        self.vs.TiltSpeedDegrees()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_vs_zoom(self):
        self.vs.Zoom()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_vs_minzoom(self):
        self.vs.MinZoom()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_vs_maxzoom(self):
        self.vs.MaxZoom()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_vs_zoomspeed(self):
        self.vs.ZoomSpeed()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_vs_horizontalfovdegrees(self):
        self.vs.HorizontalFOVDegrees()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_vs_verticalfovdegrees(self):
        self.vs.VerticalFOVDegrees()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_ts_playspeed(self):
        self.ts.PlaySpeed()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_ts_time(self):
        self.ts.Time()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_iss_minx(self):
        self.iss.MinX()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_iss_maxx(self):
        self.iss.MaxX()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_iss_miny(self):
        self.iss.MinY()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_iss_maxy(self):
        self.iss.MaxY()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_ps_altitude(self):
        self.ps.Altitude()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_ps_latitude(self):
        self.ps.Latitude()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_ps_longitude(self):
        self.ps.Longitude()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_ps_pitch(self):
        self.ps.Pitch()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_ps_roll(self):
        self.ps.Roll()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_ps_roll(self):
        self.ps.Yaw()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_sp_canskip(self):
        self.sp.CanSkip()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_sp_display(self):
        self.sp.Display()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_sp_framerate(self):
        self.sp.FrameRate()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_sp_fullscreen(self):
        self.sp.FullScreen()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_sp_height(self):
        self.sp.Height()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_sp_width(self):
        self.sp.Width()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_sp_idrinterval(self):
        self.sp.IDRInterval()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_sp_quality(self):
        self.sp.Quality()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_sp_type(self):
        self.sp.Type()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_sp_windowx(self):
        self.sp.WindowX()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_sp_windowy(self):
        self.sp.WindowY()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_rapi_addcamera(self):
        self.rapi.AddCamera("cam")

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_rapi_boolparameter(self):
        self.rapi.BoolParameter()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_rapi_floatparameter(self):
        self.rapi.FloatParameter()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_rapi_getfloatparameterrange(self):
        self.rapi.GetFloatParameterRange()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_rapi_getnextframe(self):
        self.rapi.GetNextFrame()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_rapi_removecamera(self):
        self.rapi.RemoveCamera("")

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_rapi_setstreamingstate(self):
        self.rapi.SetStreamingState()

        self.isStatusOK(self.api)

    @unittest.SkipTest
    def test_003(self):
        self.rapi.SetStreamingState(True)

        cnt = 0
        while cnt <= 100:
            frame = self.rapi.GetNextFrame()
            if self.rapi.GetStatus() == AQT.aqt_STATUS_OKAY:
                cnt += 1
                if frame.Type() == AQT.aqt_H264_I_FRAME:
                    print('Received H264 I Frame')
                elif frame.Type() == AQT.aqt_H264_P_FRAME:
                    print('Received H264 P Frame')
                else:
                    print('Unexpected image type: ' + frame.Type())
                    self.fail()


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(APITest)
    unittest.TextTestRunner().run(suite)
