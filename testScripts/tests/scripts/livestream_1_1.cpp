/**
 * Checking:
 * ability to run livestream in JPEG H264 H265
 *
 */

#include "tests.h"

using namespace td;

uint32_t NUM_OF_FRAMES = 0;

void newCameraCallback(ACOS_CAMERA cam, void* data)
{
    static int i = 0;
    ACOS_CAMERA* camList = (ACOS_CAMERA*) data;
    camList[i++] = cam;
}

void frameCallback(FRAME frame, void* data)
{
	NUM_OF_FRAMES++;
}

struct Result {
	bool se;
	int nof;
};

int main(int argc, char * argv[])
{
	Env::setUp("livestream_1_1");

	connectToCameraServer(v2_ip, port);

	ACOS_CAMERA camList[getNumberOfCameras()];
    NEW_CAMERA_CALLBACK camCB;
    camCB.f = newCameraCallback;
    camCB.data = &camList;
    setNewCameraCallback(camCB);

    ACOS_CAMERA cam = camList[0];

    if( isCameraConnected(cam) != AQ_CAMERA_CONNECTED ){
        setCameraConnection(cam, true, 10);
    }

    fillCameraMCamList(&cam);

    FRAME_CALLBACK fcb;
    fcb.f = frameCallback;
    fcb.data = {};

    ACOS_STREAM stream;
    map<char*, Result> res;

    vector<char *> modes;
    modes.push_back(V2_ENCODE_JPEG);
    modes.push_back(V2_ENCODE_H264);
    modes.push_back(V2_ENCODE_H265);
   
    for (int i = 0; i < modes.size(); i++) {
		strcpy(profile.videoEncoder.encoding, modes[i]);

		stream = createLiveStream( cam, profile );
		initStreamReceiver( fcb, stream, r_port, 2.0 );
		setStreamGoLive( stream ); sleep(1);

		NUM_OF_FRAMES = 0;
		sleep(1);

		res[modes[i]].nof = NUM_OF_FRAMES;
		res[modes[i]].se = streamExists(stream, 2.0);

		deleteStream(stream);
		closeStreamReceiver(r_port);
    }

    setCameraConnection(cam, false, 10);

    disconnectFromCameraServer();

    cout << "\t" << "exists\t" << "frames" << endl;
    std::map<char*, Result>::iterator it = res.begin();
    while (it != res.end())
    {
    	cout << it->first << "\t"
    		 << it->second.se << "\t"
    		 << it->second.nof << "\t"
             << (it->second.se && it->second.nof > 0 ? "pass" : "fail" )
    		 << endl;
        if(act_res) act_res = (it->second.se && it->second.nof > 0); 
    	it++;
    }
    
    Env::tearDown();

    return 0;
}
