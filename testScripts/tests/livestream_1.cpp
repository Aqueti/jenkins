/**
 * Checking:
 * live stream can be started
 * 
 **/

#include "tests.h"

using namespace td;

int NUM_OF_FRAMES = 0;

void newCameraCallback(ACOS_CAMERA cam, void* data)
{
    ACOS_CAMERA* _cam = (ACOS_CAMERA*) data;
    *_cam = cam;
}

void frameCallback(FRAME frame, void* data)
{
	NUM_OF_FRAMES++;

	FRAME *_frame = (FRAME*)data;
	*_frame = frame;
}

struct Result {
	int nof;
	bool se;
};

int main(int argc, char * argv[])
{
	Env::setUp("livestream_1");

	connectToCameraServer(v2_ip, port);

	ACOS_CAMERA camList[getNumberOfCameras()];
    NEW_CAMERA_CALLBACK camCB;
    camCB.f = newCameraCallback;
    camCB.data = &camList;
    setNewCameraCallback(camCB);

    ACOS_CAMERA cam = camList[0];

    if( isCameraConnected(cam) != AQ_CAMERA_CONNECTED ){
        setCameraConnection(cam, true, 10);
    }

    fillCameraMCamList(&cam);

    FRAME frame;
    FRAME_CALLBACK fcb;
    fcb.f = frameCallback;
    fcb.data = &frame;

    ACOS_STREAM stream;
    map<int, Result> res;
    setCameraReceivingData(cam, true, 5);
    for (int i = 0; i < 10; i++) {
		stream = createLiveStream( cam, profile );
		initStreamReceiver( fcb, stream, r_port, 2.0 );
		setStreamGoLive( stream ); sleep(1);

		NUM_OF_FRAMES = 0;
		sleep(1);
		res[i].nof = NUM_OF_FRAMES;
		res[i].se = streamExists(stream, 2.0);

		deleteStream(stream);
		closeStreamReceiver(r_port);
    }
    setCameraReceivingData(cam, false, 5);

    setCameraConnection(cam, false, 10);

    disconnectFromCameraServer();

    cout << "\t" << "exists\t" << "frames" << endl;
    map<int, Result>::iterator it = res.begin();
	while (it != res.end())
	{
    	cout << it->first << "\t"
    		 << it->second.se << "\t"
    		 << it->second.nof << "\t"
    		 << (it->second.nof > 0 ? "pass" : "fail")
    		 << endl;
    	if (act_res) act_res = (it->second.nof > 0);
    	it++;
    }

    Env::tearDown();

    return 0;
}
