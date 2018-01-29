/**
 * Checking:
 * PTZ absolute positioning
 * 
 **/

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

struct Coords {
	double theta;
	double phi;
	double rho;
};

struct Result {
	Coords exp;
	Coords act;
	Coords delta;
};

struct Data {
	AtlRange_64f range;
	double step;
	double c_step;
};

int main(int argc, char * argv[])
{
	Env::setUp("livestream_3_4");

    ACOS_CAMERA cam;
    NEW_CAMERA_CALLBACK camCB;
    camCB.f = newCameraCallback;
    camCB.data = &cam;
    setNewCameraCallback(camCB);

    connectToCameraServer(v2_ip, port);

    if( isCameraConnected(cam) != AQ_CAMERA_CONNECTED ){
        setCameraConnection(cam, true, 10);
    }

    fillCameraMCamList(&cam);

    FRAME frame;
    FRAME_CALLBACK fcb;
    fcb.f = frameCallback;
    fcb.data = &frame;

    ACOS_STREAM stream = createLiveStream( cam, profile );
    initStreamReceiver(fcb, stream, r_port, 2.0);
    setStreamGoLive( stream );
    sleep(2);

    map<int, Result> res;
    map<string, Data> data;

	int num_of_steps = 10;

    data["pan"].range = getStreamPanRange( stream );
    data["tilt"].range = getStreamTiltRange( stream );
    data["zoom"].range = getStreamZoomRange( stream );

	data["pan"].step = (data["pan"].range.max - data["pan"].range.min) / num_of_steps;
    data["tilt"].step = (data["tilt"].range.max - data["tilt"].range.min) / num_of_steps;
    data["zoom"].step = (data["zoom"].range.max - data["zoom"].range.min) / num_of_steps;

	data["pan"].c_step = data["pan"].range.min;
	data["tilt"].c_step = data["tilt"].range.min;
	data["zoom"].c_step = data["zoom"].range.max;
	for (int i = 0; i <= num_of_steps; i++) {
		res[i].exp.theta = data["pan"].c_step;
		res[i].exp.phi = data["tilt"].c_step;
		res[i].exp.rho = data["zoom"].c_step;

		setStreamPTZAbsolute( stream, {res[i].exp.theta, res[i].exp.phi, res[i].exp.rho} );
		sleep(1);

		res[i].act.theta = frame.m_metadata.m_position.m_theta;
		res[i].act.phi = frame.m_metadata.m_position.m_phi;
		res[i].act.rho = frame.m_metadata.m_position.m_rho;

		res[i].delta.theta = abs(res[i].act.theta - res[i].exp.theta) < 0.001 ? 0 : abs(res[i].act.theta - res[i].exp.theta);
		res[i].delta.phi = abs(res[i].act.phi - res[i].exp.phi) < 0.001 ? 0 : abs(res[i].act.phi - res[i].exp.phi);
		res[i].delta.rho = abs(res[i].act.rho - res[i].exp.rho) < 0.001 ? 0 : abs(res[i].act.rho - res[i].exp.rho);

		data["pan"].c_step += data["pan"].step;
		data["tilt"].c_step += data["tilt"].step;
		data["zoom"].c_step -= data["zoom"].step;
	}

    closeStreamReceiver(r_port);
    deleteStream(stream);

    setCameraConnection(cam, false, 10);

    disconnectFromCameraServer();

	cout << "\t" << "exp_t\t" << "act_t\t" << "delta\t" << "exp_phi\t" << "act_phi\t"  << "delta\t"  << "exp_rho\t" << "act_rho\t"  << "delta\t" << endl;

    map<int, Result>::iterator it = res.begin();
	while (it != res.end())
	{
		cout << setprecision(4)
			 << it->first << "\t"
			 << it->second.exp.theta << "\t"
			 << it->second.act.theta << "\t"
			 << it->second.delta.theta << "\t"
			 << it->second.exp.phi << "\t"
			 << it->second.act.phi << "\t"
			 << it->second.delta.phi << "\t"
			 << it->second.exp.rho  << "\t"
			 << it->second.act.rho << "\t"
			 << it->second.delta.rho << "\t"
			 << ((it->second.delta.theta == 0 && it->second.delta.rho == 0) ? "pass" : "fail")
			 << endl;
		if (act_res) act_res = (it->second.delta.theta == 0 && it->second.delta.rho == 0);
		it++;
	}

	Env::tearDown();

    return 0;
}
