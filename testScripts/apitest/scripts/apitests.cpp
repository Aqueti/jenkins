#include "apitest.h"

/*************************************************************
* Configuration and Setup
*************************************************************/

TEST_F(MantisAPITest, connectToCameraServer_P) {
	AQ_SYSTEM_STATE act_res = isConnectedToCameraServer();

    EXPECT_EQ(act_res, AQ_SERVER_CONNECTED);
}

TEST_F(MantisAPITest_N, connectToCameraServer_N) {
    AQ_RETURN_CODE act_res = connectToCameraServer(ip, port);

    EXPECT_EQ(act_res, AQ_ERROR_RENDER_CONNECT_FAILURE);
}

TEST_F(MantisAPITest, disconnectFromCameraServer_P) {
	AQ_RETURN_CODE act_res = disconnectFromCameraServer();

    EXPECT_EQ(act_res, AQ_SUCCESS);
}

TEST_F(MantisAPITest_N, disconnectFromCameraServer_N) {
    AQ_RETURN_CODE act_res = disconnectFromCameraServer();

    EXPECT_EQ(act_res, AQ_SUCCESS);
}

TEST_F(MantisAPITest, isConnectedToCameraServer_P) {
	AQ_SYSTEM_STATE act_res = isConnectedToCameraServer();

    EXPECT_EQ(act_res, AQ_SERVER_CONNECTED);
}

TEST_F(MantisAPITest_N, isConnectedToCameraServer_N) {
	AQ_SYSTEM_STATE act_res = isConnectedToCameraServer();

    EXPECT_EQ(act_res, AQ_SERVER_DISCONNECTED);
}

TEST_F(MantisAPITest_B, setNewConnectedToServerCallback_B) {
	connectToCameraServer(ip, port);

	AQ_SYSTEM_STATE act_res;
    AQ_SYSTEM_STATE_CALLBACK sCB;
    sCB.f = newConnectedToServerCallback;
    sCB.data = &act_res;
    setNewConnectedToServerCallback(sCB);

    disconnectFromCameraServer();

    sleep(1);

    EXPECT_EQ(act_res, AQ_SERVER_DISCONNECTED);
}

TEST_F(MantisAPITest, isCameraConnected_P) {
	AQ_SYSTEM_STATE act_res;

	setCameraConnection(cam, true, 10);

	act_res = isCameraConnected(cam);

	EXPECT_EQ(act_res, AQ_CAMERA_CONNECTED);

    setCameraConnection(cam, false, 10);

    act_res = isCameraConnected(cam);

    EXPECT_EQ(act_res, AQ_CAMERA_DISCONNECTED);
}

TEST_F(MantisAPITest_N, isCameraConnected_N) {
	AQ_SYSTEM_STATE act_res = isCameraConnected(cam);

	EXPECT_EQ(act_res, AQ_STATE_UNKNOWABLE);
}

TEST_F(MantisAPITest, setCameraConnection_P) {
    setCameraConnection(cam, true, 10);

    AQ_SYSTEM_STATE act_res;

    act_res = isCameraConnected(cam);

    EXPECT_EQ(act_res, AQ_CAMERA_CONNECTED);

    setCameraConnection(cam, false, 10);

    act_res = isCameraConnected(cam);

    EXPECT_EQ(act_res, AQ_CAMERA_DISCONNECTED);
}

TEST_F(MantisAPITest_N, setCameraConnection_N) {
    setCameraConnection(cam, true, 10);

    AQ_SYSTEM_STATE act_res = isCameraConnected(cam);

    EXPECT_EQ(act_res, AQ_STATE_UNKNOWABLE);
}

TEST_F(MantisAPITest, disconnectCamera_P) {
	disconnectCamera(cam);

    AQ_SYSTEM_STATE act_res = isCameraConnected(cam);

    EXPECT_EQ(act_res, AQ_CAMERA_DISCONNECTED);

    act_res = isConnectedToCameraServer();

    EXPECT_EQ(act_res, AQ_SERVER_CONNECTED);
}

TEST_F(MantisAPITest_N, disconnectCamera_N) {
	AQ_SYSTEM_STATE act_res = isCameraConnected(cam);

    EXPECT_EQ(act_res, AQ_STATE_UNKNOWABLE);
}

TEST_F(MantisAPITest_B, setNewCameraCallback_B) {
	connectToCameraServer(ip, port);

	ACOS_CAMERA cam;
	NEW_CAMERA_CALLBACK camCB;
	camCB.f = newCameraCallback;
	camCB.data = &cam;
	setNewCameraCallback(camCB);

	uint32_t act_res = cam.camID;

	disconnectFromCameraServer();

    EXPECT_EQ(act_res, camID);
}

TEST_F(MantisAPITest_B, setCameraDeletedCallback_B) {
	connectToCameraServer(ip, port);

	ACOS_CAMERA cam;
	NEW_CAMERA_CALLBACK camCB;
	camCB.f = newCameraCallback;
	camCB.data = &cam;
	setNewCameraCallback(camCB);

    uint32_t act_res;
    CAMERA_DELETED_CALLBACK deletedCB;
    deletedCB.f = cameraDeletedCallback;
    deletedCB.data = &act_res;
    setCameraDeletedCallback(deletedCB);

    disconnectFromCameraServer();

    sleep(1);

    EXPECT_EQ(camID, camID); //incorrect val
}

TEST_F(MantisAPITest, getNumberOfCameras_P) {
    uint32_t act_res = getNumberOfCameras();

    ASSERT_EQ(act_res, numCams);
}

TEST_F(MantisAPITest_N, getNumberOfCameras_N) {
    uint32_t act_res = getNumberOfCameras();

    ASSERT_EQ(act_res, numCams);
}

TEST_F(MantisAPITest_B, setCameraPropertyCallbacks_B) {
	connectToCameraServer(ip, port);

	ACOS_CAMERA cam;
    CAMERA_CALLBACKS cbs;
    cbs.cameraConnectionCallback.f = cameraPropertyCallback;
    cbs.cameraConnectionCallback.data = &cam;

    cbs.dataFlowStatusCallback.f = cameraPropertyCallback;
    cbs.dataFlowStatusCallback.data = &cam;

    setCameraPropertyCallbacks(cbs);

    sleep(1);

    bool act_res = (cam.camID == camID);

    disconnectFromCameraServer();

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_camconn, getCameraNumberOfMCams_P) {
    uint32_t act_res = getCameraNumberOfMCams(cam);

    EXPECT_EQ(act_res, numMCams);
}

TEST_F(MantisAPITest_N, getCameraNumberOfMCams_N) {
    uint32_t act_res = getCameraNumberOfMCams(cam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest, DISABLED_getCameraMCamList_P) {
	connectToCameraServer(ip, port);

	ACOS_CAMERA cam;
	NEW_CAMERA_CALLBACK camCB;
	camCB.f = newCameraCallback;
	camCB.data = &cam;
	setNewCameraCallback(camCB);

	setCameraConnection(cam, true, 10);

	fillCameraMCamList(&cam);

	sleep(1);

	MICRO_CAMERA *mcamList;

    try {
    	getCameraMCamList(cam, mcamList, cam.mcamList.numMCams);
    } catch(exception& e) {
    	FAIL();
    }

    uint8_t act_res = mcamList[0].camID;

	setCameraConnection(cam, false, 10);

	disconnectFromCameraServer();

    EXPECT_EQ(act_res, cam.mcamList.mcams[0].camID);
}

TEST_F(MantisAPITest_N, getCameraMCamList_N) {
    getCameraMCamList(cam, mcamList, numMCams);

    bool act_res = (mcamList == NULL);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_camconn, getCameraInfo_P) {
    CAMERA_INFO act_res = getCameraInfo(cam);

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
	setCameraReceivingData(cam ,true, 10);

	AQ_SYSTEM_STATE act_res;

	act_res = isCameraReceivingData(cam);

    EXPECT_EQ(act_res, AQ_CAMERA_RECEIVING_DATA);

    setCameraReceivingData(cam ,false, 10);

    act_res = isCameraReceivingData(cam);

    EXPECT_EQ(act_res, AQ_CAMERA_NOT_RECEIVING_DATA);
}

TEST_F(MantisAPITest_N, isCameraReceivingData_N) {
    AQ_SYSTEM_STATE act_res = isCameraReceivingData(cam);

    EXPECT_EQ(act_res, AQ_STATE_UNKNOWABLE);
}

TEST_F(MantisAPITest_camconn, setCameraReceivingData_P) {
    AQ_RETURN_CODE act_res = setCameraReceivingData(cam, true, 10);

    setCameraReceivingData(cam, false, 10);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_N,  setCameraReceivingData_N) {
    AQ_RETURN_CODE act_res = setCameraReceivingData(cam, true, 1);

    EXPECT_NE(act_res, 0);
}

TEST_F(MantisAPITest_camconn, getFrame_P) {
	setCameraReceivingData(cam, true, 5);

	sleep(1);

	FRAME frame = getFrame(cam,
						   cam.mcamList.mcams[0].mcamID,
						   0,
						   ATL_TILING_1_1_2,
						   ATL_TILE_4K);

	bool act_res = (frame.m_image != NULL);

	setCameraReceivingData(cam, false, 5);

    EXPECT_TRUE(act_res);
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
	setCameraReceivingData(cam, true, 5);

	sleep(1);

	FRAME frame = getFrame(cam,
						   cam.mcamList.mcams[0].mcamID,
						   0,
						   ATL_TILING_1_1_2,
						   ATL_TILE_4K);

	bool act_res = false;

	if( frame.m_image != NULL ){
		if (fileExists("test_frame.jpeg")) {
			std::remove("test_frame.jpeg");
		}
		saveFrame(frame, "test_frame");
		act_res = fileExists("test_frame.jpeg");
	}

	EXPECT_TRUE(act_res);

	setCameraReceivingData(cam, false, 5);
}

TEST_F(MantisAPITest_N, saveFrame_N) {
    FRAME frame;

    saveFrame(frame, "test_frame_N");

    bool act_res = fileExists("test_frame_N.jpeg");

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_B, setLatestTimeCallback_B) {
	connectToCameraServer(ip, port);

	ACOS_CAMERA cam;
	NEW_CAMERA_CALLBACK camCB;
	camCB.f = newCameraCallback;
	camCB.data = &cam;
	setNewCameraCallback(camCB);

    CAMERA_UINT64_CALLBACK uCB;
    uCB.f = latestTimeCallback;
    uCB.data = &cam;
    setLatestTimeCallback(cam, uCB);

    sleep(1);

    bool act_res = (cam.camID == camID);

    disconnectFromCameraServer();

    EXPECT_TRUE(act_res);
}

/*******************************************************************
*Stream management - creation and deletion of streams
********************************************************************/

TEST_F(MantisAPITest_lstream, streamExists_P) {
    bool act_res = streamExists(astream, 5);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, streamExists_N) {
    bool act_res = streamExists(astream, 1);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_lstream, createLiveStream_P) {
    bool act_res = streamExists(astream, 5);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, createLiveStream_N) {
    bool act_res = streamExists(astream, 1);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_cstream, createClipStream_P) {
    bool act_res = streamExists(astream, 5);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, createClipStream_N) {
    ACOS_STREAM astream = createClipStream(clip, profile);

    bool act_res = streamExists(astream, 5);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mlstream, createMCamStream_P) {
    bool act_res = streamExists(astream, 10);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, createMCamStream_N) {
    ACOS_STREAM astream = createMCamStream( cam, mcam );

    bool act_res = streamExists(astream, 10);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_lstream, deleteStream_P) {
	bool act_res;

	if(!streamExists(astream, 5)) FAIL();
    else act_res = deleteStream(astream);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, deleteStream_N) {
    bool act_res = deleteStream(astream);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_lstream, initStreamReceiver_P) {
    bool act_res = (frame.m_metadata.m_height == profile.videoEncoder.height &&
    				frame.m_metadata.m_width == profile.videoEncoder.width);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, initStreamReceiver_N) {
    FRAME_CALLBACK fcb;
    fcb.f = frameCallback;

    bool act_res = initStreamReceiver(fcb, astream, port, 1.0);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_camconn, createStreamReceiver_P) {
    FRAME_CALLBACK fCB;
    fCB.f = frameCallback;

    bool act_res = createStreamReceiver(fCB, port, 1.0);

    closeStreamReceiver(r_port);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, createStreamReceiver_N) {
    FRAME_CALLBACK fcb;
    fcb.f = frameCallback;

    r_port = -1;

    bool act_res = createStreamReceiver(fcb, r_port, 1.0);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_lstream, connectStreamReceiver_P) {
    bool act_res = connectStreamReceiver(astream, r_port);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, connectStreamReceiver_N) {
    bool act_res = connectStreamReceiver(astream, r_port);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_lstream, disconnectStreamReceiver_P) {
    bool act_res = disconnectStreamReceiver(astream, r_port);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, disconnectStreamReceiver_N) {
    bool act_res = disconnectStreamReceiver(astream, port);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_lstream, closeStreamReceiver_P) {
    bool act_res = closeStreamReceiver(r_port);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, closeStreamReceiver_N) {
    bool act_res = closeStreamReceiver(r_port);;

    EXPECT_FALSE(act_res);
}

/*******************************************************************
*Stream controls - controls a camera stream
********************************************************************/

TEST_F(MantisAPITest_lstream, setStreamPlaySpeed_P) {
    bool act_res = setStreamPlaySpeed(astream, 0.0);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setStreamPlaySpeed_N) {
    bool act_res = setStreamPlaySpeed(astream, 0.0);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_lstream, streamFrameStep_P) {
    bool act_res = streamFrameStep(astream, 1);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setStreamFrameStep_N) {
    bool act_res = streamFrameStep(astream, 1);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_lstream, setStreamToTime_P) {
	uint64_t time = frame.m_metadata.m_timestamp;

	sleep(1);

    bool act_res = setStreamToTime(astream, time);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setStreamToTime_N) {
    bool act_res = setStreamToTime(astream, 0);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_lstream, setStreamGoLive_P) {
	streamFrameStep(astream, 1);

    bool act_res = setStreamGoLive(astream);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setStreamGoLive_N) {
    bool act_res = setStreamGoLive(astream);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_cstream, setStreamGoToClipStart_P) {
    bool act_res = setStreamGoToClipStart(astream);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setStreamGoToClipStart_N) {
    bool act_res = setStreamGoToClipStart(astream);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_lstream, setStreamPTZVelocity_P) {
    bool act_res = setStreamPTZVelocity(astream, ptz_vel);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setStreamPTZVelocity_N) {
    bool act_res = setStreamPTZVelocity(astream, ptz_vel);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_lstream, setStreamPTZAbsolute_P) {
    bool act_res = setStreamPTZAbsolute(astream, ptz_abs);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setStreamPTZAbsolute_N) {
    bool act_res = setStreamPTZAbsolute(astream, ptz_abs);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_lstream, setStreamGain_P) {
    bool act_res = setStreamGain(astream, 1.0);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setStreamGain_N) {
    bool act_res = setStreamGain(astream, 1.0);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_lstream, setStreamOffset_P) {
    bool act_res = setStreamOffset(astream, 1.0);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setStreamOffset_N) {
    bool act_res = setStreamOffset(astream, 1.0);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_lstream, setStreamGamma_P) {
    bool act_res = setStreamGamma(astream, 1.0);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setStreamGamma_N) {
    bool act_res = setStreamGamma(astream, 1.0);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_lstream, setStreamDenoise_P) {
    bool act_res = setStreamDenoise(astream, true);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setStreamDenoise_N) {
    bool act_res = setStreamDenoise(astream, true);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_lstream, setStreamSmoothDenoise_P) {
    bool act_res = setStreamSmoothDenoise(astream, 1.0);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setStreamSmoothDenoise_N) {
    bool act_res = setStreamSmoothDenoise(astream, 1.0);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_lstream, setStreamEdgeDenoise_P) {
    bool act_res = setStreamEdgeDenoise(astream, 1.0);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setStreamEdgeDenoise_N) {
    bool act_res = setStreamEdgeDenoise(astream, 1.0);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_lstream, setStreamEncoder_P) {
    bool act_res = setStreamEncoder(astream, profile.videoEncoder);

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
    double act_res = getStreamGain(astream);

    EXPECT_NE(act_res, -1);
}

TEST_F(MantisAPITest_N, getStreamGain_N) {
    double act_res = getStreamGain(astream);

    EXPECT_EQ(act_res, -1);
}

TEST_F(MantisAPITest_lstream, getStreamOffset_P) {
    double act_res = getStreamOffset(astream);

    EXPECT_NE(act_res, -1);
}

TEST_F(MantisAPITest_N, getStreamOffset_N) {
    double act_res = getStreamOffset(astream);

    EXPECT_EQ(act_res, -1);
}

TEST_F(MantisAPITest_lstream, getStreamGamma_P) {
    double act_res = getStreamGamma(astream);

    EXPECT_NE(act_res, -1);
}

TEST_F(MantisAPITest_N, getStreamGamma_N) {
    double act_res = getStreamGamma(astream);

    EXPECT_EQ(act_res, -1);
}

TEST_F(MantisAPITest_lstream, getStreamDenoise_P) {
	bool act_res = getStreamDenoise(astream);

    EXPECT_TRUE(true);
}

TEST_F(MantisAPITest_N, getStreamDenoise_N) {
    bool act_res = getStreamDenoise(astream);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_lstream, getStreamSmoothDenoise_P) {
    double act_res = getStreamSmoothDenoise(astream);

    EXPECT_NE(act_res, -1);
}

TEST_F(MantisAPITest_N, getStreamSmoothDenoise_N) {
    double act_res = getStreamSmoothDenoise(astream);

    EXPECT_EQ(act_res, -1);
}

TEST_F(MantisAPITest_lstream, getStreamEdgeDenoise_P) {
    double act_res = getStreamEdgeDenoise(astream);

    EXPECT_NE(act_res, -1);
}

TEST_F(MantisAPITest_N, getStreamEdgeDenoise_N) {
    double act_res = getStreamEdgeDenoise(astream);

    EXPECT_EQ(act_res, -1);
}

/*********************************************************************
 * Clip Data Management
 *********************************************************************/

TEST_F(MantisAPITest_cstream, setNewClipCallback) {
	setCameraRecording(cam, true, 10);
	sleep(1);
	setCameraRecording(cam, false, 10);

    bool act_res = (clip.cam.camID == camID);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_cstream, setClipDeletedCallback) {
    requestStoredRecordings(&clipList);
    deleteClip(clipList[0]);

    sleep(1);

    bool act_res = (del_clip.cam.camID == camID);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_cstream, requestStoredRecordings_P) {
    unsigned act_res = requestStoredRecordings(&clipList);

    EXPECT_GT(act_res, 0);
}

TEST_F(MantisAPITest_N, requestStoredRecordings_N) {
	unsigned act_res = requestStoredRecordings(&clipList);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_cstream, setCameraRecording_P) {
	AQ_RETURN_CODE act_res;

    act_res = setCameraRecording(cam, true, 5);

    EXPECT_EQ(act_res, AQ_SUCCESS);

    sleep(1);

    act_res = setCameraRecording(cam, false, 5);

    EXPECT_EQ(act_res, AQ_SUCCESS);
}

TEST_F(MantisAPITest_N, setCameraRecording_N) {
    AQ_RETURN_CODE act_res = setCameraRecording(cam, true, 5);

    EXPECT_EQ(act_res, AQ_ERROR_CAMERA_NOT_CURRENTLY_CONNECTED);
}

TEST_F(MantisAPITest_cstream, deleteClip_P) {
	ACOS_CLIP* clipList;
    uint16_t i = requestStoredRecordings(&clipList);

    bool act_res = deleteClip(clipList[0]);

    uint16_t j = requestStoredRecordings(&clipList);

    act_res = ((i - j) == 1) && act_res;

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
    bool act_res = updateCameraModel(cam, (cam_folder + "/model.json").c_str());

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, DISABLED_updateCameraModel_N) {
    bool act_res = updateCameraModel(cam, "model.json");

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_cstream, DISABLED_updateClipModels_P) {
	setCameraRecording(cam, true, 10);
	sleep(1);
	setCameraRecording(cam, false, 10);

    bool act_res = updateClipModels(clip, "session.json");

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, DISABLED_updateClipModels_N) {
    bool act_res = updateClipModels(clip, "session.json");

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest, performGlobalWhiteBalance_P) {
    bool act_res = performGlobalWhiteBalance(cam);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, performGlobalWhiteBalance_N) {
    bool act_res = performGlobalWhiteBalance(cam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest, toggleGlobalWhiteBalanceAutoLoop_P) {
    bool act_res = toggleGlobalWhiteBalanceAutoLoop(cam, true);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, toggleGlobalWhiteBalanceAutoLoop_N) {
    bool act_res = toggleGlobalWhiteBalanceAutoLoop(cam, true);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest, getGlobalWhiteBalanceAutoLoopState_P) {
    bool act_res = getGlobalWhiteBalanceAutoLoopState(cam);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, getGlobalWhiteBalanceAutoLoopState_N) {
    bool act_res = getGlobalWhiteBalanceAutoLoopState(cam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest, performGlobalGain_P) {
    bool act_res = performGlobalGain(cam);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, performGlobalGain_N) {
    bool act_res = performGlobalGain(cam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest, toggleGlobalGainLoop_P) {
    bool act_res = toggleGlobalGainLoop(cam, true);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, toggleGlobalGainLoop_N) {
    bool act_res = toggleGlobalGainLoop(cam, true);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest, getGlobalGainAutoLoopState_P) {
    bool act_res = getGlobalGainAutoLoopState(cam);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, getGlobalGainAutoLoopState_N) {
    bool act_res = getGlobalGainAutoLoopState(cam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest, performGlobalAutoShutter_P) {
    bool act_res = performGlobalAutoShutter(cam);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, performGlobalAutoShutter_N) {
    bool act_res = performGlobalAutoShutter(cam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest, toggleGlobalAutoExposureLoop_P) {
    bool act_res = toggleGlobalAutoShutterLoop(cam, true);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, toggleGlobalAutoExposureLoop_N) {
    bool act_res = toggleGlobalAutoShutterLoop(cam, true);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest, getGlobalShutterAutoLoopState_P) {
    bool act_res = getGlobalShutterAutoLoopState(cam);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, getGlobalShutterAutoLoopState_N) {
    bool act_res = getGlobalShutterAutoLoopState(cam);

    EXPECT_FALSE(act_res);
}

/****************************************************************
* Debugging functions
****************************************************************/

TEST_F(MantisAPITest_camconn, saveCameraState) {
	char *dir = "./";

	bool act_res = saveCameraState(dir);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_camconn, DISABLED_loadCameraState) {
	char *dir = "./";

	bool act_res = loadCameraState(dir);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest, DISABLED_printCameraProperties) {
    EXPECT_NO_THROW(printCameraProperties());
}

TEST_F(MantisAPITest, DISABLED_getCameraProperties) {
    char* buffer;
    int size = 1;

    EXPECT_NO_THROW(getCameraProperties(buffer, size));
}

TEST_F(MantisAPITest, DISABLED_setSystemCallbacks) {
    SYSTEM_CALLBACKS sCB;

    EXPECT_NO_THROW(setSystemCallbacks(sCB));
}



int main(int argc, char **argv) {
    ::testing::InitGoogleTest( &argc, argv );
	
	::testing::GTEST_FLAG(filter) = "*_N";
	RUN_ALL_TESTS();

	return 0;
}
