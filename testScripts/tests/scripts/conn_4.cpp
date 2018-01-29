/**
 * Checking:
 * connections v2->dc, dc->v2
 * 
 **/

#include "tests.h"

using namespace td;

void newCameraCallback(ACOS_CAMERA cam, void* data)
{
    ACOS_CAMERA* _cam = (ACOS_CAMERA*) data;
    *_cam = cam;
}

void statusCallback(void* data, AQ_SYSTEM_STATE o, AQ_SYSTEM_STATE n)
{
    cout << "got status callback" << endl;
}

int main(int argc, char * argv[])
{
    Env::setUp("conn_4");

    int times = 1;

    ACOS_CAMERA cam;
    NEW_CAMERA_CALLBACK camCB;
    camCB.f = newCameraCallback;
    camCB.data = &cam;
    setNewCameraCallback(camCB);

    map<string, bool> res;

    res["dc_v2"] = true; // connect to mcam(direct connection) and then to mcam(connection to render)
    res["v2_dc"] = true; // connect to mcam(connection to render) and then to mcam(direct connection)
    res["v2_dc_o"] = true; // connect to mcam(connection to render) and then to mcam(direct connection) without disconnecting
    res["dc_v2_o"] = true;  // connect to mcam(direct connection) and then to mcam(connection to render) without disconnecting
    res["render_t"] = true; // connect twice without disconnecting
    res["mcam_dc_t"] = true;
    res["mcam_v2_t"] = true;

    for (int i = 0; i < times; i++) {
        mCamConnect(mcam_ip, port);
        if(res["dc_v2"]) res["dc_v2"] = (getNumberOfMCams() > 0);
        mCamDisconnect(mcam_ip, port);
        if(res["dc_v2"]) res["dc_v2"] = (getNumberOfMCams() == 0);

        connectToCameraServer(v2_ip, port);
        if(isConnectedToCameraServer() == AQ_SERVER_CONNECTED){
            setCameraConnection(cam, true, 10);
            if(res["dc_v2"]) res["dc_v2"] = (isCameraConnected(cam) == AQ_CAMERA_CONNECTED);
            setCameraConnection(cam, false, 10);
            if(res["dc_v2"]) res["dc_v2"] = (isCameraConnected(cam) != AQ_CAMERA_CONNECTED);
        }
        disconnectFromCameraServer();
    }

    for (int i = 0; i < times; i++) {
        connectToCameraServer(v2_ip, port);
        if(isConnectedToCameraServer() == AQ_SERVER_CONNECTED){
            setCameraConnection(cam, true, 10);
            if(res["v2_dc"]) res["v2_dc"] = (isCameraConnected(cam) == AQ_CAMERA_CONNECTED);
        }

        mCamConnect(mcam_ip, port);
        if(res["v2_dc"]) res["v2_dc"] = (getNumberOfMCams() > 0);

        setCameraConnection(cam, false, 10);
        if(res["v2_dc"]) res["v2_dc"] = (isCameraConnected(cam) != AQ_CAMERA_CONNECTED);

        disconnectFromCameraServer();

        mCamDisconnect(mcam_ip, port);
        if(res["v2_dc"]) res["v2_dc"] = (getNumberOfMCams() == 0);
    }

    for (int i = 0; i < times; i++) {
        connectToCameraServer(v2_ip, port);
        connectToCameraServer(v2_ip, port);
        if(res["render_t"]) res["render_t"] = (isConnectedToCameraServer() == AQ_SERVER_CONNECTED);
        disconnectFromCameraServer();
        disconnectFromCameraServer();
        if(res["render_t"]) res["render_t"] = (isConnectedToCameraServer() != AQ_SERVER_CONNECTED);
    }

    for (int i = 0; i < times; i++) {
        connectToCameraServer(v2_ip, port);
        if(isConnectedToCameraServer() == AQ_SERVER_CONNECTED){
            setCameraConnection(cam, true, 10);
            setCameraConnection(cam, true, 10);
            if(res["mcam_v2_t"]) res["mcam_v2_t"] = (isCameraConnected(cam) == AQ_CAMERA_CONNECTED);
            setCameraConnection(cam, false, 10);
            setCameraConnection(cam, false, 10);
            if(res["mcam_v2_t"]) res["mcam_v2_t"] = (isCameraConnected(cam) != AQ_CAMERA_CONNECTED);
        }
        disconnectFromCameraServer();
    }

    for (int i = 0; i < times; i++) {
        mCamConnect(mcam_ip, port);
        mCamConnect(mcam_ip, port);
        if(res["mcam_dc_t"]) res["mcam_dc_t"] = (getNumberOfMCams() > 0);
        mCamDisconnect(mcam_ip, port);
        mCamDisconnect(mcam_ip, port);
        if(res["mcam_dc_t"]) res["mcam_dc_t"] = (getNumberOfMCams() == 0);
    }

	map<string, bool>::iterator it = res.begin();
	while (it != res.end())
	{
		cout << it->first << "\t"
			 << (it->first.length() < 8 ? "\t" : "")
			 << it->second << "\t"
			 << (it->second ? "pass" : "fail")
			 << endl;
		if(act_res) act_res = it->second;
		it++;
	}

	Env::tearDown();

    return 0;
}
