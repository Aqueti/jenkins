/**
* Checking:
* mcam stream can be started
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
	Env::setUp("mcam_stream_1_high");

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

    map<int, Result> mres;
    vector<map<int, Result> > res;
    vector<ACOS_STREAM> streams;
    setCameraReceivingData(cam, true, 5);
    for (int i = 0; i < 3; i++) {
    	res.push_back(mres);
    	for (int j = 0; j < cam.mcamList.numMCams; j++) {
			streams.push_back(createMCamStream( cam, cam.mcamList.mcams[j] ));
			initStreamReceiver( fcb, streams[j], r_port + j, 2.0 );
			setStreamGoLive( streams[j] ); sleep(1);

			NUM_OF_FRAMES = 0;
			sleep(1);
			res[i][j].nof = NUM_OF_FRAMES;
			res[i][j].se = streamExists(streams[j], 2.0);

			deleteStream(streams[j]);
			closeStreamReceiver(r_port + j);
    	}
    }

    setCameraReceivingData(cam, false, 5);

    setCameraConnection(cam, false, 10);

    disconnectFromCameraServer();

    cout << "\t" << "exists\t" << "frames" << endl;
    for (int i = 0; i < res.size(); i++) {
		map<int, Result>::iterator it = res[i].begin();
		while (it != res[i].end())
		{
			cout << it->first << "\t"
				 << it->second.se << "\t"
				 << it->second.nof << "\t"
				 << (it->second.nof > 0 ? "pass" : "fail")
				 << endl;
			if (act_res) act_res = (it->second.nof > 0);
			it++;
		}
		cout << endl;
    }

    Env::tearDown();

    return 0;
}