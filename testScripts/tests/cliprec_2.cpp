// checking that all frames are saved

#include "tests.h"

using namespace td;

vector<FRAME> frames;
vector<FRAME> saved_frames;
bool isRecording = false;
bool isPlaying = false;
ACOS_CLIP clip;

void newCameraCallback(ACOS_CAMERA cam, void* data)
{
    ACOS_CAMERA* _cam = (ACOS_CAMERA*) data;
    *_cam = cam;
}

void frameCallback(FRAME frame, void* data)
{
	if (isRecording) {
		frames.push_back(frame);
	}
	if (isPlaying) {
		static FRAME f_frame;
		if(f_frame.m_image == NULL) f_frame = frame;
		if((frame.m_metadata.m_timestamp - f_frame.m_metadata.m_timestamp) <= (clip.endTime - clip.startTime)) {
			saved_frames.push_back(frame);
		}
		else {
			isPlaying = false;
		}
	}

	FRAME* _frame = (FRAME*)data;
	*_frame = frame;
}

void newClipCallback(ACOS_CLIP clip, void* data)
{
	ACOS_CLIP* _clip = (ACOS_CLIP*)data;
	*_clip = clip;
}

int main(int argc, char * argv[])
{
	Env::setUp("cliprec_2");

	int duration = 5;

    connectToCameraServer(v2_ip, port);

    ACOS_CAMERA cam;
    NEW_CAMERA_CALLBACK camCB;
    camCB.f = newCameraCallback;
    camCB.data = &cam;
    setNewCameraCallback(camCB);

    if( isCameraConnected(cam) != AQ_CAMERA_CONNECTED ) {
        setCameraConnection(cam, true, 10);
    }

    fillCameraMCamList(&cam);

    FRAME frame;
    FRAME_CALLBACK fcb;
    fcb.f = frameCallback;
    fcb.data = &frame;

	setCameraReceivingData(cam, true, 5);

    ACOS_STREAM stream = createLiveStream( cam, profile );
    initStreamReceiver( fcb, stream, r_port, 2.0 );
    setStreamGoLive( stream );
    sleep(3);

	ACOS_CLIP_CALLBACK clipcb;
	clipcb.f = newClipCallback;
	clipcb.data = &clip;
	setNewClipCallback(clipcb);

	setCameraRecording(cam , true, 5);

	if(isCameraRecording(cam)) {
		isRecording = true;
		sleep(duration);
		isRecording = false;
	}

	setCameraRecording(cam, false, 5);

    deleteStream(stream);
    closeStreamReceiver(r_port);

    setCameraReceivingData(cam, false, 5);

    stream = createClipStream( clip, profile );
    initStreamReceiver( fcb, stream, r_port, 2.0 );
    setStreamPlaySpeed(stream, 1.0);

    isPlaying = true;
    while(isPlaying) sleep(0.03);

    deleteStream(stream);
    closeStreamReceiver(r_port);

    setCameraConnection(cam, false, 10);

    disconnectFromCameraServer();

    cout << "frames" << "\t"
    	 << "saved_frames" << "\n"
    	 << frames.size() << "\t"
    	 << saved_frames.size() << "\t"
    	 << ((frames.size() / saved_frames.size() < 1.05 &&  frames.size() / saved_frames.size() > 0.95) ? "pass" : "fail")
    	 << endl;

    act_res = (frames.size() / saved_frames.size() < 1.05 &&  frames.size() / saved_frames.size() > 0.95);

    Env::tearDown();

    return 0;
}
