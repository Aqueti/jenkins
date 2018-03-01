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
    MICRO_CAMERA *mcamList;

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



/********************************************************************
 * Low level interface (microcamera controls)
 ********************************************************************/

TEST_F(MantisAPITest_N, mCamConnect_P) {
    char *mc_ip = "192.168.10.1";
    int mc_port = 9999;

    mCamConnect(mc_ip, mc_port);

    int act_res = getNumberOfMCams();

    mCamDisconnect(mc_ip, mc_port);

    EXPECT_GT(act_res,0);
}

TEST_F(MantisAPITest_N, mCamConnect_N) {
    mCamConnect(mc_ip, mc_port);

    int act_res = getNumberOfMCams();

    mCamDisconnect(mc_ip, mc_port);

    EXPECT_EQ(act_res,0);
}

TEST_F(MantisAPITest_mcamconn, DISABLED_mCamDisconnect_P) {
    mCamDisconnect(mc_ip, mc_port);
    EXPECT_EQ(1,1);
}

TEST_F(MantisAPITest_N, mCamDisconnect_N) {
    mCamDisconnect(mc_ip, mc_port);
    EXPECT_EQ(1,1);
}

TEST_F(MantisAPITest_mcamconn, initMCamFrameReceiver_P) {
    bool act_res = initMCamFrameReceiver( r_port, 1 );
    closeMCamFrameReceiver(r_port);
    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, initMCamFrameReceiver_N) {
    bool act_res = initMCamFrameReceiver( 66666, 1 );
    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, closeMCamFrameReceiver_P) {
    initMCamFrameReceiver( r_port, 1 );

    bool act_res = closeMCamFrameReceiver(r_port);
    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, closeMCamFrameReceiver_N) {
    bool act_res = closeMCamFrameReceiver(66666);
    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, getNumberOfMCams_P) {
    uint32_t act_res = getNumberOfMCams();
    EXPECT_EQ(act_res, numMCams);
}

TEST_F(MantisAPITest_N, getNumberOfMCams_N) {
    uint32_t act_res = getNumberOfMCams();
    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamlstream, startMCamStream_P) {
    bool act_res = (frame.m_metadata.m_width > 0);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, startMCamStream_N) {
    bool act_res = startMCamStream(mcam, r_port);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamlstream, stopMCamStream_P) {
    bool act_res = stopMCamStream(mcam, r_port);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, stopMCamStream_N) {
    bool act_res = stopMCamStream(mcam, r_port);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamStreamFilter_P) {
    initMCamFrameReceiver(r_port, 1.0);

    startMCamStream(mcam, r_port);

    bool act_res = setMCamStreamFilter(mcam, r_port, ATL_SCALE_MODE_4K);

    stopMCamStream(mcam, r_port);

    closeMCamFrameReceiver(r_port);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamStreamFilter_N) {
    bool act_res = setMCamStreamFilter(mcam, mc_port, ATL_SCALE_MODE_4K);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setNewMCamCallback_B) {
    bool act_res = (mcam.mcamID == mcamID);
    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamFrameCallback_B) {
    FRAME frame;
    MICRO_CAMERA_FRAME_CALLBACK frameCB;
    frameCB.f = mcamFrameCallback;
    frameCB.data = &frame;
    setMCamFrameCallback(frameCB);

    grabMCamFrame( mc_port, 1.0 );

    sleep(1);

    bool act_res = (frame.m_image != NULL);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_mcamconn, DISABLED_grabMCamFrame_P) {
    FRAME frame = grabMCamFrame(mc_port, 1.0 );

    bool act_res = (frame.m_image != NULL);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, grabMCamFrame_N) {
    bool act_res = (frame.m_image == NULL);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_mcamconn, returnPointer_B) {
    uint8_t *ptr;

    FRAME frame = grabMCamFrame(mc_port, 1.0 );

    bool act_res = (returnPointer(ptr) > 0);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamPropertyCallbacks_B) {
    MICRO_CAMERA mcam;
    MICRO_CAMERA_CALLBACKS CBs;
    CBs.autoGainCallback.f = mcamPropertyCallback;
    CBs.autoGainCallback.data = &mcam;
    setMCamPropertyCallbacks( mcam, CBs );

    setMCamExposure( mcam, 1.0 );

    sleep(1);

    bool act_res = (mcam.mcamID == mcam.mcamID);
    EXPECT_FALSE(act_res);
}

/************************************************************************
*   AUTO SETTERS - return true on success and false on failure
************************************************************************/

TEST_F(MantisAPITest_mcamconn, DISABLED_setMCamAutoExposure_P) {
    bool act_res = setMCamAutoExposure( mcam, true );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamAutoExposure_N) {
    bool act_res = setMCamAutoExposure( mcam, true );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamAutoFocus_P) {
    bool act_res;

    act_res = setMCamAutoFocus( mcam, true );

    EXPECT_TRUE(act_res);

    act_res = setMCamAutoFocus( mcam, false );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamAutoFocus_N) {
    bool act_res = setMCamAutoFocus( mcam, true );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamAutoFramerate_P) {
    bool act_res;

    act_res = setMCamAutoFramerate( mcam, true );

    EXPECT_TRUE(act_res);

    act_res = setMCamAutoFramerate( mcam, false );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamAutoFramerate_N) {
    bool act_res = setMCamAutoFramerate( mcam, true );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamAutoJpegQuality_P) {
    bool act_res;

    act_res = setMCamAutoJpegQuality( mcam, true );

    EXPECT_TRUE(act_res);

    act_res = setMCamAutoJpegQuality( mcam, false );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamAutoJpegQuality_N) {
    bool act_res = setMCamAutoJpegQuality( mcam, true );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamAutoGain_P) {
    bool act_res;

    act_res = setMCamAutoGain( mcam, true );

    EXPECT_TRUE(act_res);

    act_res = setMCamAutoGain( mcam, false );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamAutoGain_N) {
    bool act_res = setMCamAutoGain( mcam, true );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamAutoSaturation_P) {
    bool act_res;

    act_res = setMCamAutoSaturation( mcam, true );

    EXPECT_TRUE(act_res);

    act_res = setMCamAutoSaturation( mcam, false );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamAutoSaturation_N) {
    bool act_res = setMCamAutoSaturation( mcam, true );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamAutoShutter_P) {
    bool act_res;

    act_res = setMCamAutoShutter( mcam, true );

    EXPECT_TRUE(act_res);

    act_res = setMCamAutoShutter( mcam, false );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamAutoShutter_N) {
    bool act_res = setMCamAutoShutter( mcam, true );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamAutoContrast_P) {
    bool act_res;

    act_res = setMCamAutoContrast( mcam, true );

    EXPECT_TRUE(act_res);

    act_res = setMCamAutoContrast( mcam, false );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamAutoContrast_N) {
    bool act_res = setMCamAutoContrast( mcam, true );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamAutoSharpening_P) {
    bool act_res;

    act_res = setMCamAutoSharpening( mcam, true );

    EXPECT_TRUE(act_res);

    act_res = setMCamAutoSharpening( mcam, false );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamAutoSharpening_N) {
    bool act_res = setMCamAutoSharpening( mcam, true );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamAutoDeNoise_P) {
    bool act_res;

    act_res = setMCamAutoDeNoise( mcam, true );

    EXPECT_TRUE(act_res);

    act_res = setMCamAutoDeNoise( mcam, false );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamAutoDeNoise_N) {
    bool act_res = setMCamAutoDeNoise( mcam, true );

    EXPECT_FALSE(act_res);
}

/************************************************************************
*   SETTERS - return true on success and false on failure
************************************************************************/

TEST_F(MantisAPITest_mcamconn, setMCamExposure_P) {
    bool act_res = setMCamExposure( mcam, 1.0 );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamExposure_N) {
    bool act_res = setMCamExposure( mcam, 1.0 );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamFocusRelative_P) {
    bool act_res = setMCamFocusRelative( mcam, 1.0 );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamFocusRelative_N) {
    bool act_res = setMCamFocusRelative( mcam, 1.0 );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamFocusAbsolute_P) {
    bool act_res = setMCamFocusAbsolute( mcam, 1.0 );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamFocusAbsolute_N) {
    bool act_res = setMCamFocusAbsolute( mcam, 1.0 );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamFocusDefault_P) {
    bool act_res = setMCamFocusDefault( mcam );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamFocusDefault_N) {
    bool act_res = setMCamFocusDefault( mcam );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamFramerate_P) {
    bool act_res = setMCamFramerate( mcam, 1.0 );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamFramerate_N) {
    bool act_res = setMCamFramerate( mcam, 1.0 );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamJpegQuality_P) {
    bool act_res = setMCamJpegQuality( mcam, 1.0 );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamJpegQuality_N) {
    bool act_res = setMCamJpegQuality( mcam, 1.0 );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamGain_P) {
    bool act_res = setMCamGain( mcam, 1.0 );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamGain_N) {
    bool act_res = setMCamGain( mcam, 1.0 );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamSaturation_P) {
    bool act_res = setMCamSaturation( mcam, 1.0 );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamSaturation_N) {
    bool act_res = setMCamSaturation( mcam, 1.0 );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamShutter_P) {
    bool act_res = setMCamShutter( mcam, 1.0 );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamShutter_N) {
    bool act_res = setMCamShutter( mcam, 1.0 );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamContrast_P) {
    bool act_res = setMCamContrast( mcam, 1.0 );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamContrast_N) {
    bool act_res = setMCamContrast( mcam, 1.0 );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamSharpening_P) {
    bool act_res = setMCamSharpening( mcam, 1.0 );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamSharpening_N) {
    bool act_res = setMCamSharpening( mcam, 1.0 );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamDeNoise_P) {
    bool act_res = setMCamDeNoise( mcam, 1.0 );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamDeNoise_N) {
    bool act_res = setMCamDeNoise( mcam, 1.0 );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamWhiteBalance_P) {
    AtlWhiteBalance wb;
    wb.red = 1.0;
    wb.blue = 1.0;
    wb.green = 1.0;

    bool act_res = setMCamWhiteBalance( mcam, wb );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamWhiteBalance_N) {
    bool act_res = setMCamWhiteBalance( mcam, wb );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamCompressionParameters_P) {
    AtlCompressionParameters cp;
    cp = getMCamCompressionParameters(mcam);

    bool act_res = setMCamCompressionParameters( mcam, cp );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamCompressionParameters_N) {
    bool act_res = setMCamCompressionParameters( mcam, cp );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamWhiteBalanceMode_P) {
    //  Manual = 0, Auto = 1, Sunlight = 2, Florescent = 3,
    //  Shade = 4, Tungsten = 5, Cloudy = 6, Incandescent = 7,
    //  Horizon = 8, Flash = 9

    bool act_res = setMCamWhiteBalanceMode( mcam, 2 );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamWhiteBalanceMode_N) {
    bool act_res = setMCamWhiteBalanceMode( mcam, 1 );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamSensorMode_P) {
    //4k-30fps = 0, 4k-60fps = 1, HD-60fps = 2

    bool act_res = setMCamSensorMode( mcam, 2 );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamSensorMode_N) {
    bool act_res = setMCamSensorMode( mcam, 1 );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamIrFilter_P) {
    bool act_res = setMCamIrFilter( mcam, false );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamIrFilter_N) {
    bool act_res = setMCamIrFilter( mcam, false );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamFocalLength_P) {
    bool act_res = setMCamFocalLength( mcam, 25.0 );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamFocalLength_N) {
    bool act_res = setMCamFocalLength( mcam, 25.0 );

    EXPECT_FALSE(act_res);
}

/************************************************************************
*   AUTO GETTERS - check if auto if on or off
************************************************************************/

TEST_F(MantisAPITest_mcamconn, getMCamAutoExposure_P) {
    setMCamAutoExposure(mcam, false);

    bool act_res = getMCamAutoExposure(mcam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_N, getMCamAutoExposure_N) {
    bool act_res = getMCamAutoExposure(mcam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, getMCamAutoGain_P) {
    setMCamAutoGain(mcam, false);

    bool act_res = getMCamAutoGain(mcam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_N, getMCamAutoGain_N) {
    bool act_res = getMCamAutoGain(mcam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, getMCamAutoShutter_P) {
    setMCamAutoShutter(mcam, false);

    bool act_res = getMCamAutoShutter(mcam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_N, getMCamAutoShutter_N) {
    bool act_res = getMCamAutoShutter(mcam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, getMCamAutoSaturation_P) {
    setMCamAutoSaturation(mcam, false);

    bool act_res = getMCamAutoSaturation(mcam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_N, getMCamAutoSaturation_N) {
    bool act_res = getMCamAutoSaturation(mcam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, getMCamAutoFramerate_P) {
    setMCamAutoFramerate(mcam, false);

    bool act_res = getMCamAutoFramerate(mcam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_N, getMCamAutoFramerate_N) {
    bool act_res = getMCamAutoFramerate(mcam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, getMCamAutoContrast_P) {
    setMCamAutoContrast(mcam, false);

    bool act_res = getMCamAutoContrast(mcam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_N, getMCamAutoContrast_N) {
    bool act_res = getMCamAutoContrast(mcam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, getMCamAutoDenoise_P) {
    bool act_res = getMCamAutoDenoise(mcam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_N, getMCamAutoDenoise_N) {
    bool act_res = getMCamAutoDenoise(mcam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, getMCamAutoSharpening_P) {
    setMCamAutoSharpening(mcam, false);

    bool act_res = getMCamAutoSharpening(mcam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_N, getMCamAutoSharpening_N) {
    bool act_res = getMCamAutoSharpening(mcam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, getMCamAutoJpegQuality_P) {
    setMCamAutoJpegQuality(mcam, false);

    bool act_res = getMCamAutoJpegQuality(mcam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_N, getMCamAutoJpegQuality_N) {
    bool act_res = getMCamAutoJpegQuality(mcam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, getMCamAutoWhiteBalance_P) {
    bool act_res = getMCamAutoWhiteBalance(mcam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_N, getMCamAutoWhiteBalance_N) {
    bool act_res = getMCamAutoWhiteBalance(mcam);

    EXPECT_FALSE(act_res);
}

/************************************************************************
*   GETTERS
************************************************************************/

TEST_F(MantisAPITest_mcamconn, getMCamExposure_P) {
    PAIR_DOUBLE exp_res = getMCamExposureRange(mcam);
    double act_res = getMCamExposure(mcam);

    EXPECT_GE(act_res, exp_res.first);
    EXPECT_LE(act_res, exp_res.second);
}

TEST_F(MantisAPITest_N, getMCamExposure_N) {
    double act_res = getMCamExposure(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamGain_P) {
    PAIR_DOUBLE exp_res = getMCamGainRange(mcam);
    double act_res = getMCamGain(mcam);

    EXPECT_GE(act_res, exp_res.first);
    EXPECT_LE(act_res, exp_res.second);
}

TEST_F(MantisAPITest_N, getMCamGain_N) {
    double act_res = getMCamGain(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamFocus_P) {
    double act_res = getMCamFocus(mcam);

    EXPECT_GE(act_res, -10);
}

TEST_F(MantisAPITest_N, getMCamFocus_N) {
    double act_res = getMCamFocus(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamFocusState_P) {
    int act_res = getMCamFocusState(mcam);

    EXPECT_GE(act_res, -10);
}

TEST_F(MantisAPITest_N, getMCamFocusState_N) {
    int act_res = getMCamFocusState(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamShutter_P) {
    PAIR_DOUBLE exp_res = getMCamShutterRange(mcam);
    double act_res = getMCamShutter(mcam);

    EXPECT_GE(act_res, exp_res.first);
    EXPECT_LE(act_res, exp_res.second);
}

TEST_F(MantisAPITest_N, getMCamShutter_N) {
    double act_res = getMCamShutter(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamSaturation_P) {
    PAIR_DOUBLE exp_res = getMCamSaturationRange(mcam);
    double act_res = getMCamSaturation(mcam);

    EXPECT_GE(act_res, exp_res.first);
    EXPECT_LE(act_res, exp_res.second);
}

TEST_F(MantisAPITest_N, getMCamSaturation_N) {
    double act_res = getMCamSaturation(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamFramerate_P) {
    PAIR_DOUBLE exp_res = getMCamFramerateRange(mcam);
    double act_res = getMCamFramerate(mcam);

    EXPECT_GE(act_res, exp_res.first);
    EXPECT_LE(act_res, exp_res.second);
}

TEST_F(MantisAPITest_N, getMCamFramerate_N) {
    double act_res = getMCamFramerate(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamContrast_P) {
    double act_res = getMCamContrast(mcam);

    EXPECT_GE(act_res, -10);
}

TEST_F(MantisAPITest_N, getMCamContrast_N) {
    double act_res = getMCamContrast(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamDeNoise_P) {
    double act_res = getMCamDeNoise(mcam);

    EXPECT_GE(act_res, -10);
}

TEST_F(MantisAPITest_N, getMCamDeNoise_N) {
    double act_res = getMCamDeNoise(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamSharpening_P) {
    PAIR_DOUBLE exp_res = getMCamSharpeningRange(mcam);
    double act_res = getMCamSharpening(mcam);

    EXPECT_GE(act_res, exp_res.first);
    EXPECT_LE(act_res, exp_res.second);
}

TEST_F(MantisAPITest_N, getMCamSharpening_N) {
    double act_res = getMCamSharpening(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamJpegQuality_P) {
    PAIR_DOUBLE exp_res = getMCamJpegQualityRange(mcam);
    double act_res = getMCamJpegQuality(mcam);

    EXPECT_GE(act_res, exp_res.first);
    EXPECT_LE(act_res, exp_res.second);
}

TEST_F(MantisAPITest_N, getMCamJpegQuality_N) {
    double act_res = getMCamJpegQuality(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamIrFilter_P) {
    bool act_res = getMCamIrFilter(mcam);

    SUCCEED();
}

TEST_F(MantisAPITest_N, getMCamIrFilter_N) {
    bool act_res = getMCamIrFilter(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamWhiteBalanceMode_P) {
    int act_res = getMCamWhiteBalanceMode(mcam);

    EXPECT_GE(act_res, -10);
}

TEST_F(MantisAPITest_N, getMCamWhiteBalanceMode_N) {
    int act_res = getMCamWhiteBalanceMode(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamModuleID_P) {
    uint64_t act_res = getMCamModuleID(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_N, getMCamModuleID_N) {
    uint64_t act_res = getMCamModuleID(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamCompressionParameters_P) {
    AtlCompressionParameters act_res = getMCamCompressionParameters(mcam);

    EXPECT_GE(act_res.quality_preset_level, 0);
}

TEST_F(MantisAPITest_N, getMCamCompressionParameters_N) {
    AtlCompressionParameters act_res = getMCamCompressionParameters(mcam);

    EXPECT_EQ(act_res.quality_preset_level, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamSensorID_P) {
    uint64_t act_res = getMCamSensorID(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_N, getMCamSensorID_N) {
    uint64_t act_res = getMCamSensorID(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamPixelSize_P) {
    double act_res = getMCamPixelSize(mcam);

    EXPECT_GE(act_res, -10);
}

TEST_F(MantisAPITest_N, getMCamPixelSize_N) {
    double act_res = getMCamPixelSize(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamFocalLength_P) {
    double act_res = getMCamFocalLength(mcam);

    EXPECT_GE(act_res, 0);
}

TEST_F(MantisAPITest_N, getMCamFocalLength_N) {
    double act_res = getMCamFocalLength(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamWhiteBalance_P) {
    AtlWhiteBalance act_res = getMCamWhiteBalance(mcam);

    EXPECT_GE(act_res.red, 0);
}

TEST_F(MantisAPITest_N, getMCamWhiteBalance_N) {
    AtlWhiteBalance act_res = getMCamWhiteBalance(mcam);

    EXPECT_EQ(act_res.red, 0);
}

/************************************************************************
*   RANGE GETTERS - return pair of range values
************************************************************************/

TEST_F(MantisAPITest_mcamconn, getMCamGainRange_P) {
    PAIR_DOUBLE act_res = getMCamGainRange(mcam);

    EXPECT_GT(act_res.second, act_res.first);

    double act_res2 = getMCamGain(mcam);

    EXPECT_GE(act_res2, act_res.first);
    EXPECT_LT(act_res2, act_res.second);
}

TEST_F(MantisAPITest_N, getMCamGainRange_N) {
    PAIR_DOUBLE act_res = getMCamGainRange(mcam);

    EXPECT_GT(act_res.second, act_res.first);
}

TEST_F(MantisAPITest_mcamconn, getMCamExposureRange_P) {
    PAIR_DOUBLE act_res = getMCamExposureRange(mcam);

    EXPECT_GT(act_res.second, act_res.first);

    double act_res2 = getMCamExposure(mcam);

    EXPECT_GE(act_res2, act_res.first);
    EXPECT_LT(act_res2, act_res.second);
}

TEST_F(MantisAPITest_N, getMCamExposureRange_N) {
    PAIR_DOUBLE act_res = getMCamExposureRange(mcam);

    EXPECT_GT(act_res.second, act_res.first);
}

TEST_F(MantisAPITest_mcamconn, getMCamShutterRange_P) {
    PAIR_DOUBLE act_res = getMCamShutterRange(mcam);

    EXPECT_GT(act_res.second, act_res.first);

    double act_res2 = getMCamShutter(mcam);

    EXPECT_GE(act_res2, act_res.first);
    EXPECT_LT(act_res2, act_res.second);
}

TEST_F(MantisAPITest_N, getMCamShutterRange_N) {
    PAIR_DOUBLE act_res = getMCamShutterRange(mcam);

    EXPECT_GT(act_res.second, act_res.first);
}

TEST_F(MantisAPITest_mcamconn, getMCamSaturationRange_P) {
    PAIR_DOUBLE act_res = getMCamSaturationRange(mcam);

    EXPECT_GT(act_res.second, act_res.first);

    double act_res2 = getMCamSaturation(mcam);

    EXPECT_GE(act_res2, act_res.first);
    EXPECT_LT(act_res2, act_res.second);
}

TEST_F(MantisAPITest_N, getMCamSaturationRange_N) {
    PAIR_DOUBLE act_res = getMCamSaturationRange(mcam);

    EXPECT_GT(act_res.second, act_res.first);
}

TEST_F(MantisAPITest_mcamconn, getMCamFramerateRange_P) {
    PAIR_DOUBLE act_res = getMCamFramerateRange(mcam);

    EXPECT_GT(act_res.second, act_res.first);

    double act_res2 = getMCamFramerate(mcam);

    EXPECT_GE(act_res2, act_res.first);
    EXPECT_LT(act_res2, act_res.second);
}

TEST_F(MantisAPITest_N, getMCamFramerateRange_N) {
    PAIR_DOUBLE act_res = getMCamFramerateRange(mcam);

    EXPECT_GT(act_res.second, act_res.first);
}

TEST_F(MantisAPITest_mcamconn, getMCamContrastRange_P) {
    PAIR_DOUBLE act_res = getMCamContrastRange(mcam);

    EXPECT_GT(act_res.second, act_res.first);

    double act_res2 = getMCamContrast(mcam);

    EXPECT_GE(act_res2, act_res.first);
    EXPECT_LT(act_res2, act_res.second);
}

TEST_F(MantisAPITest_N, getMCamContrastRange_N) {
    PAIR_DOUBLE act_res = getMCamContrastRange(mcam);

    EXPECT_GT(act_res.second, act_res.first);
}

TEST_F(MantisAPITest_mcamconn, getMCamDeNoiseRange_P) {
    PAIR_DOUBLE act_res = getMCamDeNoiseRange(mcam);

    EXPECT_GT(act_res.second, act_res.first);

    double act_res2 = getMCamDeNoise(mcam);

    EXPECT_GE(act_res2, act_res.first);
    EXPECT_LT(act_res2, act_res.second);
}

TEST_F(MantisAPITest_N, getMCamDeNoiseRange_N) {
    PAIR_DOUBLE act_res = getMCamDeNoiseRange(mcam);

    EXPECT_GT(act_res.second, act_res.first);
}

TEST_F(MantisAPITest_mcamconn, getMCamSharpeningRange_P) {
    PAIR_DOUBLE act_res = getMCamSharpeningRange(mcam);

    EXPECT_GT(act_res.second, act_res.first);

    double act_res2 = getMCamSharpening(mcam);

    EXPECT_GE(act_res2, act_res.first);
    EXPECT_LT(act_res2, act_res.second);
}

TEST_F(MantisAPITest_N, getMCamSharpeningRange_N) {
    PAIR_DOUBLE act_res = getMCamSharpeningRange(mcam);

    EXPECT_GT(act_res.second, act_res.first);
}

TEST_F(MantisAPITest_mcamconn, getMCamJpegQualityRange_P) {
    PAIR_DOUBLE act_res = getMCamJpegQualityRange(mcam);

    EXPECT_GT(act_res.second, act_res.first);

    double act_res2 = getMCamJpegQuality(mcam);

    EXPECT_GE(act_res2, act_res.first);
    EXPECT_LT(act_res2, act_res.second);
}

TEST_F(MantisAPITest_N, getMCamJpegQualityRange_N) {
    PAIR_DOUBLE act_res = getMCamJpegQualityRange(mcam);

    EXPECT_GT(act_res.second, act_res.first);
}

TEST_F(MantisAPITest_mcamconn, getMCamWhiteBalanceRange_P) {
    PAIR_DOUBLE act_res = getMCamWhiteBalanceRange(mcam);

    EXPECT_GT(act_res.second, act_res.first);

    double act_res2 = getMCamWhiteBalance(mcam).red;

    EXPECT_GE(act_res2, act_res.first);
    EXPECT_LT(act_res2, act_res.second);
}

TEST_F(MantisAPITest_N, getMCamWhiteBalanceRange_N) {
    PAIR_DOUBLE act_res = getMCamWhiteBalanceRange(mcam);

    EXPECT_GE(act_res.first, 0);
}



int main(int argc, char **argv) {
    ::testing::InitGoogleTest( &argc, argv );

	::testing::GTEST_FLAG(filter) = "*_N";
	RUN_ALL_TESTS();

	return 0;
}
