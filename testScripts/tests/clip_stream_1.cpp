// checking that clip stream can be started

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

struct result {
	int mode;
	bool se;
};

int main(int argc, char * argv[])
{
	Env::setUp("clip_stream");

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

	map<string, result> res;
	ACOS_STREAM stream;

    strcpy(profile.videoEncoder.encoding, V2_ENCODE_JPEG); frame = {};

    stream = createClipStream(clipList[size - 1], profile);
    initStreamReceiver( fcb, stream, r_port, 2.0 );
    setStreamPlaySpeed(stream, 1.0);
    sleep(1);
    res["JPEG"].se = streamExists(stream, 2.0);
    res["JPEG"].mode = frame.m_metadata.m_mode;
    closeStreamReceiver(r_port);
    deleteStream(stream);

    strcpy(profile.videoEncoder.encoding, V2_ENCODE_H264); frame = {};

    stream = createClipStream(clipList[size - 1], profile);
    initStreamReceiver( fcb, stream, r_port, 2.0 );
    setStreamPlaySpeed(stream, 1.0);
    sleep(2);
    res["H264"].se = streamExists(stream, 2.0);
    res["H264"].mode = frame.m_metadata.m_mode;
    closeStreamReceiver(r_port);
    deleteStream(stream);

    strcpy(profile.videoEncoder.encoding, V2_ENCODE_H265); frame = {};

    stream = createClipStream(clipList[size - 1], profile);
    initStreamReceiver( fcb, stream, r_port, 2.0 );
    setStreamPlaySpeed(stream, 1.0);
    sleep(2);
    res["H265"].se = streamExists(stream, 2.0);
    res["H265"].mode = frame.m_metadata.m_mode;
    closeStreamReceiver(r_port);
    deleteStream(stream);

    setCameraConnection(cam, false, 10);

    disconnectFromCameraServer();

    cout << "\t" << "stream\t" << "mode\t" << "" << endl;
	map<string, result>::iterator it = res.begin();
	while (it != res.end())
	{
		cout << it->first << "\t"
			 << it->second.se << "\t"
			 << it->second.mode << "\t"
			 << (it->second.se && it->second.mode != 0 ? "pass" : "fail")
			 << endl;
		if(act_res) act_res = (it->second.se && it->second.mode != 0);
		it++;
	}

	Env::tearDown();

    return 0;
}
