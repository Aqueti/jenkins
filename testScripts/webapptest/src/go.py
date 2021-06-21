import math
import random
import re
import subprocess
import json
import datetime as dt
import os
import ctypes
import time

from datetime import datetime, timedelta
from src.decorators import *

try:
    import AQT
except ImportError:
    print('no AQT lib found')
    exit(1)


class GO2:
    api = None

    vs = None
    ts = None
    iss = None
    ps = None
    sp = None

    stream = None

    frame = None

    cur_cam = None

    path = os.path.expanduser("~")

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

    @async_
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

class GO:
    cams = None
    renderers = None

    api = None
    cam = None

    def __init__(self, *args, **kwargs):
        self.sys_name = args[0]
        self.cam_name = args[1]

        if self.api == None: # or self.api.GetStatus() != 0
            self.recreate()

        self.__call__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        self.cams = self.api.GetAvailableCameras()
        self.renderers = self.api.GetAvailableRenderers()

    def recreate(self):
        self.api = AQT.AquetiAPI("test_api", AQT.U8Vector(), AQT.StringVector(["aqt://{}".format(self.sys_name)]))
        self.cam = AQT.Camera(self.api, self.cam_name)

    def get_stream_info(self, r_index=0, s_index=0):
        if self.renderers is not None:
            renderer_info = json.loads(self.api.GetDetailedStatus(self.renderers[r_index].Name()))

            if len(renderer_info["render_streams"]) > s_index:
                stream_info = json.loads(self.api.GetDetailedStatus("/aqt/render/" + renderer_info["id"] + '/' + renderer_info["render_streams"][s_index]))

                return stream_info

    def get_renderer_info(self, r_index=0):
        if self.renderers is not None:
            renderer_info = json.loads(self.api.GetDetailedStatus(self.renderers[r_index].Name()))

            return renderer_info

    def get_cam_info(self, cam):
        if "/aqt/camera/" not in cam:
            cam = "/aqt/camera/{}".format(cam)

        try:
            cam_info = json.loads(self.api.GetDetailedStatus(str(cam)))
        except:
            cam_info = {}

        return cam_info

    def get_params(self, cam_name):
        ret = json.loads(self.api.GetParameters(cam_name))

        return ret

    def set_params(self, cam_name, d):
        ret = self.api.SetParameters(cam_name, d)

        return ret


    def get_mcam_status(self, cam):
        status = {}
        for mcam in cam.sensors:
            status[mcam] = json.loads(self.api.GetDetailedStatus("/aqt/camera/" + cam.cam_id + "/" + mcam))

        return status

    def get_mcam_params(self, cam):
        params = {}
        for mcam in cam.sensors:
            try:
                params[mcam] = json.loads(self.api.GetParameters("/aqt/camera/" + cam.cam_id + "/" + mcam))
            except:
                params[mcam] = {}

        return params

    def set_mcam_status(self, cam, d):
        status = {}
        for mcam in cam.sensors:
            status[mcam] = self.api.SetDetailedStatus("/aqt/camera/" + cam.cam_id + "/" + mcam, d)

        return status

    def set_mcam_params(self, cam, d):
        params = {}
        for mcam in cam.sensors:
            params[mcam] = self.api.SetParameters("/aqt/camera/" + cam.cam_id + "/" + mcam, d)

        return params

    def is_connected(self, *args, **kwargs):
        if "cam" in kwargs:
            params = self.get_cam_info(kwargs["cam"])

            if params == {}:
                return False
            else:
                for k, v in params["mcam_state"].items():
                    if v != "CONNECTED":
                        return False

                return True