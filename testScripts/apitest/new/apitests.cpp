#include "apitest.h"

/*************************************************************
* Configuration and Setup
*************************************************************/

TEST_F(MantisAPITest, connectToCameraServer_P) {
	AQ_SYSTEM_STATE act_res = isConnectedToCameraServer();

    EXPECT_EQ(act_res, AQ_SERVER_CONNECTED);
}

TEST_F(MantisAPITest_N, connectToCameraServer_N) {
    AQ_RETURN_CODE act_res = connectToCameraServer(tp->ip, tp->port);

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
	connectToCameraServer(tp->ip, tp->port);

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

	setCameraConnection(tp->cam, true, 10);

	act_res = isCameraConnected(tp->cam);

	EXPECT_EQ(act_res, AQ_CAMERA_CONNECTED);

    setCameraConnection(tp->cam, false, 10);

    act_res = isCameraConnected(tp->cam);

    EXPECT_EQ(act_res, AQ_CAMERA_DISCONNECTED);
}

TEST_F(MantisAPITest_N, isCameraConnected_N) {
	AQ_SYSTEM_STATE act_res = isCameraConnected(tp->cam);

	EXPECT_EQ(act_res, AQ_STATE_UNKNOWABLE);
}

TEST_F(MantisAPITest, setCameraConnection_P) {
    setCameraConnection(tp->cam, true, 10);

    AQ_SYSTEM_STATE act_res;

    act_res = isCameraConnected(tp->cam);

    EXPECT_EQ(act_res, AQ_CAMERA_CONNECTED);

    setCameraConnection(tp->cam, false, 10);

    act_res = isCameraConnected(tp->cam);

    EXPECT_EQ(act_res, AQ_CAMERA_DISCONNECTED);
}

TEST_F(MantisAPITest_N, setCameraConnection_N) {
    setCameraConnection(tp->cam, true, 10);

    AQ_SYSTEM_STATE act_res = isCameraConnected(tp->cam);

    EXPECT_EQ(act_res, AQ_STATE_UNKNOWABLE);
}

TEST_F(MantisAPITest, disconnectCamera_P) {
	disconnectCamera(tp->cam);

    AQ_SYSTEM_STATE act_res = isCameraConnected(tp->cam);

    EXPECT_EQ(act_res, AQ_CAMERA_DISCONNECTED);

    act_res = isConnectedToCameraServer();

    EXPECT_EQ(act_res, AQ_SERVER_CONNECTED);
}

TEST_F(MantisAPITest_N, disconnectCamera_N) {
	AQ_SYSTEM_STATE act_res = isCameraConnected(tp->cam);

    EXPECT_EQ(act_res, AQ_STATE_UNKNOWABLE);
}

TEST_F(MantisAPITest_B, setNewCameraCallback_B) {
	connectToCameraServer(tp->ip, tp->port);

	ACOS_CAMERA cam;
	NEW_CAMERA_CALLBACK camCB;
	camCB.f = newCameraCallback;
	camCB.data = &cam;
	setNewCameraCallback(camCB);

	uint32_t act_res = cam.camID;

	disconnectFromCameraServer();

    EXPECT_EQ(act_res, tp->camID);
}

TEST_F(MantisAPITest_B, setCameraDeletedCallback_B) {
	connectToCameraServer(tp->ip, tp->port);

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

    EXPECT_EQ(tp->camID, tp->camID); //incorrect val
}

TEST_F(MantisAPITest, getNumberOfCameras_P) {
    uint32_t act_res = getNumberOfCameras();

    ASSERT_EQ(act_res, tp->numCams);
}

TEST_F(MantisAPITest_N, getNumberOfCameras_N) {
    uint32_t act_res = getNumberOfCameras();

    ASSERT_EQ(act_res, tp->numCams);
}

TEST_F(MantisAPITest_B, setCameraPropertyCallbacks_B) {
	connectToCameraServer(tp->ip, tp->port);

	ACOS_CAMERA cam;
    CAMERA_CALLBACKS cbs;
    cbs.cameraConnectionCallback.f = cameraPropertyCallback;
    cbs.cameraConnectionCallback.data = &cam;

    cbs.dataFlowStatusCallback.f = cameraPropertyCallback;
    cbs.dataFlowStatusCallback.data = &cam;

    setCameraPropertyCallbacks(cbs);

    sleep(1);

    bool act_res = (cam.camID == tp->camID);

    disconnectFromCameraServer();

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_camconn, getCameraNumberOfMCams_P) {
    uint32_t act_res = getCameraNumberOfMCams(tp->cam);

    EXPECT_EQ(act_res, tp->numMCams);
}

TEST_F(MantisAPITest_N, getCameraNumberOfMCams_N) {
    uint32_t act_res = getCameraNumberOfMCams(tp->cam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest, getCameraMCamList_P_DISABLED) {
	connectToCameraServer(tp->ip, tp->port);

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
    getCameraMCamList(tp->cam, tp->mcamList, tp->numMCams);

    bool act_res = (tp->mcamList == NULL);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_camconn, getCameraInfo_P) {
    CAMERA_INFO act_res = getCameraInfo(tp->cam);

    EXPECT_EQ(act_res.serialNumber, 1234);
}

TEST_F(MantisAPITest_N, getCameraInfo_N) {
    CAMERA_INFO act_res = getCameraInfo(tp->cam);

    EXPECT_EQ(act_res.serialNumber, 1234);
}

/*********************************************************************
 * Data Interface
 *********************************************************************/

TEST_F(MantisAPITest_camconn, isCameraReceivingData_P) {
	setCameraReceivingData(tp->cam ,true, 10);

	AQ_SYSTEM_STATE act_res;

	act_res = isCameraReceivingData(tp->cam);

    EXPECT_EQ(act_res, AQ_CAMERA_RECEIVING_DATA);

    setCameraReceivingData(tp->cam ,false, 10);

    act_res = isCameraReceivingData(tp->cam);

    EXPECT_EQ(act_res, AQ_CAMERA_NOT_RECEIVING_DATA);
}

TEST_F(MantisAPITest_N, isCameraReceivingData_N) {
    AQ_SYSTEM_STATE act_res = isCameraReceivingData(tp->cam);

    EXPECT_EQ(act_res, AQ_STATE_UNKNOWABLE);
}

TEST_F(MantisAPITest_camconn, setCameraReceivingData_P) {
    AQ_RETURN_CODE act_res = setCameraReceivingData(tp->cam, true, 10);

    setCameraReceivingData(tp->cam, false, 10);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_N,  setCameraReceivingData_N) {
    AQ_RETURN_CODE act_res = setCameraReceivingData(tp->cam, true, 1);

    EXPECT_NE(act_res, 0);
}

TEST_F(MantisAPITest_camconn, getFrame_P) {
	setCameraReceivingData(tp->cam, true, 5);

	sleep(1);

	FRAME frame = getFrame(tp->cam,
						   tp->cam.mcamList.mcams[0].mcamID,
						   0,
						   ATL_TILING_1_1_2,
						   ATL_TILE_4K);

	bool act_res = (frame.m_image != NULL);

	setCameraReceivingData(tp->cam, false, 5);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, getFrame_N) {
    FRAME frame = getFrame(tp->cam,
                           tp->mcam.mcamID,
                           0,
                           ATL_TILING_1_1_2,
                           ATL_TILE_4K);

    bool act_res = (frame.m_image != NULL);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest, saveFrame_P) {
	setCameraReceivingData(tp->cam, true, 5);

	sleep(1);

	FRAME frame = getFrame(tp->cam,
						   tp->cam.mcamList.mcams[0].mcamID,
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

	setCameraReceivingData(tp->cam, false, 5);
}

TEST_F(MantisAPITest_N, saveFrame_N) {
    FRAME frame;

    saveFrame(frame, "test_frame_N");

    bool act_res = fileExists("test_frame_N.jpeg");

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_B, setLatestTimeCallback_B) {
	connectToCameraServer(tp->ip, tp->port);

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

    bool act_res = (cam.camID == tp->camID);

    disconnectFromCameraServer();

    EXPECT_TRUE(act_res);
}



int main(int argc, char **argv) {
    ::testing::InitGoogleTest( &argc, argv );
	::testing::GTEST_FLAG(filter) = "*_P";
	RUN_ALL_TESTS();
	::testing::GTEST_FLAG(filter) = "*_B";
	RUN_ALL_TESTS();
	::testing::GTEST_FLAG(filter) = "*_N";
	RUN_ALL_TESTS();

	return 0;
}
