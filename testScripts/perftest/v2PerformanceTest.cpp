#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <map>
#include <iterator>
#include <cmath>
#include <string>
#include <cstring>
#include <sstream>
#include <vector>
#include <iostream>

#include "mantis/MantisAPI.h"

using namespace std;

bool isCounting = false;
vector<FRAME> frames;

void newCameraCallback(ACOS_CAMERA mcam, void* data)
{
    ACOS_CAMERA* _mcam = (ACOS_CAMERA*) data;
    *_mcam = mcam;
}

void frameCallback(FRAME frame, void* data)
{
    if (isCounting) {
        frames.push_back(frame);
        if ((frame.m_metadata.m_timestamp - frames[0].m_metadata.m_timestamp) > 1e6 ) isCounting = false;
    }
}

string exec(string cmd) {
    FILE *popen_result;
    char buff[128];
    popen_result = popen(cmd.c_str(), "r");

    ostringstream ss;
    if (popen_result) {
        while (fgets(buff, sizeof(buff), popen_result) != NULL) {
            ss << buff;
        }
        pclose(popen_result);
    }

    return ss.str();
}

struct result{
    int mhz;
    int num_of_frames;
};

int main(int argc, char * argv[])
{
    char ip[24] = "127.0.0.1";
    int port = 9999;
    int r_port = 13013;

    connectToCameraServer(ip, port);

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

    STREAM_PROFILE profile;
    profile.videoSource.width = 3840;
    profile.videoSource.height = 2144;
    profile.videoEncoder.width = 1920;
    profile.videoEncoder.height = 1080;
    profile.videoEncoder.quality = 4;
    profile.videoEncoder.sessionTimeout = 10;
    profile.videoEncoder.framerate = 30;
    profile.videoEncoder.encodingInterval = 50;
    profile.videoEncoder.bitrateLimit = 2048;
    strcpy(profile.videoEncoder.encoding, V2_ENCODE_JPEG);

    FRAME_CALLBACK fcb;
    fcb.f = frameCallback;
    fcb.data = {};

    ACOS_STREAM stream = createLiveStream( cam, profile );
    initStreamReceiver( fcb, stream, r_port, 2.0 );

    setStreamGoLive( stream );
    sleep(1);

    string basePath = "/sys/devices/system/cpu/";

    string cmd;
    cmd = "sudo cat " + basePath + "cpu0/cpufreq/cpuinfo_min_freq";
    int min = atoi( exec(cmd).c_str() ) / 1000;
    cmd = "sudo cat " + basePath + "cpu0/cpufreq/cpuinfo_max_freq";
    int max = atoi( exec(cmd).c_str() ) / 1000;

    int step = floor(max - min) / 5;
    map<int, vector<result> > res;
    cmd = "nproc";
    int num_of_cores = atoi( exec(cmd).c_str() );
    for (int i = num_of_cores; i > 0; i--) {
        int mhz = max;
        while(mhz >= min) {
            ostringstream sscmd;
            sscmd << "sudo cpufreq-set --min " << (mhz - 50) << "MHz --max " << mhz << "MHz --governor performance";
            exec(sscmd.str());
            sleep(0.5);

            isCounting = true;
            while (isCounting) sleep(0.5);
            res[i].push_back({mhz, frames.size() - 2});
            frames.clear();

            mhz -= step;
        }

        ostringstream sscmd;
        sscmd << "echo 0 | sudo tee /sys/devices/system/cpu/cpu" << (i - 1) << "/online";
        exec(sscmd.str());
    }

    for (int i = 1; i < num_of_cores; i++) {
        ostringstream sscmd;
        sscmd << "echo 1 | sudo tee /sys/devices/system/cpu/cpu" << i << "/online";
        exec(sscmd.str());
    }

    ostringstream sscmd;
    sscmd << "sudo cpufreq-set --min " << max << "MHz --max " << max << "MHz --governor performance";
    exec(sscmd.str());

    deleteStream(stream);

    closeStreamReceiver(r_port);

    setCameraConnection(cam, false, 10);

    disconnectFromCameraServer();

    cout << "cores\t" << "mhz\t" << "frames\t" << endl;

    map<int, vector<result> >::iterator it = res.begin();
    while (it != res.end())
    {
        for (int i = 0; i < it->second.size(); i++){
            cout << it->first << "\t" << it->second[i].mhz << "\t" << it->second[i].num_of_frames << "\t" << endl;
        }
        cout << endl;
        it++;
    }
}
