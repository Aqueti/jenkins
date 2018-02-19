#ifndef MANTISAPITEST_H
#define MANTISAPITEST_H

#include <cstring>
#include <string>
#include <sstream>
#include <fstream>
#include <time.h>
#include <sys/time.h>
#include <sys/stat.h>
#include <cmath>
#include <map>
#include <list>
#include <vector>
#include <iterator>
#include <exception>

#include "gtest/gtest.h"
#include "mantis/MantisAPI.h"

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

int cnt_err(bool p);
string exec(string cmd);
uint64_t getCurrentTimestamp();
bool fileExists( const std::string &Filename );

class TestParams {
public:
    char *ip;
    char *mc_ip;
    uint16_t port;
    uint16_t mc_port;
    uint16_t r_port;
    uint16_t mcamID;
    uint32_t numCams;
    uint32_t camID;
    uint32_t numMCams;
    uint32_t duration;
    uint16_t num_of_mcams;
    ACOS_CAMERA cam;
    MICRO_CAMERA mcam;
    MICRO_CAMERA *mcamList;
    VIDEO_SOURCE videoSource;
    VIDEO_ENCODER videoEncoder;
    STREAM_PROFILE profile;
    ACOS_STREAM astream;
    ACOS_CLIP clip;
    ACOS_CLIP del_clip;
    ACOS_CLIP* clipList;
	FRAME frame;
	ACOS_PTZ_VELOCITY ptz_vel;
	ACOS_PTZ_ABSOLUTE ptz_abs;
	AtlWhiteBalance wb;
	AtlCompressionParameters cp;
    string storage_path;
    string cam_folder;
    string env_type;
    string tegra_user;
    char mode[10];

    TestParams();

    ~TestParams();
};

class MantisAPITest : public ::testing::Test, public TestParams
{
  protected:
    virtual void SetUp();
    virtual void TearDown();
};

class MantisAPITest_B : public ::testing::Test, public TestParams
{
  protected:
	virtual void SetUp();
    virtual void TearDown();
};

class MantisAPITest_N : public ::testing::Test, public TestParams
{
  protected:
	virtual void SetUp();
    virtual void TearDown();
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

class MantisAPITest_mlstream : public MantisAPITest_camconn
{
  protected:
    virtual void SetUp();
    virtual void TearDown();
};

class MantisAPITest_mcamconn : public ::testing::Test, public TestParams
{
  protected:
    virtual void SetUp();
    virtual void TearDown();
};

class MantisAPITest_mcamlstream : public MantisAPITest_mcamconn
{
  protected:
    virtual void SetUp();
    virtual void TearDown();
};

class acosd {
public:
  static void start(string tegra_user, char* mc_ip, char* mode);
  static void stop(string tegra_user, char* mc_ip);
  static void restart(string tegra_user, char* mc_ip, char* mode);
};

class V2 {
public:
  static void start(uint16_t camID, string storage_path);
  static void stop();
  static void restart(uint16_t camID, string storage_path);
};

#endif
