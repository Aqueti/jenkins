//checking that several streams can be opened by V2 at the same time

#include "tests.h"

using namespace td;

struct result {
	bool se;
	int nof;
};

vector<result> res;
bool isCounting;
int ind;

void newCameraCallback(ACOS_CAMERA cam, void* data)
{
    ACOS_CAMERA* _cam = (ACOS_CAMERA*) data;
    *_cam = cam;
}

void frameCallback0(FRAME frame, void* data)
{
	static int NUM_OF_FRAMES = 0;

	if (isCounting)	NUM_OF_FRAMES++;
	else if (res[0].nof == 0) res[0].nof = NUM_OF_FRAMES;
}

void frameCallback1(FRAME frame, void* data)
{
	static int NUM_OF_FRAMES = 0;

	if (isCounting)	NUM_OF_FRAMES++;
	else if (res[1].nof == 0) res[1].nof = NUM_OF_FRAMES;
}

void frameCallback2(FRAME frame, void* data)
{
	static int NUM_OF_FRAMES = 0;

	if (isCounting)	NUM_OF_FRAMES++;
	else if (res[2].nof == 0) res[2].nof = NUM_OF_FRAMES;
}

int main(int argc, char * argv[])
{
    Env::setUp("livestream_2");

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

	STREAM_PROFILE profile;
    profile.videoSource.width = 3840;
    profile.videoSource.height = 2144;
    profile.videoEncoder.width = 1920;
    profile.videoEncoder.height = 1080;
    profile.videoEncoder.quality = 4;
    profile.videoEncoder.sessionTimeout = 10;
    profile.videoEncoder.framerate = 30;
    profile.videoEncoder.encodingInterval = 50;
    profile.videoEncoder.bitrateLimit = 2048;
    strcpy(profile.videoEncoder.encoding, V2_ENCODE_H264);

    vector<ACOS_STREAM> streams;

    FRAME_CALLBACK fcb;

    for (ind = 0; ind < 3; ind++) {
    	res.push_back({});
    	streams.push_back(createLiveStream( cam, profile ));

    	if (ind == 0) fcb.f = frameCallback0;
    	else if (ind == 1) fcb.f = frameCallback1;
    	else fcb.f = frameCallback2;
    	initStreamReceiver( fcb, streams[ind], r_port + ind, 2.0 );

    	setStreamGoLive(streams[ind]);
		res[ind].se = streamExists(streams[ind], 2.0);
    }

    isCounting = true;
    sleep(1);
    isCounting = false;

    for (int i = 0; i < streams.size(); i++) {
    	closeStreamReceiver(r_port + i);
    	deleteStream(streams[i]);
    }

    setCameraConnection(cam, false, 10);

    disconnectFromCameraServer();

    cout << "\t" << "exists\t" << "frames" << endl;
    for (int i = 0; i < res.size(); i++) {
    	cout << i << "\t"
    		 << res[i].se << "\t"
    		 << res[i].nof << "\t"
    		 << (res[i].nof > 0 ? "pass" : "fail")
    		 << endl;
    	if (act_res) act_res = (res[i].nof > 0);
    }

    Env::tearDown();

    return 0;
}
