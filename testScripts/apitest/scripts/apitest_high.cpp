#include "apitest.h"

void newCameraCallback(ACOS_CAMERA cam, void* data)
{
    ACOS_CAMERA* _cam = (ACOS_CAMERA*) data;
    *_cam = cam;
}

void newMCamCallback(MICRO_CAMERA mcam, void* data)
{
    MICRO_CAMERA* _mcam = (MICRO_CAMERA*) data;
    *_mcam = mcam;
}

void newFrameCallback(FRAME frame, void* data)
{
    FRAME* _frame = (FRAME*) data;
    *_frame = frame;
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
    bool* _res = (bool *)data;
    *_res = true;
}

void cameraPropertyCallback(ACOS_CAMERA cam, void* data, int16_t o, int16_t n)
{
    ACOS_CAMERA* _cam = (ACOS_CAMERA*) data;
    *_cam = cam;
}

void newConnectedToServerCallback(void* data, AQ_SYSTEM_STATE o, AQ_SYSTEM_STATE n)
{
    bool* _res = (bool *)data;
    *_res = true;
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

void MantisAPITest::SetUp()
{
    tp = new TestParams();
    if (isConnectedToCameraServer() != 100) {
		connectToCameraServer(tp->ip, tp->port);
		if(isConnectedToCameraServer() != 100) {
			FAIL();
		}
    }

    NEW_CAMERA_CALLBACK camCB;
    camCB.f = newCameraCallback;
    camCB.data = &tp->cam;
    setNewCameraCallback(camCB);
}

void MantisAPITest::TearDown()
{
    delete tp;
    //disconnectFromCameraServer();
}

void MantisAPITest_camconn::SetUp() {
    MantisAPITest::SetUp();

    if(isCameraConnected(tp->cam) != 110) {
        setCameraConnection(tp->cam, true, 10);
        if (isCameraConnected(tp->cam) != 110) {
            FAIL();
        }
    }

    fillCameraMCamList(&tp->cam);

    MICRO_CAMERA *t_mcam = &tp->mcam;
    *t_mcam = tp->cam.mcamList.mcams[0];
}

void MantisAPITest_camconn::TearDown() {
    if(isCameraConnected(tp->cam) == 110) {
       // setCameraConnection(tp->cam, false, 10);
    }
    MantisAPITest::TearDown();
}

void MantisAPITest_lstream::SetUp() {
    MantisAPITest_camconn::SetUp();
    //requires model file
    tp->astream = createLiveStream( tp->cam, tp->profile );
}

void MantisAPITest_lstream::TearDown() {
    deleteStream(tp->astream);
    MantisAPITest_camconn::TearDown();
}

void MantisAPITest_cstream::SetUp() {
    MantisAPITest_camconn::SetUp();

    ACOS_CLIP* recordingList;
	requestStoredRecordings( &recordingList );

	tp->astream = createClipStream(recordingList[0], tp->profile); // MODEL FILE

    sleep(1);
}

void MantisAPITest_cstream::TearDown() {
    deleteStream(tp->astream);
    MantisAPITest_camconn::TearDown();
}

void MantisAPITest_mcamconn::SetUp() {
	tp = new TestParams();

	if (getNumberOfMCams() == 0) {
		mCamConnect(tp->mc_ip, tp->mc_port);
	}

	//initMCamFrameReceiver(tp->r_port, 1.0);

    NEW_MICRO_CAMERA_CALLBACK mcamCB;
    mcamCB.f = newMCamCallback;
    mcamCB.data = &tp->mcam;
    setNewMCamCallback(mcamCB);

    FRAME frame;
    MICRO_CAMERA_FRAME_CALLBACK frameCB;
	frameCB.f = mcamFrameCallback;
	frameCB.data = &frame;
    setMCamFrameCallback(frameCB);
}

void MantisAPITest_mcamconn::TearDown() {
	mCamDisconnect(tp->mc_ip, tp->mc_port);
	//closeMCamFrameReceiver(tp->r_port);
}
/*************************************************************
* Configuration and Setup
*************************************************************/

TEST_F(MantisAPITest_N, connectToCameraServer_P) {
	AQ_RETURN_CODE act_res = connectToCameraServer(n_ip, n_port);

	disconnectFromCameraServer();

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_N, connectToCameraServer_N) {
    AQ_RETURN_CODE act_res = connectToCameraServer(ip, port);

    EXPECT_NE(act_res, 0);
}

TEST_F(MantisAPITest_N, disconnectFromCameraServer_P) {
	connectToCameraServer(n_ip, n_port);

	AQ_RETURN_CODE act_res = disconnectFromCameraServer();

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_N, disconnectFromCameraServer_N) {
    AQ_RETURN_CODE act_res = disconnectFromCameraServer();

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest, isConnectedToCameraServer_P) {
	AQ_SYSTEM_STATE act_res = isConnectedToCameraServer();

    EXPECT_EQ(act_res, 100);
}

TEST_F(MantisAPITest_N, isConnectedToCameraServer_N) {
	AQ_SYSTEM_STATE act_res = isConnectedToCameraServer();

    EXPECT_EQ(act_res, 101);
}

TEST_F(MantisAPITest, setNewConnectedToServerCallback_B) {
    bool response = false;
    AQ_SYSTEM_STATE_CALLBACK sCB;
    sCB.f = newConnectedToServerCallback;
    sCB.data = &response;
    setNewConnectedToServerCallback(sCB);

    disconnectFromCameraServer();

    sleep(1);

    bool act_res = response;

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest, isCameraConnected_B) {
	AQ_SYSTEM_STATE act_res;

	setCameraConnection(tp->cam, true, 10);

	act_res = isCameraConnected(tp->cam);

	EXPECT_EQ(act_res, AQ_CAMERA_CONNECTED);

    setCameraConnection(tp->cam, false, 10);

    act_res = isCameraConnected(tp->cam);

    EXPECT_EQ(act_res, AQ_CAMERA_DISCONNECTED);
}

TEST_F(MantisAPITest, setCameraConnection_B) {
    setCameraConnection(tp->cam, true, 10);

    AQ_SYSTEM_STATE act_res;

    act_res = isCameraConnected(tp->cam);

    EXPECT_EQ(act_res, 110);

    setCameraConnection(tp->cam, false, 10);

    act_res = isCameraConnected(tp->cam);

    EXPECT_EQ(act_res, 111);
}

TEST_F(MantisAPITest, disconnectCamera_P) {
	disconnectCamera(tp->cam);

    AQ_SYSTEM_STATE act_res = isCameraConnected(tp->cam);

    EXPECT_EQ(act_res, 111);

    act_res = isConnectedToCameraServer();

    EXPECT_EQ(act_res, 101);
}

TEST_F(MantisAPITest_N, disconnectCamera_N) {
	AQ_SYSTEM_STATE act_res = isCameraConnected(cam);

    EXPECT_EQ(act_res, 999);
}

TEST_F(MantisAPITest, setNewCameraCallback_B) {
    bool act_res = (tp->cam.camID == tp->camID);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest, setCameraDeletedCallback_B) {
    bool response = false;
    CAMERA_DELETED_CALLBACK deletedCB;
    deletedCB.f = cameraDeletedCallback;
    deletedCB.data = &response;
    setCameraDeletedCallback(deletedCB);

    disconnectFromCameraServer();

    sleep(1);

    bool act_res = response;

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest, getNumberOfCameras_B) {
    uint32_t act_res = getNumberOfCameras();

    ASSERT_EQ(act_res, tp->numCams);
}

TEST_F(MantisAPITest_camconn, setCameraPropertyCallbacks_B) {
    CAMERA_CALLBACKS cbs;
    cbs.cameraConnectionCallback.f = cameraPropertyCallback;
    cbs.cameraConnectionCallback.data = &tp->cam;

    cbs.dataFlowStatusCallback.f = cameraPropertyCallback;
    cbs.dataFlowStatusCallback.data = &tp->cam;

    setCameraPropertyCallbacks(cbs);

    setCameraConnection(tp->cam, false, 10);

    sleep(1);

    bool act_res = (tp->cam.camID == tp->camID);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_camconn, getCameraNumberOfMCams_P) {
    uint32_t act_res = getCameraNumberOfMCams(tp->cam);
    EXPECT_EQ(act_res, tp->numMCams);
}

TEST_F(MantisAPITest_N, getCameraNumberOfMCams_N) {
    uint32_t act_res = getCameraNumberOfMCams(cam);
    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_camconn, getCameraMCamList_B) {
    MICRO_CAMERA *mcamList = tp->cam.mcamList.mcams;
    getCameraMCamList(tp->cam, mcamList, tp->cam.mcamList.numMCams);

    uint8_t act_res = mcamList[0].camID;

    EXPECT_EQ(act_res, tp->cam.camID);
}

TEST_F(MantisAPITest_camconn, getCameraInfo_P) {
    CAMERA_INFO act_res = getCameraInfo(tp->cam);

    EXPECT_EQ(act_res.serialNumber, 1234);
}

TEST_F(MantisAPITest_N, getCameraInfo_N) {
    CAMERA_INFO act_res = getCameraInfo(cam);

    EXPECT_EQ(act_res.serialNumber, 1234);
}

/*********************************************************************
 * Data Interface
 *********************************************************************/

TEST_F(MantisAPITest_camconn, isCameraReceivingData_P) {
	setCameraReceivingData(tp->cam ,true, 10);

	AQ_RETURN_CODE act_res;

    act_res = setCameraRecording(tp->cam, true, 5);

    EXPECT_EQ(act_res, AQ_SUCCESS);

    act_res = setCameraRecording(tp->cam, false, 5);

    EXPECT_EQ(act_res, AQ_SUCCESS);

    setCameraReceivingData(tp->cam ,false, 10);
}

TEST_F(MantisAPITest_N, isCameraReceivingData_N) {
    AQ_SYSTEM_STATE act_res = isCameraReceivingData(cam);

    EXPECT_EQ(act_res, 999);
}

TEST_F(MantisAPITest_camconn, setCameraReceivingData_P) {
    AQ_RETURN_CODE act_res = setCameraReceivingData(tp->cam, true, 10);

    setCameraReceivingData(tp->cam, false, 10);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_N,  setCameraReceivingData_N) {
    AQ_RETURN_CODE act_res = setCameraReceivingData(cam, true, 1);

    EXPECT_NE(act_res, 0);
}

TEST_F(MantisAPITest_camconn, getFrame_P) {
	setCameraReceivingData(tp->cam, true, 5);

    bool act_res = false;

    uint32_t frame_cnt = 0;
    for( int i = 0; i < tp->cam.mcamList.numMCams; i++ ){
        FRAME frame = getFrame(tp->cam,
                               tp->cam.mcamList.mcams[i].mcamID,
                               0,
                               ATL_TILING_1_1_2,
                               ATL_TILE_4K);

        if( frame.m_image != NULL ){
            if (fileExists("test_frame.jpeg")) {
                std::remove("test_frame.jpeg");
            }
            saveFrame(frame, "test_frame");
            act_res = fileExists("test_frame.jpeg");
            frame_cnt++;
        }
    }

    EXPECT_TRUE(act_res);

    setCameraReceivingData(tp->cam, false, 5);

    //EXPECT_EQ(frame_cnt, cam.numMCams);
}

TEST_F(MantisAPITest_N, getFrame_N) {
    FRAME frame = getFrame(cam,
                           mcam.mcamID,
                           0,
                           ATL_TILING_1_1_2,
                           ATL_TILE_4K);

    bool act_res = (frame.m_image != NULL);
    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest, saveFrame_P) {
    //getFrame
}

TEST_F(MantisAPITest_N, saveFrame_N) {
    FRAME frame;

    bool act_res = saveFrame(frame, "test_frame_N");

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest, setLatestTimeCallback) {
    CAMERA_UINT64_CALLBACK uCB;
    uCB.f = latestTimeCallback;
    uCB.data = &tp->cam;
    setLatestTimeCallback(tp->cam, uCB);

    sleep(1);

    bool act_res = (tp->cam.camID == tp->cam.camID);

    EXPECT_TRUE(act_res);
}

/*******************************************************************
*Stream management - creation and deletion of streams
********************************************************************/
//issue with unclosed receiver
TEST_F(MantisAPITest_lstream, streamExists_P) {
    bool act_res = streamExists(tp->astream, 5);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, streamExists_N) {
    bool act_res = streamExists(astream, 1);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_lstream, createLiveStream_P) {
    bool act_res = streamExists(tp->astream, 5);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, createLiveStream_N) {
    bool act_res = streamExists(astream, 1);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_camconn, createClipStream_P) {
	setCameraRecording(tp->cam , true, 5);
	sleep(2);
	setCameraRecording(tp->cam , false, 5);

	ACOS_CLIP* recordingList;

    requestStoredRecordings( &recordingList );

    ACOS_STREAM astream = createClipStream(recordingList[0], tp->profile);

    bool act_res = streamExists(astream, 5);

    deleteStream(astream);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, createClipStream_N) {
    ACOS_CLIP clip;

    ACOS_STREAM astream = createClipStream(clip, profile);

    bool act_res = streamExists(astream, 5);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_camconn, createMCamStream_P) {
    ACOS_STREAM astream = createMCamStream( tp->cam, tp->mcam );

    bool act_res = streamExists(astream, 10);

    deleteStream(astream);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, createMCamStream_N) {
    ACOS_STREAM astream = createMCamStream( cam, mcam );

    bool act_res = streamExists(astream, 10);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_camconn, deleteStream_P) {
    ACOS_STREAM astream;

    astream = createLiveStream(tp->cam, tp->profile);

    bool act_res;

    act_res = deleteStream(astream);

    EXPECT_TRUE(act_res);

    ACOS_CLIP* recordingList;

    requestStoredRecordings( &recordingList );

    astream = createClipStream(recordingList[0], tp->profile);

    act_res = deleteStream(astream);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, deleteStream_N) {
    bool act_res = deleteStream(astream);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_camconn, initStreamReceiver_P) {
    FRAME frame;
    FRAME_CALLBACK fCB;
    fCB.f = frameCallback;
    fCB.data = &frame;

    ACOS_STREAM astream = createMCamStream( tp->cam, tp->mcam );

    bool act_res = initStreamReceiver(fCB, astream, tp->port, 1.0);

    closeStreamReceiver(tp->r_port);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, initStreamReceiver_N) {
    bool act_res = initStreamReceiver(fCB, astream, port, 1.0);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_camconn, createStreamReceiver_P) {
    FRAME frame;
    FRAME_CALLBACK fCB;
    fCB.f = frameCallback;
    fCB.data = &frame;

    ACOS_STREAM stream;

    uint16_t clientport = tp->port;

    bool act_res = createStreamReceiver(fCB, clientport, 1.0);

    closeStreamReceiver(tp->r_port);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, createStreamReceiver_N) {
    bool act_res = createStreamReceiver(fCB, r_port, 1.0);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_lstream, connectStreamReceiver_P) {
    FRAME frame;
    FRAME_CALLBACK fCB;
    fCB.f = frameCallback;
    fCB.data = &frame;

    createStreamReceiver(fCB, tp->r_port, 1);

    bool act_res = connectStreamReceiver(tp->astream, tp->r_port);

    closeStreamReceiver(tp->r_port);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, connectStreamReceiver_N) {
    bool act_res = connectStreamReceiver(astream, r_port);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_lstream, disconnectStreamReceiver_P) {
    FRAME frame;
    FRAME_CALLBACK fCB;
    fCB.f = frameCallback;
    fCB.data = &frame;

    createStreamReceiver(fCB, tp->r_port, 1);

    connectStreamReceiver(tp->astream, tp->r_port);

    bool act_res = disconnectStreamReceiver(tp->astream, tp->r_port);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, disconnectStreamReceiver_N) {
    bool act_res = disconnectStreamReceiver(astream, port);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_camconn, closeStreamReceiver_P) {
    FRAME frame;
    FRAME_CALLBACK fCB;
    fCB.f = frameCallback;
    fCB.data = &frame;

    createStreamReceiver(fCB, tp->r_port, 1);

    bool act_res = closeStreamReceiver(tp->r_port);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, closeStreamReceiver_N) {
    bool act_res = closeStreamReceiver(r_port);;

    EXPECT_FALSE(act_res);
}

/*******************************************************************
*Stream controls - controls a camera stream
********************************************************************/

TEST_F(MantisAPITest_cstream, setStreamPlaySpeed_P) {
    bool act_res = setStreamPlaySpeed(tp->astream, 1.0);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setStreamPlaySpeed_N) {
    bool act_res = setStreamPlaySpeed(astream, 1.0);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_cstream, streamFrameStep_P) {
    bool act_res = streamFrameStep(tp->astream, 1);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setStreamFrameStep_N) {
    bool act_res = streamFrameStep(astream, 1);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_cstream, setStreamToTime_P) {
    bool act_res = setStreamToTime(tp->astream, getCurrentTimestamp());

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setStreamToTime_N) {
    bool act_res = setStreamToTime(astream, 1);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_cstream, DISABLED_setStreamGoLive_P) {
    bool act_res = setStreamGoLive(tp->astream);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setStreamGoLive_N) {
    bool act_res = setStreamGoLive(astream);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_cstream, setStreamGoToClipStart_P) {
    bool act_res = setStreamGoToClipStart(tp->astream);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setStreamGoToClipStart_N) {
    bool act_res = setStreamGoToClipStart(astream);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_lstream, setStreamPTZVelocity_P) {
    ACOS_PTZ_VELOCITY vel;

    vel.pan_per_second = 1.0;
    vel.tilt_per_second = 1.0;
    vel.zoom_per_second = 1.0;

    bool act_res = setStreamPTZVelocity(tp->astream, vel);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setStreamPTZVelocity_N) {
    bool act_res = setStreamPTZVelocity(astream, vel);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_lstream, setStreamPTZAbsolute_P) {
    ACOS_PTZ_ABSOLUTE abs;

    abs.pan_degrees = 1.0;
    abs.tilt_degrees = 1.0;
    abs.zoom_factor = 1.0;

    bool act_res = setStreamPTZAbsolute(tp->astream, abs);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setStreamPTZAbsolute_N) {
    bool act_res = setStreamPTZAbsolute(astream, abs);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_lstream, setStreamGain_P) {
    bool act_res = setStreamGain(tp->astream, 1.0);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setStreamGain_N) {
    bool act_res = setStreamGain(astream, 1.0);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_lstream, setStreamOffset_P) {
    bool act_res = setStreamOffset(tp->astream, 1.0);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setStreamOffset_N) {
    bool act_res = setStreamOffset(astream, 1.0);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_lstream, setStreamGamma_P) {
    bool act_res = setStreamGamma(tp->astream, 1.0);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setStreamGamma_N) {
    bool act_res = setStreamGamma(astream, 1.0);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_lstream, setStreamDenoise_P) {
    bool act_res = setStreamDenoise(tp->astream, true);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setStreamDenoise_N) {
    bool act_res = setStreamDenoise(astream, true);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_lstream, setStreamSmoothDenoise_P) {
    bool act_res = setStreamSmoothDenoise(tp->astream, 1.0);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setStreamSmoothDenoise_N) {
    bool act_res = setStreamSmoothDenoise(astream, 1.0);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_lstream, setStreamEdgeDenoise_P) {
    bool act_res = setStreamEdgeDenoise(tp->astream, 1.0);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setStreamEdgeDenoise_N) {
    bool act_res = setStreamEdgeDenoise(astream, 1.0);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_lstream, setStreamEncoder_P) {
    bool act_res = setStreamEncoder(tp->astream, tp->profile.videoEncoder);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setStreamEncoder_N) {
    bool act_res = setStreamEncoder(astream, profile.videoEncoder);

    EXPECT_FALSE(act_res);
}

/*********************************************************************
 * Stream State Getters
 *********************************************************************/

TEST_F(MantisAPITest_lstream, getStreamGain_P) {
    double act_res = getStreamGain(tp->astream);

    EXPECT_NE(act_res, -1);
}

TEST_F(MantisAPITest_N, getStreamGain_N) {
    double act_res = getStreamGain(astream);

    EXPECT_EQ(act_res, -1);
}

TEST_F(MantisAPITest_lstream, getStreamOffset_P) {
    double act_res = getStreamOffset(tp->astream);

    EXPECT_NE(act_res, -1);
}

TEST_F(MantisAPITest_N, getStreamOffset_N) {
    double act_res = getStreamOffset(astream);

    EXPECT_EQ(act_res, -1);
}

TEST_F(MantisAPITest_lstream, getStreamGamma_P) {
    double act_res = getStreamGamma(tp->astream);

    EXPECT_NE(act_res, -1);
}

TEST_F(MantisAPITest_N, getStreamGamma_N) {
    double act_res = getStreamGamma(astream);

    EXPECT_EQ(act_res, -1);
}

TEST_F(MantisAPITest_lstream, getStreamDenoise_P) {
	bool act_res = getStreamDenoise(tp->astream);

    EXPECT_TRUE(true);
}

TEST_F(MantisAPITest_N, getStreamDenoise_N) {
    bool act_res = getStreamDenoise(astream);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_lstream, getStreamSmoothDenoise_P) {
    double act_res = getStreamSmoothDenoise(tp->astream);

    EXPECT_NE(act_res, -1);
}

TEST_F(MantisAPITest_N, getStreamSmoothDenoise_N) {
    double act_res = getStreamSmoothDenoise(astream);

    EXPECT_EQ(act_res, -1);
}

TEST_F(MantisAPITest_lstream, getStreamEdgeDenoise_P) {
    double act_res = getStreamEdgeDenoise(tp->astream);

    EXPECT_NE(act_res, -1);
}

TEST_F(MantisAPITest_N, getStreamEdgeDenoise_N) {
    double act_res = getStreamEdgeDenoise(astream);

    EXPECT_EQ(act_res, -1);
}

 /*********************************************************************
 * Clip Data Management
 *********************************************************************/

TEST_F(MantisAPITest_camconn, setNewClipCallback) {
    ACOS_CLIP clip;
    ACOS_CLIP_CALLBACK clipCB;
    clipCB.f = newClipCallback;
    clipCB.data = &clip;
    setNewClipCallback(clipCB);

    setCameraReceivingData(tp->cam ,true, 10);
	setCameraRecording(tp->cam, true, 10);
	sleep(1);
	setCameraRecording(tp->cam, false, 10);
	setCameraReceivingData(tp->cam ,false, 10);

    bool act_res = (clip.cam.camID != tp->camID);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest, setClipDeletedCallback) {
    ACOS_CLIP clip;
    ACOS_CLIP_CALLBACK deletedClipCB;
    deletedClipCB.f = deletedClipCallback;
    deletedClipCB.data = &clip;
    setClipDeletedCallback(deletedClipCB);

    setCameraReceivingData(tp->cam ,true, 10);
	setCameraRecording(tp->cam, true, 10);
	sleep(1);
	setCameraRecording(tp->cam, false, 10);
	setCameraReceivingData(tp->cam ,false, 10);

    ACOS_CLIP* clipList;
    requestStoredRecordings(&clipList);
    deleteClip(clipList[0]);

    sleep(1);

    bool act_res = (clip.cam.camID != tp->camID);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_camconn, requestStoredRecordings_P) {
    setCameraReceivingData(tp->cam ,true, 10);
	setCameraRecording(tp->cam, true, 10);
	sleep(1);
	setCameraRecording(tp->cam, false, 10);
	setCameraReceivingData(tp->cam ,false, 10);

	ACOS_CLIP* clipList;

    unsigned act_res = requestStoredRecordings(&clipList);

    EXPECT_GT(act_res, 0);
}

TEST_F(MantisAPITest_N, requestStoredRecordings_N) {
	ACOS_CLIP* clipList;

	unsigned act_res = requestStoredRecordings(&clipList);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest, setCameraRecording_P) {
	setCameraReceivingData(tp->cam ,true, 10);

	AQ_RETURN_CODE act_res;

    act_res = setCameraRecording(tp->cam, true, 5);

    EXPECT_EQ(act_res, AQ_SUCCESS);

    act_res = setCameraRecording(tp->cam, false, 5);

    EXPECT_EQ(act_res, AQ_SUCCESS);
}

TEST_F(MantisAPITest_N, setCameraRecording_N) {
    AQ_RETURN_CODE act_res = setCameraRecording(cam, true, 5);

    EXPECT_NE(act_res, AQ_SUCCESS);
}

TEST_F(MantisAPITest_camconn, deleteClip_P) {
    setCameraReceivingData(tp->cam ,true, 10);
	setCameraRecording(tp->cam, true, 10);
	sleep(1);
	setCameraRecording(tp->cam, false, 10);
	setCameraReceivingData(tp->cam ,false, 10);

	ACOS_CLIP* clipList;
    requestStoredRecordings(&clipList);

    bool act_res = deleteClip(clipList[0]);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, deleteClip_N) {
    bool act_res = deleteClip(clip);

    EXPECT_FALSE(act_res);
}

/********************************************************************
 * High-level operations and processing threads
 ********************************************************************/

TEST_F(MantisAPITest, DISABLED_updateCameraModel_P) {
    bool act_res = updateCameraModel(tp->cam, tp->model_file);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, updateCameraModel_N) {
    bool act_res = updateCameraModel(cam, model_file);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest, DISABLED_updateClipModels_P) {
    setCameraReceivingData(tp->cam ,true, 10);
	setCameraRecording(tp->cam, true, 10);
	sleep(1);
	setCameraRecording(tp->cam, false, 10);
	setCameraReceivingData(tp->cam ,false, 10);

	ACOS_CLIP* clipList;
    requestStoredRecordings(&clipList);

    bool act_res = updateClipModels(clipList[0], tp->clip_model_file);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, updateClipModels_N) {
    bool act_res = updateClipModels(clip, model_file);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest, performGlobalWhiteBalance_P) {
    bool act_res = performGlobalWhiteBalance(tp->cam);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, performGlobalWhiteBalance_N) {
    bool act_res = performGlobalWhiteBalance(cam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest, toggleGlobalWhiteBalanceAutoLoop_P) {
    bool act_res = toggleGlobalWhiteBalanceAutoLoop(tp->cam, false);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, toggleGlobalWhiteBalanceAutoLoop_N) {
    bool act_res = toggleGlobalWhiteBalanceAutoLoop(cam, false);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest, performGlobalGain_P) {
    bool act_res = performGlobalGain(tp->cam);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, performGlobalGain_N) {
    bool act_res = performGlobalGain(cam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest, toggleGlobalGainLoop_P) {
    bool act_res = toggleGlobalGainLoop(tp->cam, true);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, toggleGlobalGainLoop_N) {
    bool act_res = toggleGlobalGainLoop(cam, false);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest, performGlobalAutoShutter_P) {
    bool act_res = performGlobalAutoShutter(tp->cam);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, performGlobalAutoShutter_N) {
    bool act_res = performGlobalAutoShutter(cam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest, toggleGlobalAutoExposureLoop_P) {
    bool act_res = toggleGlobalAutoShutterLoop(tp->cam, true);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, toggleGlobalAutoExposureLoop_N) {
    bool act_res = toggleGlobalAutoShutterLoop(cam, false);

    EXPECT_FALSE(act_res);
}

/****************************************************************
* Debugging functions
****************************************************************/

TEST_F(MantisAPITest_camconn, saveCameraState) {
	char *dir = "_state_.json";

	bool act_res = saveCameraState(dir);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_camconn, loadCameraState) {
	char *dir = "_state.json_";

	bool act_res = loadCameraState(dir);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest, printCameraProperties) {
    EXPECT_NO_THROW(printCameraProperties());
}

TEST_F(MantisAPITest, getCameraProperties) {
    char* buffer;
    int size = 1;

    EXPECT_NO_THROW(getCameraProperties(buffer, size));
}

TEST_F(MantisAPITest, setSystemCallbacks) {
    SYSTEM_CALLBACKS sCB;

    EXPECT_NO_THROW(setSystemCallbacks(sCB));
}



int main(int argc, char **argv) {
    ::testing::InitGoogleTest( &argc, argv );
	::testing::GTEST_FLAG(filter) = "*_P";
	RUN_ALL_TESTS();
	::testing::GTEST_FLAG(filter) = "*_B";
	RUN_ALL_TESTS();
	::testing::GTEST_FLAG(filter) = "*_N";
	RUN_ALL_TESTS();
    ::testing::GTEST_FLAG(filter) = "*_CC";
    RUN_ALL_TESTS();

	return 0;
}
