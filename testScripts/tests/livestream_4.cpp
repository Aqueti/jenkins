// checking that live stream can't be started when model.json is missing

#include "tests.h";

using namespace td;

void newCameraCallback(ACOS_CAMERA cam, void* data)
{
    ACOS_CAMERA* _cam = (ACOS_CAMERA*) data;
    *_cam = cam;
}

void frameCallback(FRAME frame, void* data)
{

}

int main(int argc, char * argv[])
{
	Env::setUp("livestream_4");

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

    string cmd;
	cmd = "mv " + cam_folder + "/model.json " + cam_folder + "/model_old.json";
	exec(cmd);

	FRAME_CALLBACK fcb;
	fcb.f = frameCallback;
	fcb.data = {};

    ACOS_STREAM stream = createLiveStream( cam, profile );
    initStreamReceiver(fcb, stream, r_port, 2.0);

    setStreamGoLive(stream);

    sleep(1);

    act_res = streamExists(stream, 2.0);
	deleteStream(stream);

    closeStreamReceiver(r_port);

    cmd = "mv " + cam_folder + "/model_old.json " + cam_folder + "/model.json";
    exec(cmd);

    //updateCameraModel( cam, (cam_folder + "/mantis_old.json").c_str() );

    setCameraConnection(cam, false, 10);

    disconnectFromCameraServer();

    Env::tearDown();

    return 0;
}
