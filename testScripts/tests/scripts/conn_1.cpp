/**
 * Checking:
 * checking connections
 * 
 **/

#include "tests.h"

using namespace td;

vector<ACOS_CAMERA> camList;
map<string, bool> map_res;
vector<map<string, bool> > res;
bool isConnected;
int times = 10;
int ind = 0;

void newCameraCallback(ACOS_CAMERA cam, void* data)
{
    camList.push_back(cam);
    res[ind]["newcam_cb"] = true;
}

void statusCallback(void* data, AQ_SYSTEM_STATE o, AQ_SYSTEM_STATE n)
{
	static AQ_SYSTEM_STATE prev = n;
	res[ind]["status_cb"] = (o == isConnected ? 100 : 101 && n == prev);
	prev = o;
}

void deletedCameraCallback(uint32_t camID, void* data)
{
	res[ind]["delcam_cb"] = ( camID == camList[0].camID );
}

int main(int argc, char * argv[])
{
	Env::setUp("conn_1");

    NEW_CAMERA_CALLBACK camCB;
    camCB.f = newCameraCallback;
    setNewCameraCallback(camCB);

	AQ_SYSTEM_STATE_CALLBACK statuscb;
	statuscb.f = statusCallback;
	setNewConnectedToServerCallback(statuscb);

	CAMERA_DELETED_CALLBACK deleteCallback;
	deleteCallback.f = deletedCameraCallback;
	setCameraDeletedCallback(deleteCallback);

    for (int i = 0; i < times; i++) {
    	res.push_back(map_res);

        connectToCameraServer(v2_ip, port);
        isConnected = true;
        res[ind]["connected"] = (isConnectedToCameraServer() == AQ_SERVER_CONNECTED);
        res[ind]["numofcams"] = (getNumberOfCameras() == camList.size());
        disconnectFromCameraServer();
        res[ind]["disconned"] = (isConnectedToCameraServer() != AQ_SERVER_CONNECTED);
        isConnected = false;
        camList.clear();
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
