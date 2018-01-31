/**
 * Checking:
 * DataRecoveryTool
 * 
 **/

#include "tests.h"

using namespace td;

void newCameraCallback(ACOS_CAMERA cam, void* data)
{
	ACOS_CAMERA* _cam = (ACOS_CAMERA*) data;
    *_cam = cam;
}

void frameCallback(FRAME frame, void* data)
{
	FRAME* _frame = (FRAME*)data;
	*_frame = frame;
}

int main(int argc, char * argv[])
{
	Env::setUp("cliprecovery");	

	string cmd;
	cmd = "find " + storage_path + " -name 'session*' -type d | head -1";
	string folder_name = exec(cmd); folder_name = folder_name.substr(0, folder_name.length() - 1);	
	cmd = "rm " + folder_name + "/*.*";
	exec(cmd);
	cmd = "DataRecoveryTool " + folder_name;
	exec(cmd); sleep(5);

	cout << "folder_name: " << folder_name << endl;

	if(act_res) act_res = fileExists((folder_name + "/session.json").c_str());
	if(act_res) act_res = fileExists((folder_name + "/AciBaseContainerMap.map").c_str());
	if(act_res) act_res = fileExists((folder_name + "/AciHContainerMap.map").c_str());

	if (act_res) {
		V2::restart();

		connectToCameraServer(v2_ip, port);

		ACOS_CAMERA cam;
		NEW_CAMERA_CALLBACK camCB;
		camCB.f = newCameraCallback;
		camCB.data = &cam;
		setNewCameraCallback(camCB);

		if( isCameraConnected(cam) != AQ_CAMERA_CONNECTED ){
			setCameraConnection(cam, true, 10);
		}

		fillCameraMCamList(&cam);

		FRAME frame;
		FRAME_CALLBACK fcb;
		fcb.f = frameCallback;
		fcb.data = &frame;

		ACOS_CLIP* clipList;

		if (requestStoredRecordings(&clipList) > 0) {
			ACOS_STREAM stream = createClipStream(clipList[0], profile);
			initStreamReceiver( fcb, stream, r_port, 2.0 );
			setStreamPlaySpeed(stream, 1.0);
			sleep(1);
			act_res = ( streamExists(stream, 2.0) && frame.m_metadata.m_mode != 0 );

			closeStreamReceiver(r_port);
			deleteStream(stream);
		}

		setCameraConnection(cam, false, 10);

		disconnectFromCameraServer();
	}

    Env::tearDown();

    return 0;
}
