#include "apitest.h"

void newCameraCallback(ACOS_CAMERA cam, void* data)
{
    ACOS_CAMERA* _cam = (ACOS_CAMERA*) data;
    *_cam = cam;
}

void newMCamCallback(MICRO_CAMERA mcam, void* data)
{
	static int i = 0;
	MICRO_CAMERA* _mcam = (MICRO_CAMERA*) data;
    _mcam[i++] = mcam;
}

void newClipCallback(ACOS_CLIP clip, void* data)
{
    ACOS_CLIP* _clip = (ACOS_CLIP*) data;
    *_clip = clip;
}

void mcamFrameCallback(FRAME frame, void* data)
{
    FRAME* _frame = (FRAME*) data;
    *_frame = frame;
}

void cameraDeletedCallback(uint32_t camId, void* data)
{
	uint32_t* _res = (uint32_t*)data;
    *_res = camId;
}

void cameraPropertyCallback(ACOS_CAMERA cam, void* data, int16_t o, int16_t n)
{
	ACOS_CAMERA* _cam = (ACOS_CAMERA*) data;
    *_cam = cam;
}

void newConnectedToServerCallback(void* data, AQ_SYSTEM_STATE o, AQ_SYSTEM_STATE n)
{
	AQ_SYSTEM_STATE* _res = (AQ_SYSTEM_STATE*)data;
    *_res = n;
}

void latestTimeCallback(ACOS_CAMERA cam, void* data, uint64_t o, uint64_t n) {
    ACOS_CAMERA* _cam = (ACOS_CAMERA*) data;
    *_cam = cam;
}

void frameCallback(FRAME frame, void* data)
{
    FRAME* _frame = (FRAME*) data;
    *_frame = frame;
}

void deletedClipCallback(ACOS_CLIP clip, void* data) {
    ACOS_CLIP* _clip = (ACOS_CLIP*) data;
    *_clip = clip;
}

void mcamPropertyCallback(MICRO_CAMERA mcam, void* data, bool o, bool n)
{
	MICRO_CAMERA* _mcam = (MICRO_CAMERA*) data;
    *_mcam = mcam;
}

string readFromFile(const char* file_name) {
  ostringstream ss;
  ifstream fin(file_name);
  if (fin.is_open()) {
    string str;
    ifstream fin(file_name);

    while (getline(fin, str)) {
        ss << str << endl;
    }
    fin.close();
  }

  return ss.str();
};

string exec(string cmd) {
  FILE *popen_result;
  char buff[512];
  popen_result = popen(cmd.c_str(), "r");

  ostringstream ss;

	if (popen_result) {
		while (fgets(buff, sizeof(buff), popen_result) != NULL) {
			ss << buff;
		}
	}

  pclose(popen_result);

  return ss.str();
};

uint64_t getCurrentTimestamp()
{
   struct timeval tv;
   gettimeofday(&tv,NULL);

   double dtime = tv.tv_sec + tv.tv_usec/1e6;

   return dtime;
}

bool fileExists( const std::string &Filename )
{
    return access( Filename.c_str(), 0 ) == 0;
}

int cnt_err(bool p = false)
{
    static int i = 0;
    if (!p) return i;
    else return i++;
}

TestParams::TestParams() {
    ip = "127.0.0.1";
    port = 9999;
    mc_port = 9999;
    r_port = 14014;
    numCams = 1;
    duration = 5;
    num_of_mcams = 2;
    file_name = "/home/jenkins/tegra.txt";

    tegra_type = fileExists(file_name) ? readFromFile(file_name.c_str()) : "TX1";

    if(tegra_type == "TX1") {
        camID = 102;
        mcamID = 11;
        mc_ip = "192.168.10.1";
        numMCams = 2;
        tegra_user = "nvidia";
    } else if (tegra_type == "TX2") {
        camID = 103;
        mcamID = 111;
        mc_ip = "192.168.10.11";
        numMCams = 2;
        tegra_user = "nvidia";
    } else {
        camID = 19;
        mcamID = 91;
        mc_ip = "192.168.10.9";
        numMCams = 2;
        tegra_user = "ubuntu";
    }

    cam_folder = "/etc/aqueti/mantis_" + camID;
    storage_path =  string(getenv("HOME")); //"/mnt/ssd_e";

    videoSource = {
      1920, //width
      1080  //height
    };
    videoEncoder = {
      1920, //width
      1080, //height
      4,    //quality
      10,   //sessionTimeout
      30,   //framerate
      50,   //encodingInterval
      2048 //bitrateLimit
       	   //encoding
    };
    strcpy(videoEncoder.encoding, V2_ENCODE_H264);
    strcpy(mode, V2_ENCODE_H264);

    profile = {
    	videoSource,
    	videoEncoder
    };

    ptz_vel = {1.0, //pan_per_second
    		   1.0, //tilt_per_second
    		   1.0  //zoom_per_second
    };

    ptz_abs = {1.0, //pan_degrees
			   1.0, //tilt_degrees
			   1.0  //zoom_factor
	};

    cam = {};
    mcam = {};
    astream = {};
    clip = {};
    del_clip = {};
	frame = {};
	wb = {};
	cp = {};
}

TestParams::~TestParams() {

}

void MantisAPITest::SetUp() {
    while(isConnectedToCameraServer() != AQ_SERVER_CONNECTED) {
        if (cnt_err() >= 3) FAIL();

        connectToCameraServer(ip, port);

        if (isConnectedToCameraServer() != AQ_SERVER_CONNECTED) {
            cnt_err(true);

            V2::stop();
            acosd::restart(tegra_user, mc_ip, mode);
            V2::start(camID, storage_path);
        }
    }    	
	
	NEW_CAMERA_CALLBACK camCB;
	camCB.f = newCameraCallback;
	camCB.data = &cam;
	setNewCameraCallback(camCB);
}

void MantisAPITest::TearDown()
{
    try {
        if(isConnectedToCameraServer() == AQ_SERVER_CONNECTED) {
            disconnectFromCameraServer();
        }        
    } catch (exception e) {}
}

void MantisAPITest_B::SetUp() {

}

void MantisAPITest_B::TearDown() {

}

void MantisAPITest_N::SetUp() {
	ip = "127.0.0.127";
	port = 8888;
	mc_ip = "192.168.168.192";
	mc_port = 8888;
}

void MantisAPITest_N::TearDown()
{

}

void MantisAPITest_camconn::SetUp() {
    MantisAPITest::SetUp();

    if(isCameraConnected(cam) != AQ_CAMERA_CONNECTED) {
        setCameraConnection(cam, true, 10);      
    }

    fillCameraMCamList(&cam);
}

void MantisAPITest_camconn::TearDown() {
    try {
        if(isConnectedToCameraServer() == AQ_SERVER_CONNECTED && 
           isCameraConnected(cam) == AQ_CAMERA_CONNECTED) {
                setCameraConnection(cam, false, 10);
        }
    } catch (exception e) {}
    

    MantisAPITest::TearDown();
}

void MantisAPITest_lstream::SetUp() {
    MantisAPITest_camconn::SetUp();

	FRAME_CALLBACK fcb;
	fcb.f = frameCallback;
	fcb.data = &frame;

	setCameraReceivingData(cam, true, 5);
    astream = createLiveStream( cam, profile ); //requires model file   
    initStreamReceiver( fcb, astream, r_port, 5.0 );
    setStreamGoLive( astream );

    sleep(2);
}

void MantisAPITest_lstream::TearDown() {
    try {
         if(isConnectedToCameraServer() == AQ_SERVER_CONNECTED && 
            isCameraConnected(cam) == AQ_CAMERA_CONNECTED) {
                deleteStream(astream);
                closeStreamReceiver(r_port);
                setCameraReceivingData(cam, false, 5);
        }
    } catch (exception e) {} 

    MantisAPITest_camconn::TearDown();   
}

void MantisAPITest_mlstream::SetUp() {
    MantisAPITest_camconn::SetUp();

	FRAME_CALLBACK fcb;
	fcb.f = frameCallback;
	fcb.data = &frame;

	setCameraReceivingData(cam, true, 5);
	astream = createMCamStream( cam, cam.mcamList.mcams[0] );
	initStreamReceiver( fcb, astream, r_port, 2.0 );
}

void MantisAPITest_mlstream::TearDown() {
    try {
        if(isConnectedToCameraServer() == AQ_SERVER_CONNECTED && 
           isCameraConnected(cam) == AQ_CAMERA_CONNECTED) {
                deleteStream(astream);
                closeStreamReceiver(r_port);
                setCameraReceivingData(cam, false, 5);
        }
    } catch (exception e) {}

    MantisAPITest_camconn::TearDown();
}

void MantisAPITest_cstream::SetUp() {
    MantisAPITest_camconn::SetUp();

    ACOS_CLIP* recordingList;

    setCameraReceivingData(cam, true, 5);
	if (requestStoredRecordings( &recordingList ) == 0) {
		setCameraRecording(cam , true, 5);
		sleep(duration);
		setCameraRecording(cam , false, 5);

		requestStoredRecordings( &recordingList );
	}

	FRAME_CALLBACK fcb;
	fcb.f = frameCallback;
	fcb.data = &frame;

    ACOS_CLIP_CALLBACK clipCB;
    clipCB.f = newClipCallback;
    clipCB.data = &clip;
    setNewClipCallback(clipCB);

    ACOS_CLIP_CALLBACK deletedClipCB;
	deletedClipCB.f = deletedClipCallback;
	deletedClipCB.data = &del_clip;
	setClipDeletedCallback(deletedClipCB);

	astream = createClipStream(recordingList[0], profile);
	initStreamReceiver( fcb, astream, r_port, 2.0 );
	setStreamPlaySpeed(astream, 1.0);
}

void MantisAPITest_cstream::TearDown() {
    try {
        if(isConnectedToCameraServer() == AQ_SERVER_CONNECTED && 
           isCameraConnected(cam) == AQ_CAMERA_CONNECTED) {
                deleteStream(astream);
                closeStreamReceiver(r_port);
                setCameraReceivingData(cam, false, 5);
        }
    } catch (exception e) {}

    MantisAPITest_camconn::TearDown();
}

void MantisAPITest_mcamconn::SetUp() {
	if (getNumberOfMCams() == 0) {
		mCamConnect(mc_ip, mc_port);
	}

    NEW_MICRO_CAMERA_CALLBACK mcamCB;
    mcamCB.f = newMCamCallback;
    mcamCB.data = &mcamList;
    setNewMCamCallback(mcamCB);

    mcam = mcamList[0];
}

void MantisAPITest_mcamconn::TearDown() {
	mCamDisconnect(mc_ip, mc_port);
}

void MantisAPITest_mcamlstream::SetUp() {
	MICRO_CAMERA_FRAME_CALLBACK frameCB;
	frameCB.f = mcamFrameCallback;
	frameCB.data = &frame;
	setMCamFrameCallback(frameCB);

	initMCamFrameReceiver(r_port, 1.0);
	startMCamStream(mcam, r_port);
}

void MantisAPITest_mcamlstream::TearDown() {
	stopMCamStream(mcam, r_port);
	closeMCamFrameReceiver(r_port);

	MantisAPITest_mcamconn::TearDown();
}

void acosd::start(string tegra_user, char* mc_ip, char* mode) {
  ostringstream cmd;
  cmd << "ssh " << tegra_user << "@" << mc_ip << " 'acosd -R acosdLog -C " << mode << " -s 1'"; 
  cout << "~~~ " << cmd.str() << endl;
  exec(cmd.str());  
  sleep(3);
} 
void acosd::stop(string tegra_user, char* mc_ip) {
  ostringstream cmd;
  cmd << "ssh " << tegra_user << "@" << mc_ip << " 'pkill -9 acosd'";
  exec(cmd.str());
  sleep(1);
}
void acosd::restart(string tegra_user, char* mc_ip, char* mode) {
  acosd::stop(tegra_user, mc_ip);
  acosd::start(tegra_user, mc_ip, mode);
}

void V2::start(uint16_t camID, string storage_path) {
  ostringstream cmd;
  cmd << "V2 " 
      << "--cache-size 20000 " 
      << "--maxRecordingLength 3600 "
      << "--tightPrefetch "
      << "--force-gpu-compatibility "
      << "-p 24816 "
      << "--numJpegDecompressors 16 "
      << "--numH26XDecompressors 5 "
      << "--prefetchSize 40 "
      << "--dir " << storage_path << " " 
      << "--camera " << camID << " " 
      << "1>/dev/null &";
  exec(cmd.str());
  cout << "~~~ " << cmd.str() << endl;
  sleep(5);
}
void V2::stop() {
  string cmd = "pkill -9 V2";
  exec(cmd);
  sleep(1);
}
void V2::restart(uint16_t camID, string storage_path) {
  V2::stop();
  V2::start(camID, storage_path);
}