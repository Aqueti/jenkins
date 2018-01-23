// checking that live stream speed can be changed

#include "tests.h"

using namespace td;

vector<FRAME> frames;

void newCameraCallback(ACOS_CAMERA cam, void* data)
{
    ACOS_CAMERA* _cam = (ACOS_CAMERA*) data;
    *_cam = cam;
}

void frameCallback(FRAME frame, void* data)
{
	frames.push_back(frame);
}

struct Range {
	double f;
	double l;
};

struct Result {
	uint32_t frames;
	int delta;
};

int main(int argc, char * argv[])
{
	Env::setUp("livestream_3_1");

    ACOS_CAMERA cam;
    NEW_CAMERA_CALLBACK camCB;
    camCB.f = newCameraCallback;
    camCB.data = &cam;
    setNewCameraCallback(camCB);

    connectToCameraServer(v2_ip, port);

    if( isCameraConnected(cam) != AQ_CAMERA_CONNECTED ){
        setCameraConnection(cam, true, 10);
    }

    fillCameraMCamList(&cam);

    FRAME_CALLBACK fcb;
    fcb.f = frameCallback;

    ACOS_STREAM stream = createLiveStream( cam, profile );
    initStreamReceiver(fcb, stream, r_port, 2.0);
    setStreamGoLive( stream );
    sleep(2);

    map<double, Result> res;

    Range range = {-3, 3};
    double speed = range.l;
    while (speed >= range.f) {
    	setStreamPlaySpeed(stream, speed); sleep(1);

    	frames.clear(); sleep(1);
		res[speed].frames = frames.size();
		res[speed].delta = (frames[res[speed].frames - 1].m_metadata.m_timestamp - frames[0].m_metadata.m_timestamp);

    	speed -= 0.5;
    }

    closeStreamReceiver(r_port);
    deleteStream(stream);

    setCameraConnection(cam, false, 10);

    disconnectFromCameraServer();

    cout << "speed" << "\t" << "frames"  << "\t" << "delta" << endl;

    map<double, Result>::iterator it = res.begin();
	while (it != res.end())
	{
		double d = it->second.delta != 0 ? (it->second.delta / it->first) / 1e6 : 1;
		cout << it->first << "\t"
			 << it->second.frames  << "\t"
			 << it->second.delta << "\t"
			 << (it->second.delta > -1e6 ? "\t" : "")
			 << (it->second.frames > 0 && (d > 0.85 && d < 1.15)? "pass" : "fail")
			 << endl;
		if (act_res) act_res = (it->second.frames > 0 && (d > 0.85 && d < 1.15));
		it++;
	}

	Env::tearDown();

    return 0;
}
