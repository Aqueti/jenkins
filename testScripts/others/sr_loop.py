import AQT
import ctypes
import time
import datetime as dt


api = AQT.AquetiAPI("", AQT.U8Vector(), AQT.StringVector("aqt://seneca77"))

cams = api.GetAvailableCameras()
camera = "/aqt/camera/12"

timeControl = AQT.TimeState(api)
vs = AQT.ViewState(api)
iss = AQT.ImageSubsetState(api)
ps = AQT.PoseState(api)
sp = AQT.StreamProperties()
sp.Type(AQT.aqt_STREAM_TYPE_H264)
sp.Quality(0.8)
sp.Width(1920)
sp.Height(1080)
sp.FrameRate(30)

REPEAT_TIMES = 30

for _ in range(REPEAT_TIMES):
  streams = []
  for i in range(4):
    streams.append(AQT.RenderStream(api, vs, timeControl, iss, ps, sp))
    streams[-1].AddCamera(camera)
    streams[-1].SetStreamingState(True)

  time.sleep(1)

  start_time = dt.datetime.now()
  p_length = 10
  while (dt.datetime.now()-start_time).seconds < p_length:
    for stream in streams:
      frame = stream.GetNextFrame()
      if (stream.GetStatus() == AQT.aqt_STATUS_OKAY):
        frame.ReleaseData()

  #for stream in streams:
  #  stream.SetStreamingState(False)
  #  stream.RemoveCamera(camera)
