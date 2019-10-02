import AQT
import ctypes
import datetime as dt
import json
import os
import random
import time
from datetime import datetime, timedelta

import pytest
from src.BaseEnv import *
from src.BaseTest import BaseTest

from src.decorators import *


class GO:
    api = None

    vs = None
    ts = None
    iss = None
    ps = None
    sp = None

    stream = None

    frame = None

    cur_cam = None

    path = '/home/astepenko/ipics/'

    def __init__(self):
        self.api = AQT.AquetiAPI("", AQT.U8Vector(), AQT.StringVector(["aqt://Camera2"]))

        self.vs = AQT.ViewState(self.api)
        self.ts = AQT.TimeState(self.api)
        self.iss = AQT.ImageSubsetState(self.api)
        self.ps = AQT.PoseState(self.api)
        self.sp = AQT.StreamProperties()

    def get_detailed_status(self, s):
        return json.loads(self.api.GetDetailedStatus(s))

    def get_next_frame(self):
        if self.frame is not None:
            self.frame.ReleaseData()

        while True:
            self.frame = self.stream.GetNextFrame()

            if self.stream.GetStatus() == AQT.aqt_STATUS_OKAY:
                break

    @async
    def get_frames(self, delay=0.03):
        while True:
            self.get_next_frame()

        time.sleep(delay)

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

    def create_stream(self):
        self.sp.FrameRate(30)
        self.sp.CanSkip(True)
        self.sp.Quality(0.8)
        self.sp.IDRInterval(30)
        self.sp.WindowX()
        self.sp.WindowY()
        self.sp.FullScreen(True)
        self.sp.Display(0)

        self.stream = AQT.RenderStream(self.api, self.vs, self.ts, self.iss, self.ps, self.sp)

    def start_stream(self, c_cam=None):
        self.create_stream()

        if c_cam is None:
            cams = self.api.GetAvailableCameras()
            self.c_cam = cams[0].Name()
        else:
            self.c_cam = c_cam

        self.stream.AddCamera(self.c_cam)
        self.stream.SetStreamingState(True)
        self.ts.PlaySpeed(1.0)

        self.get_next_frame()

        time.sleep(1)

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
        self.api.RemoveCamera(self.cam.Name())
        self.api.AddCamera(cam_name)

    def toggle_win_mode(self):
        if self.sp.Type() == AQT.aqt_JPEG_IMAGE:
            self.sp.Type(AQT.aqt_STREAM_TYPE_LOCALDISPLAY)
        elif self.sp.Type() == AQT.aqt_STREAM_TYPE_LOCALDISPLAY:
            self.sp.Type(AQT.aqt_JPEG_IMAGE)

    def save_frame(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)

        if self.frame.Data() is not None:
            print(self.frame.Data())
            carr = ctypes.cast(int(self.frame.Data()), ctypes.POINTER(ctypes.c_char * self.frame.Size()))[0]
            arr = bytearray(carr)

            with open(self.path + 'img_' + dt.datetime.now().strftime('%m-%d%-y_%H-%M-%S') + '.jpeg', 'wb') as file:
                file.write(arr)


class Test_API(BaseTest):
    browser = None

    go = None

    def setup_method(self):
        self.go = GO()

    def teardown_method(self):
        pass

    def is_api_status_ok(self):
        if self.go.api.GetStatus() != AQT.aqt_STATUS_OKAY:
            self.fail()


    def get_rx(self, ni, delay=1):
        cmd = 'cat /sys/class/net/' + ni + '/statistics/rx_bytes'
        s_rx = int(self.exec_cmd(cmd))

        time.sleep(delay)

        e_rx = int(self.exec_cmd(cmd))

        return (e_rx - s_rx) * 8 / (1e6 * delay)

    @pytest.mark.skip(reason="")
    def test_stream_types(self):
        aqt_types = [AQT.aqt_STREAM_TYPE_JPEG, AQT.aqt_STREAM_TYPE_H264, AQT.aqt_STREAM_TYPE_H265]

        for aqt_type in aqt_types:
            self.go.sp.Type(aqt_type)
            self.go.start_stream()

            for i in range(10):
                self.go.get_next_frame()

                if self.go.frame.Type() == AQT.aqt_JPEG_IMAGE:
                    assert aqt_type == AQT.aqt_STREAM_TYPE_JPEG
                elif self.go.frame.Type() in (AQT.aqt_H264_P_FRAME, AQT.aqt_H264_I_FRAME):
                    assert aqt_type == AQT.aqt_STREAM_TYPE_H264
                elif self.go.frame.Type() in (AQT.aqt_H265_P_FRAME, AQT.aqt_H265_I_FRAME):
                    assert aqt_type == AQT.aqt_STREAM_TYPE_H265
                else:
                    self.fail()

    @pytest.mark.skip(reason="")
    def test_stream_resolutions(self):
        aqt_res = ["4k", "1080p", "720p", "480p"]

        for res in aqt_res:
            self.go.set_resolution(res)
            self.go.start_stream()

            for i in range(10):
                self.go.get_next_frame()

                if res == "4k":
                    assert self.go.frame.Width() == 3840
                    assert self.go.frame.Height() == 2160
                elif res == "1080p":
                    assert self.go.frame.Width() == 1920
                    assert self.go.frame.Height() == 1080
                elif res == "720p":
                    assert self.go.frame.Width() == 1280
                    assert self.go.frame.Height() == 720
                else:
                    assert self.go.frame.Width() == 854
                    assert self.go.frame.Height() == 480

    @pytest.mark.skip(reason="")
    def test_status(self):
        cams = self.go.api.GetAvailableCameras()

        self.is_api_status_ok()

        cam = AQT.Camera(self.go.api, cams[0].Name())

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
        cams = self.go.api.GetAvailableCameras()

        self.is_api_status_ok()

        self.assertEqual(len(cams), 2)

    @pytest.mark.skip(reason="")
    def test_api_getavailablerenderers(self):
        renderers = self.go.api.GetAvailableRenderers()

        self.is_api_status_ok()

        self.assertEqual(len(renderers), 2)

    @pytest.mark.skip(reason="")
    def test_api_getavailablestorage(self):
        storages = self.go.api.GetAvailableStorage()

        self.is_api_status_ok()

        self.assertEqual(len(storages), 2)

    @pytest.mark.skip(reason="")
    def test_api_getdetailedstatus(self):
        info = json.loads(self.go.api.GetDetailedStatus("/aqt/render/" + ""))  # id

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_api_getcurrentsystemtime(self):
        cur_time = self.go.api.GetCurrentSystemTime()

        self.is_api_status_ok()

        self.assertAlmostEqual((cur_time.tv_sec + cur_time.tv_usec * 1e-6), time.time(), 3)

    @pytest.mark.skip(reason="")
    def test_api_getparameters(self):
        self.go.api.GetParameters("entityName")

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_api_setparameters(self):
        self.go.api.SetParameters("entityName", "{}")

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_api_createissuereport(self):
        self.go.api.CreateIssueReport("test.txt", "summary", "description")

        self.is_api_status_ok()

        self.assertTrue(os.path.exists("test.txt"))

    @pytest.mark.skip(reason="")
    def test_api_externalntpservername(self):
        name = self.go.api.ExternalNTPServerName()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_api_userdata(self):
        sid = ""
        data = ""

        self.go.api.UserData(sid, data)

        self.is_api_status_ok()

        udata = self.go.api.UserData(sid)

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_vs_pandegrees(self):
        self.go.vs.PanDegrees()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_vs_minpandegrees(self):
        self.go.vs.MinPanDegrees()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_vs_maxpandegrees(self):
        self.go.vs.MaxPanDegrees()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_vs_panspeeddegrees(self):
        self.go.vs.PanSpeedDegrees()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_vs_tiltdegrees(self):
        self.go.vs.TiltDegrees()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_vs_mintiltdegrees(self):
        self.go.vs.MinTiltDegrees()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_vs_maxtiltdegrees(self):
        self.go.vs.MaxTiltDegrees()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_vs_tiltspeeddegrees(self):
        self.go.vs.TiltSpeedDegrees()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_vs_zoom(self):
        self.go.start_stream()

        self.go.vs.Zoom(0.5)  # random.uniform(0, 1)

        self.is_api_status_ok()

        assert self.go.frame.Zoom() == self.go.vs.Zoom()

    @pytest.mark.skip(reason="")
    def test_vs_minzoom(self):
        self.go.vs.MinZoom()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_vs_maxzoom(self):
        self.go.vs.MaxZoom()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_vs_zoomspeed(self):
        self.go.vs.ZoomSpeed()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_vs_horizontalfovdegrees(self):
        self.go.vs.HorizontalFOVDegrees()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_vs_verticalfovdegrees(self):
        self.go.vs.VerticalFOVDegrees()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_ts_playspeed(self):
        self.go.ts.PlaySpeed()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_ts_time(self):
        self.go.ts.Time()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_iss_minx(self):
        self.go.iss.MinX()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_iss_maxx(self):
        self.go.iss.MaxX()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_iss_miny(self):
        self.go.iss.MinY()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_iss_maxy(self):
        self.go.iss.MaxY()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_ps_altitude(self):
        self.go.ps.Altitude()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_ps_latitude(self):
        self.go.ps.Latitude()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_ps_longitude(self):
        self.go.ps.Longitude()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_ps_pitch(self):
        self.go.ps.Pitch()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_ps_roll(self):
        self.go.ps.Roll()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_ps_roll(self):
        self.go.ps.Yaw()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_sp_canskip(self):
        self.go.sp.CanSkip()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_sp_display(self):
        self.go.sp.Display()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_sp_framerate(self):
        self.go.sp.FrameRate()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_sp_fullscreen(self):
        self.go.sp.FullScreen(False)

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_sp_height(self):
        self.go.sp.Height(random.randint(0, 10e4))

        self.is_api_status_ok()

        self.go.start_stream()

        assert self.go.frame.Height() == self.go.sp.Height()

    @pytest.mark.skip(reason="")
    def test_sp_width(self):
        self.go.sp.Width(random.randint(0, 10e4))

        self.is_api_status_ok()

        self.go.start_stream()

        assert self.go.frame.Width() == self.go.sp.Width()

    @pytest.mark.skip(reason="")
    def test_sp_idrinterval(self):
        self.go.sp.IDRInterval()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_sp_quality(self):
        self.go.sp.Quality()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_sp_type(self):
        self.go.sp.Type()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_sp_windowx(self):
        self.go.sp.WindowX()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_sp_windowy(self):
        self.go.sp.WindowY()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_api_addcamera(self):
        self.go.api.AddCamera("cam")

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_api_boolparameter(self):
        self.go.api.BoolParameter()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_api_floatparameter(self):
        self.go.api.FloatParameter()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_api_getfloatparameterrange(self):
        self.go.api.GetFloatParameterRange()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_api_getnextframe(self):
        self.go.api.GetNextFrame()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_api_removecamera(self):
        self.go.api.RemoveCamera("")

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_api_setstreamingstate(self):
        self.go.api.SetStreamingState()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_api_setstreamcallback(self):
        self.go.api.SetStreamCallback()

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_api_softwareupdate(self):
        sid = ""
        data = ""
        checksum = ""

        update = AQT.Update(self.go.api, sid)
        update.Install(data, checksum)

        self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_api_createissuereport(self):
        path = "/var/tmp/aqueti/test_"
        summary = "test"
        description = "test"

        for i in range(0, 10):
            self.go.api.CreateIssueReport(path + str(1) + '.txt', summary, description)

            self.is_api_status_ok()

    @pytest.mark.skip(reason="")
    def test_api_refresh(self):
        aqt_types = [AQT.aqt_STREAM_TYPE_H264, AQT.aqt_STREAM_TYPE_H265]

        for aqt_type in aqt_types:
            self.go.sp.Type(aqt_type)
            self.go.start_stream()

            is_i_frame_expected = False
            for i in range(10):
                if is_i_frame_expected:
                    is_i_frame_expected = not is_i_frame_expected
                    if aqt_types == AQT.aqt_STREAM_TYPE_H264:
                        assert self.go.frame.Type() == AQT.aqt_H264_I_FRAME
                    else:
                        assert self.go.frame.Type() == AQT.aqt_H265_I_FRAME

                self.go.get_next_frame()

                if self.go.frame.Type() in (AQT.aqt_H264_P_FRAME, AQT.aqt_H265_P_FRAME):
                    self.go.stream.Refresh()
                    is_i_frame_expected = not is_i_frame_expected
                    continue

    @pytest.mark.skip(reason="")
    def test_add_cam(self):
        env = Environment()

        self.go.create_stream()
        cams = self.go.api.GetAvailableCameras()

        #for i in range(5):
        #    self.go.stream.AddCamera(cams[0].Name())

        for cam in cams:
            self.go.stream.AddCamera(cam.Name())

        time.sleep(5)

        assert env.render.get_status() != ""

    @pytest.mark.skip(reason="")
    def test_remove_cam(self):
        self.go.create_stream()
        cams = self.go.api.GetAvailableCameras()
        renders = self.go.api.GetAvailableRenderers()

        for cam in cams:
            self.go.stream.AddCamera(cam.Name())

            c_cam = self.go.get_detailed_status(
                renders[0].Name() + "/" + self.go.get_detailed_status(renders[0].Name())['render_streams'][0])[
                'SCOP_list'][0]

            self.go.stream.RemoveCamera(cam.Name())

            assert cam.Name() == "/aqt/camera/" + c_cam


    @pytest.mark.skip(reason="")
    def test_remove_cam2(self):
        self.go.create_stream()
        cams = self.go.api.GetAvailableCameras()
        renders = self.go.api.GetAvailableRenderers()

        aqt_cam = None
        for cam in cams:
            if cam.Name() == '/aqt/camera/9':
                aqt_cam = AQT.Camera(self.go.api, cam.Name())

        #pprint.pprint(self.go.get_detailed_status(renders[0].Name()))

        ranges = aqt_cam.GetStoredDataRanges()

        for range in ranges:
            print(range.Start().tv_sec, range.End().tv_sec)


    #@pytest.mark.skip(reason="")
    def test_connection(self):
        #print(self.env.cam.get_status(tegra=1))
        #if self.env.cam.get_status(tegra=1) != "active":
        #    self.env.
        self.go.start_stream("/aqt/camera/201")
        self.go.get_frames()

        while True:
            # print(self.go.frame.Type())
            self.go.save_frame()
            time.sleep(1)



        speed = self.get_rx('enp4s0f0')
        print("speed: ", speed)
