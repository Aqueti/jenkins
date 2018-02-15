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

TestParams::TestParams() {
    ip = "127.0.0.1";
    port = 9999;
    mc_port = 9999;
    r_port = 14014;
    numCams = 1;
    //if (string(getenv("ENV_TYPE")) == "TX1-old")
    mc_ip = "192.168.168.1"; //depends
    mcamID = 11; //depends
    camID = 19; // depends
    numMCams = 2; //depends
    duration = 5;
    num_of_mcams = 2;

    fname  = "clipList.txt";
    model_file = "model.json";
    clip_model_file = "clip_model.json";

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

    profile = {
      videoSource,
      videoEncoder
    };

    cam = {};
    mcam = {};
    astream = {};
    clip = {};
	frame = {};
	ptz_vel = {};
	ptz_abs = {};
	wb = {};
	cp = {};
}

TestParams::~TestParams() {

}

void MantisAPITest::SetUp() {
	tp = new TestParams();

	if (isConnectedToCameraServer() != AQ_SERVER_CONNECTED) {
		connectToCameraServer("127.0.0.1", 9999);
	}

	NEW_CAMERA_CALLBACK camCB;
	camCB.f = newCameraCallback;
	camCB.data = &tp->cam;
	setNewCameraCallback(camCB);
}

void MantisAPITest::TearDown()
{
	disconnectFromCameraServer();

	cout << "height$$$$ " << tp->profile.videoEncoder.height << endl;

	delete tp;
}

void MantisAPITest_B::SetUp() {
	tp = new TestParams();
}

void MantisAPITest_B::TearDown() {
	delete tp;
}

void MantisAPITest_N::SetUp() {
	tp = new TestParams();

	tp->ip = "127.0.0.127";
	tp->port = 8888;
	tp->mc_ip = "192.168.168.192";
	tp->mc_port = 8888;
	tp->model_file = "";
	tp->clip_model_file = "";
}

void MantisAPITest_N::TearDown()
{
	delete tp;
}

void MantisAPITest_camconn::SetUp() {
    MantisAPITest::SetUp();

    if(isCameraConnected(tp->cam) != AQ_CAMERA_CONNECTED) {
        setCameraConnection(tp->cam, true, 10);
    }

    fillCameraMCamList(&tp->cam);
}

void MantisAPITest_camconn::TearDown() {
    if(isCameraConnected(tp->cam) == AQ_CAMERA_CONNECTED) {
       setCameraConnection(tp->cam, false, 10);
    }

    MantisAPITest::TearDown();
}

void MantisAPITest_lstream::SetUp() {
    MantisAPITest_camconn::SetUp();

	FRAME_CALLBACK fcb;
	fcb.f = frameCallback;
	fcb.data = &tp->frame;

	setCameraReceivingData(tp->cam, true, 5);
    tp->astream = createLiveStream( tp->cam, tp->profile ); //requires model file
    initStreamReceiver( fcb, tp->astream, tp->r_port, 5.0 );
    setStreamGoLive( tp->astream );

    sleep(2);
}

void MantisAPITest_lstream::TearDown() {
    deleteStream(tp->astream);
    closeStreamReceiver(tp->r_port);
    setCameraReceivingData(tp->cam, false, 5);

    MantisAPITest_camconn::TearDown();
}

void MantisAPITest_mlstream::SetUp() {
    MantisAPITest_camconn::SetUp();

	FRAME_CALLBACK fcb;
	fcb.f = frameCallback;
	fcb.data = &tp->frame;

	setCameraReceivingData(tp->cam, true, 5);
	tp->astream = createMCamStream( tp->cam, tp->cam.mcamList.mcams[0] );
	initStreamReceiver( fcb, tp->astream, tp->r_port, 2.0 );
}

void MantisAPITest_mlstream::TearDown() {
    deleteStream(tp->astream);
    closeStreamReceiver(tp->r_port);
    setCameraReceivingData(tp->cam, false, 5);

    MantisAPITest_camconn::TearDown();
}

void MantisAPITest_cstream::SetUp() {
    MantisAPITest_camconn::SetUp();

    ACOS_CLIP* recordingList;

    setCameraReceivingData(tp->cam, true, 5);
	if (requestStoredRecordings( &recordingList ) == 0) {
		setCameraRecording(tp->cam , true, 5);
		sleep(tp->duration);
		setCameraRecording(tp->cam , false, 5);

		requestStoredRecordings( &recordingList );
	}

	FRAME_CALLBACK fcb;
	fcb.f = frameCallback;
	fcb.data = &tp->frame;

	tp->astream = createClipStream(recordingList[0], tp->profile);
	initStreamReceiver( fcb, tp->astream, tp->r_port, 2.0 );
	setStreamPlaySpeed(tp->astream, 1.0);
}

void MantisAPITest_cstream::TearDown() {
    deleteStream(tp->astream);
    closeStreamReceiver(tp->r_port);
    setCameraReceivingData(tp->cam, false, 5);

    MantisAPITest_camconn::TearDown();
}

void MantisAPITest_mcamconn::SetUp() {
	tp = new TestParams();

	if (getNumberOfMCams() == 0) {
		mCamConnect(tp->mc_ip, tp->mc_port);
	}

    NEW_MICRO_CAMERA_CALLBACK mcamCB;
    mcamCB.f = newMCamCallback;
    mcamCB.data = &tp->mcamList;
    setNewMCamCallback(mcamCB);

    tp->mcam = tp->mcamList[0];
}

void MantisAPITest_mcamconn::TearDown() {
	mCamDisconnect(tp->mc_ip, tp->mc_port);

	delete tp;
}

void MantisAPITest_mcamlstream::SetUp() {
	MICRO_CAMERA_FRAME_CALLBACK frameCB;
	frameCB.f = mcamFrameCallback;
	frameCB.data = &tp->frame;
	setMCamFrameCallback(frameCB);

	initMCamFrameReceiver(tp->r_port, 1.0);
	startMCamStream(tp->mcam, tp->r_port);
}

void MantisAPITest_mcamlstream::TearDown() {
	stopMCamStream(tp->mcam, tp->r_port);
	closeMCamFrameReceiver(tp->r_port);

	MantisAPITest_mcamconn::TearDown();
}

