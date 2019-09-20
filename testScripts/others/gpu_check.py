import AQT
import sys
import ctypes
import time
import datetime as dt

api = AQT.AquetiAPI("", AQT.U8Vector(), AQT.StringVector(['aqt://Camera7']))

cams = api.GetAvailableCameras()
cam = cams[0].Name()

timeControl = AQT.TimeState(api)
vs = AQT.ViewState(api)
iss = AQT.ImageSubsetState(api)
ps = AQT.PoseState(api)
sp = AQT.StreamProperties()

res = {"4k": (3840, 2160), "1080p": (1920, 1080), "720p": (1280, 720), "480p": (640, 480)}

#pairs (pairwise used)

arr = [
    (AQT.aqt_STREAM_TYPE_H265, 10, res["480p"]),
    (AQT.aqt_STREAM_TYPE_JPEG, 15, res["480p"]),
    (AQT.aqt_STREAM_TYPE_H264, 20, res["480p"]),
    (AQT.aqt_STREAM_TYPE_H264, 25, res["480p"]),
    (AQT.aqt_STREAM_TYPE_H264, 30, res["480p"]),    
    (AQT.aqt_STREAM_TYPE_H264, 5,  res["720p"]),
    (AQT.aqt_STREAM_TYPE_H264, 10, res["720p"]),    
    (AQT.aqt_STREAM_TYPE_H264, 15, res["720p"]),
    (AQT.aqt_STREAM_TYPE_JPEG, 20, res["720p"]),
    (AQT.aqt_STREAM_TYPE_H265, 25, res["720p"]),
    (AQT.aqt_STREAM_TYPE_H264, 30, res["720p"]),
    (AQT.aqt_STREAM_TYPE_H265, 5,  res["1080p"]),
    (AQT.aqt_STREAM_TYPE_JPEG, 10, res["1080p"]),
    (AQT.aqt_STREAM_TYPE_H264, 15, res["1080p"]),
    (AQT.aqt_STREAM_TYPE_H265, 20, res["1080p"]),
    (AQT.aqt_STREAM_TYPE_H264, 25, res["1080p"]),
    (AQT.aqt_STREAM_TYPE_JPEG, 30, res["1080p"]), 
    (AQT.aqt_STREAM_TYPE_JPEG, 5,  res["4k"]),
    (AQT.aqt_STREAM_TYPE_H264, 10, res["4k"]),
    (AQT.aqt_STREAM_TYPE_H265, 15, res["4k"]),
    (AQT.aqt_STREAM_TYPE_H264, 20, res["4k"]),
    (AQT.aqt_STREAM_TYPE_JPEG, 25, res["4k"]),
    (AQT.aqt_STREAM_TYPE_H265, 30, res["4k"])
]

result = {}
for sp_type, sp_fps, sp_res in arr:
    sp.Type(sp_type)
    sp.FrameRate(sp_fps)
    sp.Width(sp_res[0])
    sp.Height(sp_res[1])

    stream = AQT.RenderStream(api, vs, timeControl, iss, ps, sp)

    stream.AddCamera(cam)
    stream.SetStreamingState(True)
    time.sleep(1)

    v_arr = {"zoom": 0, "pan_d": 0, "tilt_d": 0, "hfov": 0, "vfov": 0}
    frame_cnt = 0
    s_time = int(dt.datetime.now().strftime("%s"))
    e_time = s_time
    while (e_time - s_time) < 300:    
        frame = stream.GetNextFrame()

        if stream.GetStatus() == AQT.aqt_STATUS_OKAY:
            e_time = int(dt.datetime.now().strftime("%s"))

            frame_cnt += 1

            frame.ReleaseData()

            vs.Zoom(v_arr["zoom"])
            vs.PanDegrees(v_arr["pan_d"])
            vs.TiltDegrees(v_arr["tilt_d"])
            vs.HorizontalFOVDegrees(v_arr["hfov"])
            vs.VerticalFOVDegrees(v_arr["vfov"])

            for k in v_arr.keys():
                v_arr[k] += 0.1

    result[(sp_type, sp_fps, sp_res)] = frame_cnt / (e_time - s_time)

    print('\ntype:{} fps:{} res:{} : {}\n'.format(sp_type, sp_fps, sp_res, result[(sp_type, sp_fps, sp_res)]))

    stream.SetStreamingState(False)
    stream.RemoveCamera(cam)

    del stream


for k, v in result.items():
    print('\ntype:{} fps:{} res:{} : {}\n'.format(k[0], k[1], k[2], v))
