from datetime import datetime, timedelta
import pytest
import random
import time
import json
import os
import AQT


class NAPI:
    api = AQT.AquetiAPI()

    vs = AQT.ViewState(api)
    ts = AQT.TimeState(api)
    iss = AQT.ImageSubsetState(api)
    ps = AQT.PoseState(api)
    sp = AQT.StreamProperties()

    rapi = None

    frame = None

    cur_cam = None

    def get_next_frame(self):
        if self.frame is not None:
            self.frame.ReleaseData()

        while True:
            self.frame = self.rapi.GetNextFrame()

            if self.rapi.GetStatus() == AQT.aqt_STATUS_OKAY:
                break

    def set_resolution(self, tp="1080p"):
        if tp == "4k":
            self.sp.Width(3840)
            self.sp.Height(2160)
        elif tp == "1080p":
            self.sp.Width(1920)
            self.sp.Height(1080)
        elif tp == "720p":
            self.sp.Width(1280)
            self.sp.Height(720)
        elif tp == "480p":
            self.sp.Width(854)
            self.sp.Height(480)

    def start_stream(self):
        self.sp.FrameRate(30)
        self.sp.CanSkip(True)
        self.sp.Quality(0.8)
        self.sp.IDRInterval(30)
        self.sp.WindowX()
        self.sp.WindowY()
        self.sp.FullScreen(True)
        self.sp.Display(0)

        self.rapi = AQT.RenderStream(self.api, self.vs, self.ts, self.iss, self.ps, self.sp)

        cams = self.api.GetAvailableCameras()
        self.cur_cam = cams[0]
        self.rapi.AddCamera(self.cam.Name())
        self.rapi.SetStreamingState(True)
        self.ts.PlaySpeed(1.0)

        self.get_next_frame()

    def get_cur_time(self, is_in_ms=False):
        cur_time = self.api.GetCurrentSystemTime()

        if is_in_ms:
            return cur_time.tv_sec * pow(10, 6) + cur_time.tv_usec
        else:
            return datetime(1970, 1, 1) + timedelta(microseconds=(cur_time.tv_sec * pow(10, 6) + cur_time.tv_usec))

    def set_vs(self, control):
        if control == 'zoom_in':
            self.vs.ZoomSpeed(3 / 2)
        elif control == 'zoom_out':
            self.vs.ZoomSpeed(2 / 3)
        elif control == 'stop_zoom':
            self.vs.ZoomSpeed(1)
        elif control == 'move_left':
            self.vs.PanSpeedDegrees(5)
        elif control == 'move_right':
            self.vs.PanSpeedDegrees(-5)
        elif control == 'move_down':
            self.vs.TiltSpeedDegrees(5)
        elif control == 'move_up':
            self.vs.TiltSpeedDegrees(-5)
        elif control == 'move_stop':
            self.vs.TiltSpeedDegrees(0)
            self.vs.PanSpeedDegrees(0)

    def change_cam(self, cam_name):
        self.rapi.RemoveCamera(self.cam.Name())
        self.rapi.AddCamera(cam_name)

    def toggle_win_mode(self):
        if self.sp.Type() == AQT.aqt_JPEG_IMAGE:
            self.sp.Type(AQT.aqt_STREAM_TYPE_LOCALDISPLAY)
        elif self.sp.Type() == AQT.aqt_STREAM_TYPE_LOCALDISPLAY:
            self.sp.Type(AQT.aqt_JPEG_IMAGE)


class TestAPI:
    napi = NAPI()

    def setup(self):
        pass

    def teardown(self):
        pass

    def is_api_status_ok(self):
        if self.napi.api.GetStatus() != AQT.aqt_STATUS_OKAY:
            self.fail()

    @pytest.mark.skip(reason="")
    def test_stream_types(self):
        aqt_types = [AQT.aqt_STREAM_TYPE_JPEG, AQT.aqt_STREAM_TYPE_H264, AQT.aqt_STREAM_TYPE_H265]

        for aqt_type in aqt_types:
            self.napi.sp.Type(aqt_type)
            self.napi.start_stream()

            for i in range(10):
                self.napi.get_next_frame()

                if self.napi.frame.Type() == AQT.aqt_JPEG_IMAGE:
                    assert aqt_type == AQT.aqt_STREAM_TYPE_JPEG
                elif self.napi.frame.Type() in (AQT.aqt_H264_P_FRAME, AQT.aqt_H264_I_FRAME):
                    assert aqt_type == AQT.aqt_STREAM_TYPE_H264
                elif self.napi.frame.Type() in (AQT.aqt_H265_P_FRAME, AQT.aqt_H265_I_FRAME):
                    assert aqt_type == AQT.aqt_STREAM_TYPE_H265
                else:
                    self.fail()

    @pytest.mark.skip(reason="")
    def test_stream_resolutions(self):
        aqt_res = ["4k", "1080p", "720p", "480p"]

        for res in aqt_res:
            self.napi.set_resolution(res)
            self.napi.start_stream()

            for i in range(10):
                self.napi.get_next_frame()

                if res == "4k":
                    assert self.napi.frame.Width() == 3840
                    assert self.napi.frame.Height() == 2160
                elif res == "1080p":
                    assert self.napi.frame.Width() == 1920
                    assert self.napi.frame.Height() == 1080
                elif res == "720p":
                    assert self.napi.frame.Width() == 1280
                    assert self.napi.frame.Height() == 720
                else:
                    assert self.napi.frame.Width() == 854
                    assert self.napi.frame.Height() == 480

    @pytest.mark.skip(reason="")
    def test_status(self):
        cams = self.napi.api.GetAvailableCameras()

        self.is_api_status_ok()

        cam = AQT.Camera(self.napi.api, cams[0].Name())

        self.is_api_status_ok()

        canStream = cam.GetCanStreamLiveNow()

        self.is_api_status_ok()

        cam.Recording(True)

        self.is_api_status_ok()

        intervals = cam.GetStoredDataRanges()

        self.is_api_status_ok()

        modes = cam.GetStreamingModes()

        self.is_api_status_ok()

        modes = cam.Parameters()

        # self.is_status_ok(self.api)

    @pytest.mark.skip(reason="")
    def test_001(self):
        name = "test"
        credentials = "credentials"
        urls = AQT.StringVector(["http://localhost", "https://localhost"])
        api = AQT.AquetiAPI(name, credentials, urls)

        self.is_status_ok(api)

        stores = api.GetAvailableStorage()
        for store in stores:
            print("store " + store.Name())

        rends = api.GetAvailableRenderers()
        for rend in rends:
            print("rends " + rend.Name())

    @pytest.mark.skip(reason="")
    def test_api_getavailablecameras(self):
        cams = self.napi.api.GetAvailableCameras()

        self.is_api_status_ok()

        self.assertEqual(len(cams), 2)

    @pytest.mark.skip(reason="")
    def test_api_getavailablerenderers(self):
        renderers = self.napi.api.GetAvailableRenderers()

        self.is_api_status_ok()

        self.assertEqual(len(renderers), 2)

    @pytest.mark.skip(reason="")
    def test_api_getavailablestorage(self):
        storages = self.napi.api.GetAvailableStorage()

        self.is_api_status_ok()

        self.assertEqual(len(storages), 2)

    @pytest.mark.skip(reason="")
    def test_api_getdetailedstatus(self):
        info = json.loads(self.napi.api.GetDetailedStatus("/aqt/render/" + ""))  # id

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_api_getcurrentsystemtime(self):
        cur_time = self.napi.api.GetCurrentSystemTime()

        self.is_api_status_ok()

        self.assertAlmostEqual((cur_time.tv_sec + cur_time.tv_usec * 1e-6), time.time(), 3)

    @pytest.mark.skip(reason="")
    def test_api_getparameters(self):
        self.napi.api.GetParameters("entityName")

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_api_setparameters(self):
        self.napi.api.SetParameters("entityName", "{}")

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_api_createissuereport(self):
        self.napi.api.CreateIssueReport("test.txt", "summary", "description")

        self.is_api_status_ok()

        self.assertTrue(os.path.exists("test.txt"))

    @pytest.mark.skip(reason="")
    def test_api_externalntpservername(self):
        name = self.napi.api.ExternalNTPServerName()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_api_userdata(self):
        sid = ""
        data = ""

        self.napi.api.UserData(sid, data)

        self.is_api_status_ok()

        udata = self.napi.api.UserData(sid)

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_vs_pandegrees(self):
        self.napi.vs.PanDegrees()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_vs_minpandegrees(self):
        self.napi.vs.MinPanDegrees()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_vs_maxpandegrees(self):
        self.napi.vs.MaxPanDegrees()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_vs_panspeeddegrees(self):
        self.napi.vs.PanSpeedDegrees()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_vs_tiltdegrees(self):
        self.napi.vs.TiltDegrees()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_vs_mintiltdegrees(self):
        self.napi.vs.MinTiltDegrees()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_vs_maxtiltdegrees(self):
        self.napi.vs.MaxTiltDegrees()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_vs_tiltspeeddegrees(self):
        self.napi.vs.TiltSpeedDegrees()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_vs_zoom(self):
        self.napi.start_stream()

        self.napi.vs.Zoom(0.5)  # random.uniform(0, 1)

        self.is_api_status_ok()

        assert self.napi.frame.Zoom() == self.napi.vs.Zoom()

    @pytest.mark.skip(reason="")
    def test_vs_minzoom(self):
        self.napi.vs.MinZoom()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_vs_maxzoom(self):
        self.napi.vs.MaxZoom()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_vs_zoomspeed(self):
        self.napi.vs.ZoomSpeed()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_vs_horizontalfovdegrees(self):
        self.napi.vs.HorizontalFOVDegrees()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_vs_verticalfovdegrees(self):
        self.napi.vs.VerticalFOVDegrees()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_ts_playspeed(self):
        self.napi.ts.PlaySpeed()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_ts_time(self):
        self.napi.ts.Time()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_iss_minx(self):
        self.napi.iss.MinX()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_iss_maxx(self):
        self.napi.iss.MaxX()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_iss_miny(self):
        self.napi.iss.MinY()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_iss_maxy(self):
        self.napi.iss.MaxY()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_ps_altitude(self):
        self.napi.ps.Altitude()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_ps_latitude(self):
        self.napi.ps.Latitude()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_ps_longitude(self):
        self.napi.ps.Longitude()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_ps_pitch(self):
        self.napi.ps.Pitch()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_ps_roll(self):
        self.napi.ps.Roll()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_ps_roll(self):
        self.napi.ps.Yaw()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_sp_canskip(self):
        self.napi.sp.CanSkip()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_sp_display(self):
        self.napi.sp.Display()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_sp_framerate(self):
        self.napi.sp.FrameRate()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_sp_fullscreen(self):
        self.napi.sp.FullScreen(False)

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_sp_height(self):
        self.napi.sp.Height(random.randint(0, 10e4))

        self.is_api_status_ok()

        self.napi.start_stream()

        assert self.napi.frame.Height() == self.napi.sp.Height()

    @pytest.mark.skip(reason="")
    def test_sp_width(self):
        self.napi.sp.Width(random.randint(0, 10e4))

        self.is_api_status_ok()

        self.napi.start_stream()

        assert self.napi.frame.Width() == self.napi.sp.Width()

    @pytest.mark.skip(reason="")
    def test_sp_idrinterval(self):
        self.napi.sp.IDRInterval()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_sp_quality(self):
        self.napi.sp.Quality()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_sp_type(self):
        self.napi.sp.Type()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_sp_windowx(self):
        self.napi.sp.WindowX()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_sp_windowy(self):
        self.napi.sp.WindowY()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_rapi_addcamera(self):
        self.napi.rapi.AddCamera("cam")

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_rapi_boolparameter(self):
        self.napi.rapi.BoolParameter()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_rapi_floatparameter(self):
        self.napi.rapi.FloatParameter()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_rapi_getfloatparameterrange(self):
        self.napi.rapi.GetFloatParameterRange()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_rapi_getnextframe(self):
        self.napi.rapi.GetNextFrame()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_rapi_removecamera(self):
        self.napi.rapi.RemoveCamera("")

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_rapi_setstreamingstate(self):
        self.napi.rapi.SetStreamingState()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_rapi_setstreamcallback(self):
        self.napi.rapi.SetStreamCallback()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_rapi_softwareupdate(self):
        sid = ""
        data = ""
        checksum = ""

        update = AQT.Update(self.napi.api, sid)
        update.Install(data, checksum)

        self.is_api_status_ok()