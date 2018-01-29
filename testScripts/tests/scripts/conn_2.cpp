/**
 * Checking:
 * connections to mcams(connection to render)
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
}

void cameraConnectionCallback( ACOS_CAMERA cam, void* data, short int o, short int n )
{	
	static short int prev = n;
	res[ind]["status_cb"] = (o == isConnected ? 100 : 101 && n == prev);
	prev = o;
}

int main(int argc, char * argv[])
{
	Env::setUp("conn_2");

    NEW_CAMERA_CALLBACK camCB;
    camCB.f = newCameraCallback;
    setNewCameraCallback(camCB);

	CAMERA_CALLBACKS callbacks;
	callbacks.cameraConnectionCallback.f = cameraConnectionCallback;

	setCameraPropertyCallbacks( callbacks );

    connectToCameraServer(v2_ip, port);
    for (int i = 0; i < times; i++) {
    	res.push_back(map_res);

		setCameraConnection(camList[0], true, 10);
		res[ind]["connected"] = (isCameraConnected(camList[0]) == 110);
		res[ind]["numofcams"] = (getCameraNumberOfMCams(camList[0]) > 0);
		isConnected = true;

		setCameraConnection(camList[0], false, 10);
		res[ind]["disconned"] = (isCameraConnected(camList[0]) == 111);
		isConnected = false;

		camList.clear();
		ind++;
	}
    disconnectFromCameraServer();

    bool act_res = true;

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


