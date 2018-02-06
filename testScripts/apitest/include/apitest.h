#ifndef MANTISAPITEST_H
#define MANTISAPITEST_H

#include <fstream>
#include <string>
#include <sstream>
#include <cstring>
#include <time.h>
#include <sys/time.h>
#include <sys/stat.h>
#include <cmath>
#include <map>
#include <list>
#include <vector>
#include <iterator>

#include "mantis/MantisAPI.h"
#include "gtest/gtest.h"

using namespace std;

void newCameraCallback(ACOS_CAMERA cam, void* data);
void newMCamCallback(MICRO_CAMERA mcam, void* data);
void newFrameCallback(FRAME frame, void* data);
void newClipCallback(ACOS_CLIP clip, void* data);
void mcamFrameCallback(FRAME frame, void* data);
void cameraDeletedCallback(uint32_t camId, void* data);
void cameraPropertyCallback(ACOS_CAMERA cam, void* data, int16_t o, int16_t n);
void newConnectedToServerCallback(void* data, AQ_SYSTEM_STATE o, AQ_SYSTEM_STATE n);
void latestTimeCallback(ACOS_CAMERA cam, void* data, uint64_t o, uint64_t n);
void frameCallback(FRAME frame, void* data);
void deletedClipCallback(ACOS_CLIP clip, void* data);
void mcamPropertyCallback(MICRO_CAMERA mcam, void* data, bool o, bool n);
uint64_t getCurrentTimestamp();
bool fileExists( const std::string &Filename );

class TestParams {
public:
    TestParams() {
        ip = "127.0.0.1";
        port = 9999;
        mc_ip = "192.168.10.1";
        mc_port = 9999;
        r_port = 11000;
        mcamID = 2;
        numCams = 1;
        camID = 11;
        numMCams = 2;
        model_file = "model.json";
        clip_model_file = "clip_model.json";

        fname = "clipList.txt";
        profile.videoSource.width = 3840;
        profile.videoSource.height = 2144;
        profile.videoEncoder.width = 1920;
        profile.videoEncoder.height = 1080;
        profile.videoEncoder.quality = 4;
        profile.videoEncoder.sessionTimeout = 10;
        profile.videoEncoder.framerate = 30;
        profile.videoEncoder.encodingInterval = 50;
        profile.videoEncoder.bitrateLimit = 2048;
        strcpy(profile.videoEncoder.encoding, "H264");
    }

    ~TestParams() {

    }

    char *ip;
    char *mc_ip;
    uint16_t port;
    uint16_t mc_port;
    uint16_t r_port;
    uint16_t mcamID;
    uint32_t numCams;
    uint32_t camID;
    uint32_t numMCams;
    ACOS_CAMERA cam;
    MICRO_CAMERA mcam;
    STREAM_PROFILE profile;
    ACOS_STREAM astream;
    char *fname;
    char *model_file;
    char *clip_model_file;
};

class MantisAPITest : public ::testing::Test
{
protected:
    virtual void SetUp();
    virtual void TearDown();

    TestParams *tp;
};

class MantisAPITest_camconn : public MantisAPITest
{
  protected:
    virtual void SetUp();
    virtual void TearDown();
};

class MantisAPITest_lstream : public MantisAPITest_camconn
{
  protected:
    virtual void SetUp();
    virtual void TearDown();
};

class MantisAPITest_cstream : public MantisAPITest_camconn
{
  protected:
    virtual void SetUp();
    virtual void TearDown();
};

class MantisAPITest_mcamconn : public ::testing::Test
{
  protected:
    virtual void SetUp();
    virtual void TearDown();

    TestParams *tp;
};

class MantisAPITest_N : public ::testing::Test
{
  protected:
	MantisAPITest_N() {
		n_ip = "127.0.0.1";
		ip = "127.0.0.127";
		n_port = 9999;
		port = 8888;
		r_port = 12000;
		mc_ip = "192.168.0.1";
		mc_port = 8888;
		model_file = "";
		clip_model_file = "";
	}

	virtual void SetUp() {}

    virtual void TearDown() {}

    char *n_ip;
    char *ip;
    char *mc_ip;
    uint16_t n_port;
    uint16_t port;
    uint16_t r_port;
    uint16_t mc_port;

    ACOS_CAMERA cam;
    MICRO_CAMERA mcam;
    ACOS_STREAM astream;
    STREAM_PROFILE profile;
    ACOS_CLIP clip;
    FRAME frame;
    FRAME_CALLBACK fCB;
    ACOS_PTZ_VELOCITY vel;
    ACOS_PTZ_ABSOLUTE abs;
    AtlWhiteBalance wb;
    AtlCompressionParameters cp;
    char *model_file;
    char *clip_model_file;
};

#endif
