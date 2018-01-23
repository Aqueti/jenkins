// checking that frame step is working properly

#include "tests.h"

using namespace td;

vector<FRAME> frames;
vector<FRAME> sframes;
bool isStreaming = true;

void newCameraCallback(ACOS_CAMERA cam, void* data)
{
    ACOS_CAMERA* _cam = (ACOS_CAMERA*) data;
    *_cam = cam;
}

void frameCallback(FRAME frame, void* data)
{
	if (isStreaming) {
		int last_ind = frames.size() - 1;
		if(last_ind < 0) frames.push_back(frame);
		else {
			if (frames[last_ind].m_metadata.m_timestamp != frame.m_metadata.m_timestamp) {
				frames.push_back(frame);
			}
		}
	}

	FRAME* _frame = (FRAME*)data;
	*_frame = frame;
}

struct Result {
	uint64_t exp;
	uint64_t act;
	int delta;
};

struct Range {
	double f;
	double l;
};

int main(int argc, char * argv[])
{
	Env::setUp("livestream_3_2");

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

    FRAME frame;
    FRAME_CALLBACK fcb;
    fcb.f = frameCallback;
    fcb.data = &frame;

    ACOS_STREAM stream = createLiveStream( cam, profile );
    initStreamReceiver(fcb, stream, r_port, 2.0);
    setStreamGoLive( stream );
    sleep(2);
    setStreamPlaySpeed(stream, 0.0);
    sleep(1);
    isStreaming = false;

    map<int, Result> res;
    Range range = {-5, 5};
    int ind = range.f;
	for(int step = range.f; step <= range.l; ind += ++step) {
		streamFrameStep(stream, step);
		sleep(1);
		sframes.push_back(frame);

		res[step].exp = frames[frames.size() - 1].m_metadata.m_timestamp + ind * 3.33*1e4;
		res[step].act = sframes[sframes.size() - 1].m_metadata.m_timestamp;
		res[step].delta = (int)(res[step].act - res[step].exp);
	}

    closeStreamReceiver(r_port);
    deleteStream(stream);

    setCameraConnection(cam, false, 10);

    disconnectFromCameraServer();

    cout << "step" << "\t" << "exp"  << "\t\t\t" << "act" << "\t\t\t" << "delta" << endl;

    map<int, Result>::iterator it = res.begin();
	while (it != res.end())
	{
		cout << it->first << "\t"
			 << it->second.exp  << "\t"
			 << it->second.act << "\t"
			 << it->second.delta << "\t"
			 << (it->second.delta < 7e4 ? "pass" : "fail")
			 << endl;
		if (act_res) act_res = (it->second.delta < 7e4);
		it++;
	}

	Env::tearDown();

    return 0;
}
