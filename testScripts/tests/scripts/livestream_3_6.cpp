/**
* Checking:
* box zoom
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

struct CoordsO {
    double x;
    double y;
    double hw;
};

struct CoordsE {
    double theta;
    double phi;
    double rho;
};

struct Result {
    CoordsO xyw;
    CoordsE tpr;
};

int main(int argc, char * argv[])
{
    Env::setUp("livestream_3_6");

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

    map<string, vector<Result> > res;

    ACOS_NORMALIZED_BOX box = { 0.5, 0.5, 0.5 };

    string c_arr[] = {"x", "y", "hw"};
    for(int i = 0; i < sizeof(c_arr)/sizeof(c_arr[0]); i++) {
        double step = 0.5;     
        while(step >= 0.05) {    
            setStreamBoxZoom( stream, box );
            sleep(1);

            res[c_arr[i]].push_back({{box.x, box.y, box.halfWidth},
                                     {frame.m_metadata.m_position.m_theta, frame.m_metadata.m_position.m_phi, frame.m_metadata.m_position.m_rho}});
        
            step -= 0.05;
            if (c_arr[i] == "x") box.x = step;
            else if (c_arr[i] == "y") box.y = step;
            else box.halfWidth = step;       
        }
        box = { 0.5, 0.5, 0.5 };       
    }

    closeStreamReceiver(r_port);
    deleteStream(stream);

    setCameraConnection(cam, false, 10);

    disconnectFromCameraServer();

    bool act_res = true;

    cout << "\t" << "x\t" << "theta\t" << "y\t" << "phi\t" << "hw\t"  << "rho\t" << endl;
  
    map<string, vector<Result> >::iterator it = res.begin();
    while (it != res.end())
    { 
        int last_ind = it->second.size() - 1;
        act_res = (it->first == "x" ?  (it->second[0].tpr.theta != it->second[last_ind].tpr.theta && it->second[0].tpr.phi == it->second[last_ind].tpr.phi && it->second[0].tpr.rho == it->second[last_ind].tpr.rho) :
                  (it->first == "y" ?  (it->second[0].tpr.theta == it->second[last_ind].tpr.theta && it->second[0].tpr.phi != it->second[last_ind].tpr.phi && it->second[0].tpr.rho == it->second[last_ind].tpr.rho) :
                  (it->first == "hw" ? (it->second[0].tpr.theta == it->second[last_ind].tpr.theta && it->second[0].tpr.phi == it->second[last_ind].tpr.phi && it->second[0].tpr.rho != it->second[last_ind].tpr.rho) : false)));
        cout << setprecision(2)        
             << it->first << "\t"
             << it->second[0].xyw.x << "\t"           
             << it->second[0].tpr.theta << "\t" 
             << it->second[0].xyw.y << "\t"
             << it->second[0].tpr.phi << "\t"
             << it->second[0].xyw.hw  << "\t"
             << it->second[0].tpr.rho << "\t"
             << (act_res ? "pass" : "fail")
             << endl;
        it++;
    }

    Env::tearDown();

    return 0;
}
