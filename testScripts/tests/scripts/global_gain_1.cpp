/**
 * Checking:
 * global gain
 * 
 **/

#include "tests.h"

using namespace td;

void newCameraCallback(ACOS_CAMERA cam, void* data)
{
    ACOS_CAMERA* _cam = (ACOS_CAMERA*) data;
    *_cam = cam;
}

int main(int argc, char * argv[])
{
	Env::setUp("global_gain_1");

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

    toggleGlobalGainLoop( cam, false );
    toggleGlobalAutoShutterLoop( cam, false );

    int gain = rand() % static_cast<int>(20) + 1;
    for (int i = 0; i < cam.mcamList.numMCams; i++) {
		setMCamGain(cam.mcamList.mcams[i], gain);
		sleep(1);
    }

    sleep(3);

    performGlobalGain( cam );

    sleep(3);

    for (int i = 0; i < cam.mcamList.numMCams; i++) {
    	if (act_res) act_res = (getMCamGain(cam.mcamList.mcams[i]) != gain);
	}

	sleep(5);

    toggleGlobalGainLoop( cam, true );
    toggleGlobalAutoShutterLoop( cam, true );
    performGlobalGain( cam );
    performGlobalAutoShutter( cam );

    setCameraConnection(cam, false, 10);

    disconnectFromCameraServer();

    Env::tearDown();

    return 0;
}
