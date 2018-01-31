/**
* Checking:
* mcam stream can be started
*
**/

#include "tests.h"

using namespace td;

int NUM_OF_FRAMES = 0;

void newMCamCallback(MICRO_CAMERA mcam, void* data)
{
    static int i = 0;
	MICRO_CAMERA* mcamList = (MICRO_CAMERA*) data;
	mcamList[i++] = mcam;
}

void mcamFrameCallback(FRAME frame, void* data)
{
	NUM_OF_FRAMES++;

	FRAME *_frame = (FRAME*)data;
	*_frame = frame;
}

struct Result {
	int nof;
};

int main(int argc, char * argv[])
{
	Env::setUp("mcam_stream_1_low");

	mCamConnect(mcam_ip, port);

	int num_of_mcams = getNumberOfMCams();

	MICRO_CAMERA mCamList[num_of_mcams];
	NEW_MICRO_CAMERA_CALLBACK mcamCB;
	mcamCB.f = newMCamCallback;
	mcamCB.data = &mCamList;
	setNewMCamCallback(mcamCB);

	FRAME frame;
	MICRO_CAMERA_FRAME_CALLBACK frameCB;
	frameCB.f = mcamFrameCallback;
	frameCB.data = &frame;
	setMCamFrameCallback(frameCB);

    map<int, Result> mres;
    vector<map<int, Result> > res;
	for (int i = 0; i < 3; i++) {
		res.push_back(mres);
		for (int j = 0; j < num_of_mcams; j++) {
			initMCamFrameReceiver(r_port + j, 1.0);
			startMCamStream(mCamList[j], r_port + j);

			sleep(1);
			NUM_OF_FRAMES = 0;
			sleep(1);
			res[i][j].nof = NUM_OF_FRAMES;

			stopMCamStream(mCamList[j], r_port + j);
			closeMCamFrameReceiver(r_port + j);
		}
	}

    mCamDisconnect(mcam_ip, port);

    cout << "\t" << "frames" << endl;
    for (int i = 0; i < res.size(); i++) {
		map<int, Result>::iterator it = res[i].begin();
		while (it != res[i].end())
		{
			cout << it->first << "\t"				
				 << it->second.nof << "\t"
				 << (it->second.nof > 0 ? "pass" : "fail")
				 << endl;
			if (act_res) act_res = (it->second.nof > 0);
			it++;
		}
		cout << endl;
    }

    Env::tearDown();

    return 0;
}
