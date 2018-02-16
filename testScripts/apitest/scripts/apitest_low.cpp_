#include "apitest.h"

void newMCamCallback(MICRO_CAMERA mcam, void* data)
{
    MICRO_CAMERA* _mcam = (MICRO_CAMERA*) data;
    *_mcam = mcam;
}

void mcamFrameCallback(FRAME frame, void* data)
{
    FRAME* _frame = (FRAME*) data;
    *_frame = frame;
}

void mcamPropertyCallback(MICRO_CAMERA mcam, void* data, bool o, bool n)
{
	MICRO_CAMERA* _mcam = (MICRO_CAMERA*) data;
    *_mcam = mcam;
}

void MantisAPITest_mcamconn::SetUp() {
	tp = new TestParams();

	if (getNumberOfMCams() == 0) {
		mCamConnect(tp->mc_ip, tp->mc_port);
	}

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

TEST_F(MantisAPITest_mcamconn, mCamDisconnect_P) {
    mCamDisconnect(tp->mc_ip, tp->mc_port);
    EXPECT_EQ(1,1);
}

TEST_F(MantisAPITest_N, mCamDisconnect_N) {
    mCamDisconnect(mc_ip, mc_port);
    EXPECT_EQ(1,1);
}

TEST_F(MantisAPITest_mcamconn, initMCamFrameReceiver_P) {
    bool act_res = initMCamFrameReceiver( tp->r_port, 1 );
    closeMCamFrameReceiver(tp->r_port);
    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, initMCamFrameReceiver_N) {
    bool act_res = initMCamFrameReceiver( 66666, 1 );
    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, closeMCamFrameReceiver_P) {
	initMCamFrameReceiver( tp->r_port, 1 );

	bool act_res = closeMCamFrameReceiver(tp->r_port);
    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, closeMCamFrameReceiver_N) {
    bool act_res = closeMCamFrameReceiver(66666);
    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, getNumberOfMCams_P) {
    uint32_t act_res = getNumberOfMCams();
    EXPECT_EQ(act_res, tp->numMCams);
}

TEST_F(MantisAPITest_N, getNumberOfMCams_N) {
    uint32_t act_res = getNumberOfMCams();
    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, startMCamStream_P) {
	initMCamFrameReceiver(tp->r_port, 1.0);

	bool act_res = startMCamStream(tp->mcam, tp->r_port);

	stopMCamStream(tp->mcam, tp->r_port);

	closeMCamFrameReceiver(tp->r_port);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, startMCamStream_N) {
    bool act_res = startMCamStream(mcam, r_port);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, stopMCamStream_P) {
	initMCamFrameReceiver(tp->r_port, 1.0);

    startMCamStream(tp->mcam, tp->r_port);

    bool act_res = stopMCamStream(tp->mcam, tp->r_port);

    closeMCamFrameReceiver(tp->r_port);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, stopMCamStream_N) {
    bool act_res = stopMCamStream(mcam, r_port);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamStreamFilter_P) {
	initMCamFrameReceiver(tp->r_port, 1.0);

	startMCamStream(tp->mcam, tp->r_port);

    bool act_res = setMCamStreamFilter(tp->mcam, tp->r_port, ATL_SCALE_MODE_4K);

    stopMCamStream(tp->mcam, tp->r_port);

    closeMCamFrameReceiver(tp->r_port);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamStreamFilter_N) {
    bool act_res = setMCamStreamFilter(mcam, mc_port, ATL_SCALE_MODE_4K);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setNewMCamCallback_B) {
    bool act_res = (tp->mcam.mcamID == tp->mcamID);
    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamFrameCallback_B) {
    FRAME frame;
    MICRO_CAMERA_FRAME_CALLBACK frameCB;
    frameCB.f = mcamFrameCallback;
    frameCB.data = &frame;
    setMCamFrameCallback(frameCB);

    grabMCamFrame( tp->mc_port, 1.0 );

    sleep(1);

    bool act_res = (frame.m_image != NULL);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_mcamconn, DISABLED_grabMCamFrame_P) {
	FRAME frame = grabMCamFrame(tp->mc_port, 1.0 );

    bool act_res = (frame.m_image != NULL);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, grabMCamFrame_N) {
    bool act_res = (frame.m_image == NULL);

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_mcamconn, returnPointer_B) {
    uint8_t *ptr;

    FRAME frame = grabMCamFrame(tp->mc_port, 1.0 );

    bool act_res = (returnPointer(ptr) > 0);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamPropertyCallbacks_B) {
    MICRO_CAMERA mcam;
    MICRO_CAMERA_CALLBACKS CBs;
    CBs.autoGainCallback.f = mcamPropertyCallback;
    CBs.autoGainCallback.data = &mcam;
    setMCamPropertyCallbacks( tp->mcam, CBs );

    setMCamExposure( tp->mcam, 1.0 );

    sleep(1);

    bool act_res = (mcam.mcamID == tp->mcam.mcamID);
    EXPECT_FALSE(act_res);
}

/************************************************************************
*   AUTO SETTERS - return true on success and false on failure
************************************************************************/

TEST_F(MantisAPITest_mcamconn, setMCamAutoExposure_P) {
    bool act_res = setMCamAutoExposure( tp->mcam, true );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamAutoExposure_N) {
    bool act_res = setMCamAutoExposure( mcam, true );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamAutoFocus_P) {
    bool act_res;

    act_res = setMCamAutoFocus( tp->mcam, true );

    EXPECT_TRUE(act_res);

    act_res = setMCamAutoFocus( tp->mcam, false );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamAutoFocus_N) {
    bool act_res = setMCamAutoFocus( mcam, true );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamAutoFramerate_P) {
    bool act_res;

    act_res = setMCamAutoFramerate( tp->mcam, true );

    EXPECT_TRUE(act_res);

    act_res = setMCamAutoFramerate( tp->mcam, false );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamAutoFramerate_N) {
    bool act_res = setMCamAutoFramerate( mcam, true );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamAutoJpegQuality_P) {
    bool act_res;

    act_res = setMCamAutoJpegQuality( tp->mcam, true );

    EXPECT_TRUE(act_res);

    act_res = setMCamAutoJpegQuality( tp->mcam, false );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamAutoJpegQuality_N) {
    bool act_res = setMCamAutoJpegQuality( mcam, true );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamAutoGain_P) {
    bool act_res;

    act_res = setMCamAutoGain( tp->mcam, true );

    EXPECT_TRUE(act_res);

    act_res = setMCamAutoGain( tp->mcam, false );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamAutoGain_N) {
    bool act_res = setMCamAutoGain( mcam, true );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamAutoSaturation_P) {
    bool act_res;

    act_res = setMCamAutoSaturation( tp->mcam, true );

    EXPECT_TRUE(act_res);

    act_res = setMCamAutoSaturation( tp->mcam, false );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamAutoSaturation_N) {
    bool act_res = setMCamAutoSaturation( mcam, true );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamAutoShutter_P) {
    bool act_res;

    act_res = setMCamAutoShutter( tp->mcam, true );

    EXPECT_TRUE(act_res);

    act_res = setMCamAutoShutter( tp->mcam, false );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamAutoShutter_N) {
    bool act_res = setMCamAutoShutter( mcam, true );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamAutoContrast_P) {
    bool act_res;

    act_res = setMCamAutoContrast( tp->mcam, true );

    EXPECT_TRUE(act_res);

    act_res = setMCamAutoContrast( tp->mcam, false );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamAutoContrast_N) {
    bool act_res = setMCamAutoContrast( mcam, true );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamAutoSharpening_P) {
    bool act_res;

    act_res = setMCamAutoSharpening( tp->mcam, true );

    EXPECT_TRUE(act_res);

    act_res = setMCamAutoSharpening( tp->mcam, false );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamAutoSharpening_N) {
    bool act_res = setMCamAutoSharpening( mcam, true );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamAutoDeNoise_P) {
    bool act_res;

    act_res = setMCamAutoDeNoise( tp->mcam, true );

    EXPECT_TRUE(act_res);

    act_res = setMCamAutoDeNoise( tp->mcam, false );

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
    bool act_res = setMCamExposure( tp->mcam, 1.0 );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamExposure_N) {
    bool act_res = setMCamExposure( mcam, 1.0 );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamFocusRelative_P) {
    bool act_res = setMCamFocusRelative( tp->mcam, 1.0 );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamFocusRelative_N) {
    bool act_res = setMCamFocusRelative( mcam, 1.0 );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamFocusAbsolute_P) {
    bool act_res = setMCamFocusAbsolute( tp->mcam, 1.0 );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamFocusAbsolute_N) {
    bool act_res = setMCamFocusAbsolute( mcam, 1.0 );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamFocusDefault_P) {
    bool act_res = setMCamFocusDefault( tp->mcam );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamFocusDefault_N) {
    bool act_res = setMCamFocusDefault( mcam );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamFramerate_P) {
    bool act_res = setMCamFramerate( tp->mcam, 1.0 );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamFramerate_N) {
    bool act_res = setMCamFramerate( mcam, 1.0 );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamJpegQuality_P) {
    bool act_res = setMCamJpegQuality( tp->mcam, 1.0 );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamJpegQuality_N) {
    bool act_res = setMCamJpegQuality( mcam, 1.0 );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamGain_P) {
    bool act_res = setMCamGain( tp->mcam, 1.0 );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamGain_N) {
    bool act_res = setMCamGain( mcam, 1.0 );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamSaturation_P) {
    bool act_res = setMCamSaturation( tp->mcam, 1.0 );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamSaturation_N) {
    bool act_res = setMCamSaturation( mcam, 1.0 );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamShutter_P) {
    bool act_res = setMCamShutter( tp->mcam, 1.0 );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamShutter_N) {
    bool act_res = setMCamShutter( mcam, 1.0 );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamContrast_P) {
    bool act_res = setMCamContrast( tp->mcam, 1.0 );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamContrast_N) {
    bool act_res = setMCamContrast( mcam, 1.0 );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamSharpening_P) {
    bool act_res = setMCamSharpening( tp->mcam, 1.0 );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamSharpening_N) {
    bool act_res = setMCamSharpening( mcam, 1.0 );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamDeNoise_P) {
    bool act_res = setMCamDeNoise( tp->mcam, 1.0 );

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

    bool act_res = setMCamWhiteBalance( tp->mcam, wb );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamWhiteBalance_N) {
    bool act_res = setMCamWhiteBalance( mcam, wb );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamCompressionParameters_P) {
    AtlCompressionParameters cp;
    cp = getMCamCompressionParameters(tp->mcam);

    bool act_res = setMCamCompressionParameters( tp->mcam, cp );

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

    bool act_res = setMCamWhiteBalanceMode( tp->mcam, 2 );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamWhiteBalanceMode_N) {
    bool act_res = setMCamWhiteBalanceMode( mcam, 1 );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamSensorMode_P) {
    //4k-30fps = 0, 4k-60fps = 1, HD-60fps = 2

    bool act_res = setMCamSensorMode( tp->mcam, 2 );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamSensorMode_N) {
    bool act_res = setMCamSensorMode( mcam, 1 );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamIrFilter_P) {
    bool act_res = setMCamIrFilter( tp->mcam, false );

    EXPECT_TRUE(act_res);
}

TEST_F(MantisAPITest_N, setMCamIrFilter_N) {
    bool act_res = setMCamIrFilter( mcam, false );

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, setMCamFocalLength_P) {
    bool act_res = setMCamFocalLength( tp->mcam, 25.0 );

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
	setMCamAutoExposure(tp->mcam, false);

	bool act_res = getMCamAutoExposure(tp->mcam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_N, getMCamAutoExposure_N) {
    bool act_res = getMCamAutoExposure(mcam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, getMCamAutoGain_P) {
	setMCamAutoGain(tp->mcam, false);

    bool act_res = getMCamAutoGain(tp->mcam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_N, getMCamAutoGain_N) {
    bool act_res = getMCamAutoGain(mcam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, getMCamAutoShutter_P) {
	setMCamAutoShutter(tp->mcam, false);

	bool act_res = getMCamAutoShutter(tp->mcam);

	EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_N, getMCamAutoShutter_N) {
	bool act_res = getMCamAutoShutter(mcam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, getMCamAutoSaturation_P) {
	setMCamAutoSaturation(tp->mcam, false);

	bool act_res = getMCamAutoSaturation(tp->mcam);

	EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_N, getMCamAutoSaturation_N) {
    bool act_res = getMCamAutoSaturation(mcam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, getMCamAutoFramerate_P) {
	setMCamAutoFramerate(tp->mcam, false);

	bool act_res = getMCamAutoFramerate(tp->mcam);

	EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_N, getMCamAutoFramerate_N) {
    bool act_res = getMCamAutoFramerate(mcam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, getMCamAutoContrast_P) {
	setMCamAutoContrast(tp->mcam, false);

	bool act_res = getMCamAutoContrast(tp->mcam);

	EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_N, getMCamAutoContrast_N) {
    bool act_res = getMCamAutoContrast(mcam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, getMCamAutoDenoise_P) {
    bool act_res = getMCamAutoDenoise(tp->mcam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_N, getMCamAutoDenoise_N) {
    bool act_res = getMCamAutoDenoise(mcam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, getMCamAutoSharpening_P) {
	setMCamAutoSharpening(tp->mcam, false);

	bool act_res = getMCamAutoSharpening(tp->mcam);

	EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_N, getMCamAutoSharpening_N) {
    bool act_res = getMCamAutoSharpening(mcam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, getMCamAutoJpegQuality_P) {
	setMCamAutoJpegQuality(tp->mcam, false);

	bool act_res = getMCamAutoJpegQuality(tp->mcam);

	EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_N, getMCamAutoJpegQuality_N) {
    bool act_res = getMCamAutoJpegQuality(mcam);

    EXPECT_FALSE(act_res);
}

TEST_F(MantisAPITest_mcamconn, getMCamAutoWhiteBalance_P) {
	bool act_res = getMCamAutoWhiteBalance(tp->mcam);

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
	PAIR_DOUBLE exp_res = getMCamExposureRange(tp->mcam);
	double act_res = getMCamExposure(tp->mcam);

    EXPECT_GE(act_res, exp_res.first);
    EXPECT_LE(act_res, exp_res.second);
}

TEST_F(MantisAPITest_N, getMCamExposure_N) {
    double act_res = getMCamExposure(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamGain_P) {
	PAIR_DOUBLE exp_res = getMCamGainRange(tp->mcam);
	double act_res = getMCamGain(tp->mcam);

    EXPECT_GE(act_res, exp_res.first);
    EXPECT_LE(act_res, exp_res.second);
}

TEST_F(MantisAPITest_N, getMCamGain_N) {
    double act_res = getMCamGain(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamFocus_P) {
    double act_res = getMCamFocus(tp->mcam);

    EXPECT_GE(act_res, -10);
}

TEST_F(MantisAPITest_N, getMCamFocus_N) {
    double act_res = getMCamFocus(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamFocusState_P) {
    int act_res = getMCamFocusState(tp->mcam);

    EXPECT_GE(act_res, -10);
}

TEST_F(MantisAPITest_N, getMCamFocusState_N) {
    int act_res = getMCamFocusState(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamShutter_P) {
	PAIR_DOUBLE exp_res = getMCamShutterRange(tp->mcam);
	double act_res = getMCamShutter(tp->mcam);

    EXPECT_GE(act_res, exp_res.first);
    EXPECT_LE(act_res, exp_res.second);
}

TEST_F(MantisAPITest_N, getMCamShutter_N) {
    double act_res = getMCamShutter(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamSaturation_P) {
	PAIR_DOUBLE exp_res = getMCamSaturationRange(tp->mcam);
	double act_res = getMCamSaturation(tp->mcam);

    EXPECT_GE(act_res, exp_res.first);
    EXPECT_LE(act_res, exp_res.second);
}

TEST_F(MantisAPITest_N, getMCamSaturation_N) {
    double act_res = getMCamSaturation(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamFramerate_P) {
	PAIR_DOUBLE exp_res = getMCamFramerateRange(tp->mcam);
	double act_res = getMCamFramerate(tp->mcam);

    EXPECT_GE(act_res, exp_res.first);
    EXPECT_LE(act_res, exp_res.second);
}

TEST_F(MantisAPITest_N, getMCamFramerate_N) {
    double act_res = getMCamFramerate(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamContrast_P) {
    double act_res = getMCamContrast(tp->mcam);

    EXPECT_GE(act_res, -10);
}

TEST_F(MantisAPITest_N, getMCamContrast_N) {
    double act_res = getMCamContrast(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamDeNoise_P) {
    double act_res = getMCamDeNoise(tp->mcam);

    EXPECT_GE(act_res, -10);
}

TEST_F(MantisAPITest_N, getMCamDeNoise_N) {
    double act_res = getMCamDeNoise(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamSharpening_P) {
	PAIR_DOUBLE exp_res = getMCamSharpeningRange(tp->mcam);
	double act_res = getMCamSharpening(tp->mcam);

    EXPECT_GE(act_res, exp_res.first);
    EXPECT_LE(act_res, exp_res.second);
}

TEST_F(MantisAPITest_N, getMCamSharpening_N) {
    double act_res = getMCamSharpening(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamJpegQuality_P) {
	PAIR_DOUBLE exp_res = getMCamJpegQualityRange(tp->mcam);
	double act_res = getMCamJpegQuality(tp->mcam);

    EXPECT_GE(act_res, exp_res.first);
    EXPECT_LE(act_res, exp_res.second);
}

TEST_F(MantisAPITest_N, getMCamJpegQuality_N) {
    double act_res = getMCamJpegQuality(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamIrFilter_P) {
    bool act_res = getMCamIrFilter(tp->mcam);

    SUCCEED();
}

TEST_F(MantisAPITest_N, getMCamIrFilter_N) {
    bool act_res = getMCamIrFilter(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamWhiteBalanceMode_P) {
    int act_res = getMCamWhiteBalanceMode(tp->mcam);

    EXPECT_GE(act_res, -10);
}

TEST_F(MantisAPITest_N, getMCamWhiteBalanceMode_N) {
    int act_res = getMCamWhiteBalanceMode(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamModuleID_P) {
    uint64_t act_res = getMCamModuleID(tp->mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_N, getMCamModuleID_N) {
    uint64_t act_res = getMCamModuleID(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamCompressionParameters_P) {
    AtlCompressionParameters act_res = getMCamCompressionParameters(tp->mcam);

    EXPECT_GE(act_res.quality_preset_level, 0);
}

TEST_F(MantisAPITest_N, getMCamCompressionParameters_N) {
    AtlCompressionParameters act_res = getMCamCompressionParameters(mcam);

    EXPECT_EQ(act_res.quality_preset_level, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamSensorID_P) {
    uint64_t act_res = getMCamSensorID(tp->mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_N, getMCamSensorID_N) {
    uint64_t act_res = getMCamSensorID(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamPixelSize_P) {
    double act_res = getMCamPixelSize(tp->mcam);

    EXPECT_GE(act_res, -10);
}

TEST_F(MantisAPITest_N, getMCamPixelSize_N) {
    double act_res = getMCamPixelSize(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamFocalLength_P) {
    double act_res = getMCamFocalLength(tp->mcam);

    EXPECT_GE(act_res, 0);
}

TEST_F(MantisAPITest_N, getMCamFocalLength_N) {
    double act_res = getMCamFocalLength(mcam);

    EXPECT_EQ(act_res, 0);
}

TEST_F(MantisAPITest_mcamconn, getMCamWhiteBalance_P) {
    AtlWhiteBalance act_res = getMCamWhiteBalance(tp->mcam);

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
    PAIR_DOUBLE act_res = getMCamGainRange(tp->mcam);

    EXPECT_GT(act_res.second, act_res.first);

    double act_res2 = getMCamGain(tp->mcam);

    EXPECT_GE(act_res2, act_res.first);
    EXPECT_LT(act_res2, act_res.second);
}

TEST_F(MantisAPITest_N, getMCamGainRange_N) {
    PAIR_DOUBLE act_res = getMCamGainRange(mcam);

    EXPECT_GT(act_res.second, act_res.first);
}

TEST_F(MantisAPITest_mcamconn, getMCamExposureRange_P) {
    PAIR_DOUBLE act_res = getMCamExposureRange(tp->mcam);

    EXPECT_GT(act_res.second, act_res.first);

    double act_res2 = getMCamExposure(tp->mcam);

    EXPECT_GE(act_res2, act_res.first);
    EXPECT_LT(act_res2, act_res.second);
}

TEST_F(MantisAPITest_N, getMCamExposureRange_N) {
    PAIR_DOUBLE act_res = getMCamExposureRange(mcam);

    EXPECT_GT(act_res.second, act_res.first);
}

TEST_F(MantisAPITest_mcamconn, getMCamShutterRange_P) {
    PAIR_DOUBLE act_res = getMCamShutterRange(tp->mcam);

    EXPECT_GT(act_res.second, act_res.first);

    double act_res2 = getMCamShutter(tp->mcam);

    EXPECT_GE(act_res2, act_res.first);
    EXPECT_LT(act_res2, act_res.second);
}

TEST_F(MantisAPITest_N, getMCamShutterRange_N) {
    PAIR_DOUBLE act_res = getMCamShutterRange(mcam);

    EXPECT_GT(act_res.second, act_res.first);
}

TEST_F(MantisAPITest_mcamconn, getMCamSaturationRange_P) {
    PAIR_DOUBLE act_res = getMCamSaturationRange(tp->mcam);

    EXPECT_GT(act_res.second, act_res.first);

    double act_res2 = getMCamSaturation(tp->mcam);

    EXPECT_GE(act_res2, act_res.first);
    EXPECT_LT(act_res2, act_res.second);
}

TEST_F(MantisAPITest_N, getMCamSaturationRange_N) {
    PAIR_DOUBLE act_res = getMCamSaturationRange(mcam);

    EXPECT_GT(act_res.second, act_res.first);
}

TEST_F(MantisAPITest_mcamconn, getMCamFramerateRange_P) {
    PAIR_DOUBLE act_res = getMCamFramerateRange(tp->mcam);

    EXPECT_GT(act_res.second, act_res.first);

    double act_res2 = getMCamFramerate(tp->mcam);

    EXPECT_GE(act_res2, act_res.first);
    EXPECT_LT(act_res2, act_res.second);
}

TEST_F(MantisAPITest_N, getMCamFramerateRange_N) {
    PAIR_DOUBLE act_res = getMCamFramerateRange(mcam);

    EXPECT_GT(act_res.second, act_res.first);
}

TEST_F(MantisAPITest_mcamconn, getMCamContrastRange_P) {
    PAIR_DOUBLE act_res = getMCamContrastRange(tp->mcam);

    EXPECT_GT(act_res.second, act_res.first);

    double act_res2 = getMCamContrast(tp->mcam);

    EXPECT_GE(act_res2, act_res.first);
    EXPECT_LT(act_res2, act_res.second);
}

TEST_F(MantisAPITest_N, getMCamContrastRange_N) {
    PAIR_DOUBLE act_res = getMCamContrastRange(mcam);

    EXPECT_GT(act_res.second, act_res.first);
}

TEST_F(MantisAPITest_mcamconn, getMCamDeNoiseRange_P) {
    PAIR_DOUBLE act_res = getMCamDeNoiseRange(tp->mcam);

    EXPECT_GT(act_res.second, act_res.first);

    double act_res2 = getMCamDeNoise(tp->mcam);

    EXPECT_GE(act_res2, act_res.first);
    EXPECT_LT(act_res2, act_res.second);
}

TEST_F(MantisAPITest_N, getMCamDeNoiseRange_N) {
    PAIR_DOUBLE act_res = getMCamDeNoiseRange(mcam);

    EXPECT_GT(act_res.second, act_res.first);
}

TEST_F(MantisAPITest_mcamconn, getMCamSharpeningRange_P) {
    PAIR_DOUBLE act_res = getMCamSharpeningRange(tp->mcam);

    EXPECT_GT(act_res.second, act_res.first);

    double act_res2 = getMCamSharpening(tp->mcam);

    EXPECT_GE(act_res2, act_res.first);
    EXPECT_LT(act_res2, act_res.second);
}

TEST_F(MantisAPITest_N, getMCamSharpeningRange_N) {
    PAIR_DOUBLE act_res = getMCamSharpeningRange(mcam);

    EXPECT_GT(act_res.second, act_res.first);
}

TEST_F(MantisAPITest_mcamconn, getMCamJpegQualityRange_P) {
    PAIR_DOUBLE act_res = getMCamJpegQualityRange(tp->mcam);

    EXPECT_GT(act_res.second, act_res.first);

    double act_res2 = getMCamJpegQuality(tp->mcam);

    EXPECT_GE(act_res2, act_res.first);
    EXPECT_LT(act_res2, act_res.second);
}

TEST_F(MantisAPITest_N, getMCamJpegQualityRange_N) {
    PAIR_DOUBLE act_res = getMCamJpegQualityRange(mcam);

    EXPECT_GT(act_res.second, act_res.first);
}

TEST_F(MantisAPITest_mcamconn, getMCamWhiteBalanceRange_P) {
    PAIR_DOUBLE act_res = getMCamWhiteBalanceRange(tp->mcam);

    EXPECT_GT(act_res.second, act_res.first);

    double act_res2 = getMCamWhiteBalance(tp->mcam).red;

    EXPECT_GE(act_res2, act_res.first);
    EXPECT_LT(act_res2, act_res.second);
}

TEST_F(MantisAPITest_N, getMCamWhiteBalanceRange_N) {
    PAIR_DOUBLE act_res = getMCamWhiteBalanceRange(mcam);

    EXPECT_GE(act_res.first, 0);
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
