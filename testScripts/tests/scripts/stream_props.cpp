/**
 * Checking:
 * stream properties
 * 
 **/

#include "tests.h"

using namespace td;

void newCameraCallback(ACOS_CAMERA mcam, void* data)
{
    ACOS_CAMERA* _mcam = (ACOS_CAMERA*) data;
    *_mcam = mcam;
}

void frameCallback(FRAME frame, void* data)
{
    std::cout << frame.m_metadata.m_camId << ": " << frame.m_metadata.m_timestamp << '\n';
}

struct result{
	AtlRange_32f range;
	bool rc;
	double exp;
	double act;
};

int main(int argc, char * argv[])
{
	Env::setUp("stream_props");

	map<string, result> res;

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

	ACOS_STREAM stream = createLiveStream( cam,  profile);
	initStreamReceiver( fcb, stream, r_port, 2.0 );
	setStreamGoLive( stream );

	res["gain"].range = getStreamGainRange(stream);
	res["offset"].range = getStreamOffsetRange(stream);
	res["gamma"].range = getStreamGammaRange(stream);
	res["denoise"].range = {0,1};
	res["smoothd"].range = getStreamSmoothDenoiseRange(stream);
	res["edged"].range = getStreamEdgeDenoiseRange(stream);

	res["gain"].exp = getRnd(res["gain"].range);
	res["offset"].exp = getRnd(res["offset"].range);
	res["gamma"].exp =  getRnd(res["gamma"].range);
	res["denoise"].exp = (bool)getRnd(res["denoise"].range);
	res["smoothd"].exp = getRnd(res["smoothd"].range);
	res["edged"].exp = getRnd(res["edged"].range);

	res["gain"].rc = setStreamGain(stream, res["gain"].exp);
	res["offset"].rc = setStreamOffset(stream, res["offset"].exp);
	res["gamma"].rc = setStreamGamma(stream, res["gamma"].exp);
	res["denoise"].rc = setStreamDenoise(stream, (bool)res["denoise"].exp);
	res["smoothd"].rc = setStreamSmoothDenoise(stream, res["smoothd"].exp);
	res["edged"].rc = setStreamEdgeDenoise(stream, res["edged"].exp);

	sleep(2);

	res["gain"].act = getStreamGain(stream);
	res["offset"].act = getStreamOffset(stream);
	res["gamma"].act = getStreamGamma(stream);
	res["denoise"].act = (double)getStreamDenoise(stream);
	res["smoothd"].act = getStreamSmoothDenoise(stream);
	res["edged"].act = getStreamEdgeDenoise(stream);

	deleteStream(stream);
	closeStreamReceiver(r_port);

	setCameraConnection(cam, false, 10);

	disconnectFromCameraServer();

	cout << "\t" << "exp\t" << "act\t" << "rc\t" << endl;
	map<string, result>::iterator it = res.begin();
	while (it != res.end())
	{
		cout << it->first << "\t"
			 << it->second.exp << "\t"
			 << it->second.act << "\t"
			 << it->second.rc << "\t"
			 << (it->second.rc ? ((abs(it->second.exp - it->second.act) < 0.01) ? "pass" : "fail") : "n/a")
			 << endl;
		if(act_res && it->second.rc) act_res = abs(it->second.exp - it->second.act) < 0.01;
		it++;
	}

    Env::tearDown();

    return 0;
}

