/**
 * Checking:
 * PTZ relative positioning
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

int main(int argc, char * argv[])
{
    Env::setUp("livestream_3_5");

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

    int num_of_steps = 10;

    ACOS_PTZ_VELOCITY vptz;
    vptz.pan_per_second = 2;
    vptz.tilt_per_second = 2;
    vptz.zoom_per_second = 1.3;

    FRAME p_frame;

    setStreamPTZAbsolute( stream, {1, 1, 1} );
    for (int i = 1; i <= num_of_steps; i++) {
    	p_frame = frame;
        setStreamPTZVelocity(stream, vptz);
        sleep(1);
        res[i].exp.theta = p_frame.m_metadata.m_position.m_theta + vptz.pan_per_second;
        res[i].act.theta = frame.m_metadata.m_position.m_theta;
        res[i].delta.theta = abs(res[i].act.theta - res[i].exp.theta) < 0.01 ? 0 : abs(res[i].act.theta - res[i].exp.theta);
        res[i].exp.phi = p_frame.m_metadata.m_position.m_phi + vptz.tilt_per_second;
        res[i].act.phi = frame.m_metadata.m_position.m_phi;
        res[i].delta.phi = abs(res[i].act.phi - res[i].exp.phi) < 0.01 ? 0 : abs(res[i].act.phi - res[i].exp.phi) ;
        res[i].exp.rho = p_frame.m_metadata.m_position.m_rho * vptz.zoom_per_second;
        res[i].act.rho = frame.m_metadata.m_position.m_rho;
        res[i].delta.rho = abs(res[i].act.rho - res[i].exp.rho) < 0.01 ? 0 : abs(res[i].act.rho - res[i].exp.rho);
    };

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
             << ((it->second.delta.theta < 1 && it->second.delta.rho < 1 && it->second.delta.phi < 1) ? "pass" : "fail")
             << endl;
        if (act_res) act_res = (it->second.delta.theta < 1 && it->second.delta.rho < 1 && it->second.delta.phi < 1);
        it++;
    }

    Env::tearDown();

    return 0;
}
