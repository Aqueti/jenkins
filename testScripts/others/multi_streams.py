import AQT
import sys
import ctypes
import time
import threading
from functools import wraps


def limit(n):
    sem = threading.Semaphore(n)
    def wrapper(func):
        @wraps(func)
        def wrapped(*args):
            with sem:
                return func(*args)
        return wrapped
    return wrapper

def async(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        thr = threading.Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


def check_state(obj):
    if obj.GetStatus() != AQT.aqt_STATUS_OKAY:
        exit(1)

@limit(1)
@async
def create_api(sys_name):
    while True:
        print("creating api")

        api = AQT.AquetiAPI("", AQT.U8Vector(), AQT.StringVector(['aqt://' + sys_name]))
        check_state(api)


@limit(1)
@async
def create_streams(sys_name):
    while True:

        print("creating streams")

        api = AQT.AquetiAPI("", AQT.U8Vector(), AQT.StringVector(['aqt://' + sys_name]))
        check_state(api)

        cams = api.GetAvailableCameras()
        check_state(api)

        timeControl = AQT.TimeState(api)
        check_state(timeControl)
        vs = AQT.ViewState(api)
        check_state(vs)
        iss = AQT.ImageSubsetState(api)
        check_state(iss)
        ps = AQT.PoseState(api)
        check_state(ps)
        sp = AQT.StreamProperties()
        check_state(sp)
        sp.Type(AQT.aqt_STREAM_TYPE_H264)
        check_state(sp)

        streams = []
        for j in range(2):
            streams.append(AQT.RenderStream(api, vs, timeControl, iss, ps, sp))
            check_state(streams[-1])
            streams[j].AddCamera(cams[0].Name())
            check_state(streams[-1])
            streams[j].SetStreamingState(True)
            check_state(streams[-1])

            time.sleep(0.25)


if __name__ == '__main__':
    sys_name = 'seneca77'

    create_api(sys_name)
    create_streams(sys_name)
