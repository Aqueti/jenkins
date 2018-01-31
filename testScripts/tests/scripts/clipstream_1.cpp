/**
 * Checking:
 * clip stream can be started
 * 
 **/

#include "tests.h"

using namespace td;

uint32_t NUM_OF_FRAMES = 0;

void newCameraCallback(ACOS_CAMERA cam, void* data)
{
	ACOS_CAMERA* _cam = (ACOS_CAMERA*) data;
    *_cam = cam;
}

void frameCallback(FRAME frame, void* data)
{
	NUM_OF_FRAMES++;

    FRAME* _frame = (FRAME*)data;
	*_frame = frame;
}

struct Result {
	int nof;
	bool se;
};

int main(int argc, char * argv[])
{
	Env::setUp("clipstream_1");

	int num_of_clips = 1;

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

	ACOS_CLIP* clipList;

	uint16_t size = requestStoredRecordings(&clipList);

	for (int i = 0; i < size; i++) {
		deleteClip( clipList[i] );
	}

	setCameraReceivingData(cam, true, 5);
	for(int i = 0; i < num_of_clips; i++) {
		setCameraRecording(cam , true, 5);
		sleep(5);
		setCameraRecording(cam , false, 5);
	}
	setCameraReceivingData(cam, false, 5);
	size = requestStoredRecordings(&clipList);

	FRAME frame;
	FRAME_CALLBACK fcb;
	fcb.f = frameCallback;
	fcb.data = &frame;

	map<string, Result> res;
	ACOS_STREAM stream;

    vector<char *> modes;
    modes.push_back(V2_ENCODE_JPEG);
    modes.push_back(V2_ENCODE_H264);
    modes.push_back(V2_ENCODE_H265);

    for (int i = 0; i < modes.size(); i++) {
        strcpy(profile.videoEncoder.encoding, modes[i]); 
             
        stream = createClipStream(clipList[size - 1], profile);
        initStreamReceiver( fcb, stream, r_port, 2.0 );
        setStreamPlaySpeed(stream, 1.0);
        
        res[modes[i]].se = streamExists(stream, 2.0);
        NUM_OF_FRAMES = 0;
        sleep(1);
        res[modes[i]].nof = NUM_OF_FRAMES;
        
        closeStreamReceiver(r_port);
        deleteStream(stream);
        sleep(1);
    }

    setCameraConnection(cam, false, 10);

    disconnectFromCameraServer();

    cout << "\t" << "exists\t" << "nof\t" << "" << endl;
	map<string, Result>::iterator it = res.begin();
	while (it != res.end())
	{
		cout << it->first << "\t"
			 << it->second.se << "\t"
			 << it->second.nof << "\t"
			 << (it->second.se && it->second.nof > 0 ? "pass" : "fail")
			 << endl;
		if(act_res) act_res = (it->second.se && it->second.nof > 0);
		it++;
	}

	Env::tearDown();

    return 0;
}
