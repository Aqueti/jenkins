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

void newClipCallback(ACOS_CLIP clip, void* data)
{
	ACOS_CLIP* _clip = (ACOS_CLIP*)data;
	*_clip = clip;
}

void deletedClipCallback(ACOS_CLIP clip, void* data) {

}

int main(int argc, char * argv[])
{
	Env::setUp("cliprec_1");

	int num_of_clips = 1;
	int duration = 5;

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

    ACOS_CLIP clip_rc;
	ACOS_CLIP_CALLBACK clipcb;
	clipcb.f = newClipCallback;
	clipcb.data = &clip_rc;
	setNewClipCallback(clipcb);

	ACOS_CLIP_CALLBACK clipCallback;
	clipCallback.f = deletedClipCallback;
	setClipDeletedCallback(clipCallback);

	ACOS_CLIP* clipList;
	uint16_t i = requestStoredRecordings(&clipList);

	setCameraReceivingData(cam, true, 5);
	for(int i = 0; i < num_of_clips; i++) {
		setCameraRecording(cam , true, 5);
		sleep(duration);
		setCameraRecording(cam , false, 5);
	}
	setCameraReceivingData(cam, false, 5);

	uint16_t j = requestStoredRecordings(&clipList);

	map<string, bool> map_res;
	vector<map<string, bool> > res;

	for (int k = i; k < j; k++) {
		//cout << "clip #"<< k << " length: " << clipList[k].endTime - clipList[k].startTime << endl;

		res.push_back(map_res);

		string path = storage_path + "/session_" + string(clipList[k].name) + "/";

		res[k - i]["_bc_map_"] = fileExists(path + "AciBaseContainerMap.map");
		res[k - i]["_hc_map_"] = fileExists(path + "AciHContainerMap.map");
		res[k - i]["_session_"] = fileExists(path + "session.json");
		res[k - i]["clipsnum"] = ((j - i) == num_of_clips);
		res[k - i]["cliplength"] = (abs(duration*1e6 - (clipList[k].endTime - clipList[k].startTime)) < 1e5);
		res[k - i]["new_clip_cb"] = (clip_rc.cam.camID == cam.camID);
	}

    setCameraConnection(cam, false, 10);

    disconnectFromCameraServer();

	for (int i = 0; i < res.size(); i++) {
		cout << "name: " << clipList[j + i - num_of_clips].name << endl;
		cout << "\t\t" << "act" << endl;
		map<string, bool>::iterator it = res[i].begin();
		while (it != res[i].end())
		{
			cout << it->first << "\t"
				 << it->second << "\t"
				 << (it->second ? "pass" : "fail")
				 << endl;
			if(act_res) act_res = it->second;
			it++;
		}
		cout << endl;
	}

	Env::tearDown();

    return 0;
}
