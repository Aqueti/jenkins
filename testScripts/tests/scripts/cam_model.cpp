// checking that new model file was applied

#include "tests.h"

using namespace td;

void newCameraCallback(ACOS_CAMERA cam, void* data)
{
    ACOS_CAMERA* _cam = (ACOS_CAMERA*) data;
    *_cam = cam;
}

void frameCallback(FRAME frame, void* data)
{
    cout << "frame received" << endl;
    //FRAME *_frame = (FRAME*)data;
    //*_frame = frame;
}

int main(int argc, char * argv[])
{
    Env::setUp("cam_model");

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

    string file_path = cam_folder + "/model.json";
    string file_path2 = cam_folder + "/model.json_old";

    if (!fileExists(file_path)) exit(1);

    string cmd = "mv " + file_path + " " + file_path2;
    exec(cmd);

    updateCameraModel( cam, file_path2.c_str() );

    sleep(2);

    act_res = fileExists(file_path);

    setCameraConnection(cam, false, 10);

    disconnectFromCameraServer();

    Env::tearDown();

    return 0;
}
