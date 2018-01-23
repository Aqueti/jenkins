#include "tests.h"

using namespace td;

void newCameraCallback(ACOS_CAMERA cam, void* data)
{
    ACOS_CAMERA* _cam = (ACOS_CAMERA*) data;
    *_cam = cam;
}

int main(int argc, char * argv[])
{
	Env::setUp("global_wb_1");

    ACOS_CAMERA cam;
	NEW_CAMERA_CALLBACK camCB;
    camCB.f = newCameraCallback;
    camCB.data = &cam;
    setNewCameraCallback(camCB);

    connectToCameraServer(v2_ip, port);

    if(isCameraConnected(cam) != AQ_CAMERA_CONNECTED) {
        setCameraConnection(cam, true, 10);
    }

    fillCameraMCamList(&cam);

    toggleGlobalWhiteBalanceAutoLoop( cam, false );

    performGlobalWhiteBalance( cam );

    sleep(5);

    int d = 0.01;
    for (int i = 0; i < (cam.mcamList.numMCams - 1); i++) {
    	if(act_res) act_res = (abs(getMCamWhiteBalance(cam.mcamList.mcams[i]).red -
				       getMCamWhiteBalance(cam.mcamList.mcams[i+1]).red) <= d);

    	if(act_res) act_res = (abs(getMCamWhiteBalance(cam.mcamList.mcams[i]).green -
				       getMCamWhiteBalance(cam.mcamList.mcams[i+1]).green) <= d);

    	if(act_res) act_res = (abs(getMCamWhiteBalance(cam.mcamList.mcams[i]).blue -
				       getMCamWhiteBalance(cam.mcamList.mcams[i+1]).blue) <= d);
	}

    setCameraConnection(cam, false, 10);

    disconnectFromCameraServer();

    Env::tearDown();

    return 0;
}
