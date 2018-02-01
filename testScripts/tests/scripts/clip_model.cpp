/**
 * Checking:
 * new clip model file was applied
 *
 */

#include "tests.h"

using namespace td;

void newCameraCallback(ACOS_CAMERA cam, void* data)
{
    ACOS_CAMERA* _cam = (ACOS_CAMERA*) data;
    *_cam = cam;
}

struct Result {
    bool rc;
    int act1;
    int act2;
    int act3;
};

int main(int argc, char * argv[])
{
	Env::setUp("clip_model");

    ACOS_CAMERA cam;
    NEW_CAMERA_CALLBACK camCB;
    camCB.f = newCameraCallback;
    camCB.data = &cam;
    setNewCameraCallback(camCB);

    connectToCameraServer(v2_ip, port);

	ACOS_CLIP* clipList;

	Result res;

    res.act1 = requestStoredRecordings(&clipList);

    string cmd;
	cmd = "find " + storage_path + " -name 'session*' -type d | head -1";
	string folder_name = exec(cmd);
	folder_name = folder_name.substr(0, folder_name.length() - 1);
	cmd = "mv " + folder_name + "/session.json "+ folder_name + "/session.json_old";
	exec(cmd);

    if (res.act1 == 0) exit(1);

	V2::restart();

	res.act2 = requestStoredRecordings(&clipList);

    res.rc = updateClipModels( clipList[0], (folder_name + "/session.json_old").c_str() );

    V2::restart();

    res.act3 = requestStoredRecordings(&clipList);   

    cout << "act1\t" << "act2\t" << "act3\t" << "rc" << endl;
    cout << res.act1 << "\t"
         << res.act2 << "\t"
         << res.act3 << "\t"
         << res.rc << "\t"
         << (res.rc ? ((((res.act1 - res.act2) == 1) && res.act1 == res.act3) ? "pass" : "fail") : "n/a")
         << endl;

         act_res = (((res.act1 - res.act2) == 1) && res.act1 == res.act3);
   
    setCameraConnection(cam, false, 10);

    disconnectFromCameraServer();

    Env::tearDown();
    
    return 0;
}
