//checking the issue with a broken live stream when CamViewer started and stopped

#include "tests.h"

using namespace td;

void newCameraCallback(ACOS_CAMERA cam, void* data)
{
    ACOS_CAMERA* _cam = (ACOS_CAMERA*) data;
    *_cam = cam;
}

void mcamFrameCallback(FRAME frame, void* data)
{
    std::cout << frame.m_metadata.m_camId << endl;
}

void newMCamCallback(MICRO_CAMERA mcam, void* data)
{
    static int i = 0;
	MICRO_CAMERA* mcamList = (MICRO_CAMERA*) data;
	mcamList[i++] = mcam;
}

void frameCallback(FRAME frame, void* data)
{

}

int main(int argc, char * argv[])
{
	Env::setUp("livestream_5");

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

    vector<ACOS_STREAM> streams;

    streams.push_back(createLiveStream( cam, profile ));

    FRAME_CALLBACK fcb;
    fcb.f = frameCallback;
    fcb.data = {};
    initStreamReceiver(fcb, streams[0], r_port, 2.0);

    sleep(1);

	MICRO_CAMERA mCamList[cam.mcamList.numMCams];
	NEW_MICRO_CAMERA_CALLBACK mcamCB;
	mcamCB.f = newMCamCallback;
	mcamCB.data = &mCamList;
	setNewMCamCallback(mcamCB);

	FRAME frame;
	MICRO_CAMERA_FRAME_CALLBACK frameCB;
	frameCB.f = mcamFrameCallback;
	frameCB.data = &frame;
	setMCamFrameCallback(frameCB);

    for(int k = 0; k < 10; k++) {
		mCamConnect(mcam_ip, port);

		int num_of_mcams = getNumberOfMCams();

		for (int i = 0; i < num_of_mcams; i++) {
			initMCamFrameReceiver(2*r_port + i, 1.0);
			startMCamStream(mCamList[i], 2*r_port + i);
		}

		sleep(1);

		for (int i = 0; i < num_of_mcams; i++) {
			stopMCamStream(mCamList[i], 2*r_port + i);
			closeMCamFrameReceiver(2*r_port + i);
		}

		mCamDisconnect(mcam_ip, port);
    }

    for (int i = 0; i < streams.size(); i++) {
    	if (act_res) act_res = streamExists(streams[i], 2.0);
		deleteStream(streams[i]);
    }

    closeStreamReceiver(r_port);

    setCameraConnection(cam, false, 10);

    disconnectFromCameraServer();

    Env::tearDown();

    return 0;
}
