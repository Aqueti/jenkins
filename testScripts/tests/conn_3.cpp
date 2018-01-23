// checking connections to mcams(direct connection)

#include "tests.h";

using namespace td;

vector<MICRO_CAMERA> mcamList;
map<string, bool> map_res;
vector<map<string, bool> > res;
bool isConnected;
int times = 10;
int ind = 0;

void newMCameraCallback(MICRO_CAMERA mcam, void* data)
{
	mcamList.push_back(mcam);
	res[ind]["newmcam_cb"] = true;
}

int main(int argc, char * argv[])
{
    Env::setUp("conn_3");

	NEW_MICRO_CAMERA_CALLBACK mcamcb;
	mcamcb.f = newMCameraCallback;
	setNewMCamCallback(mcamcb);

    for (int i = 0; i < times; i++) {
    	res.push_back(map_res);

    	res[ind]["newmcam_cb"] = false;
		mCamConnect(mcam_ip, port);
		res[ind]["connected"] = (getNumberOfMCams() > 0);
		res[ind]["numofmcams"] = (getNumberOfMCams() > 0);
		isConnected = true;

		mCamDisconnect(mcam_ip, port);
		res[ind]["disconned"] = (getNumberOfMCams() == 0);
		isConnected = false;

		mcamList.clear();
		ind++;
    }

	for (int i = 0; i < times; i++) {
		cout << "time: " << i << endl;
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

