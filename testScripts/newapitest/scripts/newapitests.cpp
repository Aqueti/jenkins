#include "newapitest.h"

void HandleImageCallback(aqt::render::RenderFrame &frame, void *userData)
{
  int *_userData = static_cast<int*>(userData);
  if (_userData != NULL) *_userData = 1;

  switch (frame.Type()) {
  case aqt_H264_I_FRAME:
    std::cout << "Received H264 I Frame" << std::endl;
    break;
  case aqt_H264_P_FRAME:
    std::cout << "Received H264 P Frame" << std::endl;
    break;
  default:
    std::cerr << "Unexpected image type." << std::endl;
    return;
  }

  frame.ReleaseData();
}

double getRnd(double min, double max) {
  double value = (max - min) * ( (double)rand() / (double)RAND_MAX ) + min;
  return roundf(value * 100) / 100;
}

AquetiAPI api;
externalAnalysis::ExternalAnalysis eapi(api, "/aqt/SCOP/mantis1/microcamera2");
render::ViewState vs(api, "test");
render::ViewState t_vs(api, "test");

TestParams::TestParams() {
    zeroTime = {};
    vector<float> data = { };

    rect.Time(zeroTime);
    rect.Name("test");
    rect.XNorm(0.5);
    rect.YNorm(0.5);
    rect.WidthNorm(0.5);
    rect.HeightNorm(0.5);

    tag.Time(zeroTime);
    tag.Name("test");
    tag.XNorm(0.5);
    tag.YNorm(0.5);
    tag.Value("My tag");

    fa.Time(zeroTime);
    fa.Name("test");
    fa.Value(data);

    ua.Time(zeroTime);
    ua.Name("test");
    ua.Value();

    cm.Time(zeroTime);
    cm.Name("test");
    cm.Value("{}");

    thumb.Time(zeroTime);
    thumb.Name("test");
    thumb.XNorm(0.5);
    thumb.YNorm(0.5);
    thumb.WidthNorm(0.5);
    thumb.HeightNorm(0.5);
    thumb.ImageType(aqt_JPEG_IMAGE);
    thumb.ImageData("");

    itypes.push_back(aqt_EMPTY_IMAGE);
    itypes.push_back(aqt_H264_I_FRAME);
    itypes.push_back(aqt_H264_P_FRAME);

    num_of["cams"] = 2;
    num_of["renderers"] = 2;
    num_of["storages"] = 2;

    ec.Latitude(1);
    ec.Longitude(2);
    ec.Altitude(3);
    ec.Roll(4);
    ec.Pitch(5);
    ec.Yaw(6);

    ic.WidthDegrees(90);
    ic.HeightDegrees(50);
    ic.PixelSizeDegrees(0.1);
    
    vs.PanDegrees(0);
    vs.MinPanDegrees(-90);
    vs.MaxPanDegrees(90);
    vs.PanSpeedDegrees(6.90455e-310);
    vs.TiltDegrees(0);
    vs.MinTiltDegrees(-50);
    vs.MaxTiltDegrees(50);
    vs.TiltSpeedDegrees(1.85556e-316);
    vs.Zoom(1);
    vs.MinZoom(0.1);
    vs.MaxZoom(50);
    vs.ZoomSpeed(0);
    vs.HorizontalFOVDegrees(90);
    vs.VerticalFOVDegrees(50);

    dtypes.push_back(aqt_DATA_NONE);
    dtypes.push_back(aqt_DATA_IMAGE);
    dtypes.push_back(aqt_DATA_RECTANGLE);
    dtypes.push_back(aqt_DATA_TAG);
    dtypes.push_back(aqt_DATA_THUMBNAIL);
    dtypes.push_back(aqt_DATA_FLOATARRAY);
    dtypes.push_back(aqt_DATA_U8ARRAY);
}

TestParams::~TestParams() {

}

void MantisNewAPITest_stream::SetUp() { 
  vector<SingleCOPCameraDescription> cams = api.GetAvailableCameras();
  cam = cams[0];

  render::TimeState timeControl(api);
  timeControl.PlaySpeed(1);
  render::ViewState vs(api);
  render::ImageSubsetState iss(api);
  render::PoseState ps(api);
  StreamProperties sp;

  stream = new render::RenderStream(api, vs, timeControl, iss, ps, sp);
  stream->AddCamera(cam.Name());

  stream->SetStreamingState(true);
}

void MantisNewAPITest_stream::TearDown() {
  stream->SetStreamingState(false);

  stream->RemoveCamera(cam.Name());
  delete stream;
}

void MantisNewAPITest_viewstate::SetUp() { 

}

void MantisNewAPITest_viewstate::TearDown() { 

}

TEST_F(MantisNewAPITest, eapiGetNextRectangle_P) {
    externalAnalysis::Rectangle t_rect = eapi.GetNextRectangle();

    EXPECT_EQ( aqt_STATUS_OKAY, eapi.GetStatus() );
    EXPECT_EQ( rect.XNorm(), t_rect.XNorm() );
    EXPECT_EQ( rect.YNorm(), t_rect.YNorm() );
    EXPECT_EQ( rect.WidthNorm(), t_rect.WidthNorm() );
    EXPECT_EQ( rect.HeightNorm(), t_rect.HeightNorm() );  
}

TEST_F(MantisNewAPITest, _eapiGetNextRectangle_P) {
    externalAnalysis::Rectangle t_rect = eapi.GetNextRectangle();

    EXPECT_EQ( aqt_STATUS_OKAY, eapi.GetStatus() );
    rect.XNorm(t_rect.XNorm() + 1);
    rect.YNorm(t_rect.YNorm() + 1);
    rect.WidthNorm(t_rect.WidthNorm() + 1);
    rect.HeightNorm(t_rect.HeightNorm() + 1);
    EXPECT_EQ( rect.XNorm(), t_rect.XNorm() + 1);
    EXPECT_EQ( rect.YNorm(), t_rect.YNorm() + 1 );
    EXPECT_EQ( rect.WidthNorm(), t_rect.WidthNorm() + 1 );
    EXPECT_EQ( rect.HeightNorm(), t_rect.HeightNorm() + 1 );  
}

TEST_F(MantisNewAPITest_N, eapiGetNextRectangle_N) {
    externalAnalysis::Rectangle t_rect = eapi.GetNextRectangle();

    EXPECT_NE( aqt_STATUS_OKAY, eapi.GetStatus() );
    EXPECT_EQ( rect.XNorm(), t_rect.XNorm() );
    EXPECT_EQ( rect.YNorm(), t_rect.YNorm() );
    EXPECT_EQ( rect.WidthNorm(), t_rect.WidthNorm() );
    EXPECT_EQ( rect.HeightNorm(), t_rect.HeightNorm() );  
}

TEST_F(MantisNewAPITest, eapiGetNextTag_P) {
    externalAnalysis::Tag t_tag = eapi.GetNextTag();

    EXPECT_EQ( aqt_STATUS_OKAY, eapi.GetStatus() );
    EXPECT_EQ( tag.XNorm(), t_tag.XNorm() );
    EXPECT_EQ( tag.YNorm(), t_tag.YNorm() );
    EXPECT_EQ( tag.Value(), t_tag.Value() );
}

TEST_F(MantisNewAPITest, _eapiGetNextTag_P) {
    externalAnalysis::Tag t_tag = eapi.GetNextTag();

    EXPECT_EQ( aqt_STATUS_OKAY, eapi.GetStatus() );
    tag.XNorm(t_tag.XNorm() + 1);
    tag.YNorm(t_tag.YNorm() + 1);
    tag.Value(t_tag.Value() + "_test");
    EXPECT_EQ( tag.XNorm(), t_tag.XNorm() + 1 );
    EXPECT_EQ( tag.YNorm(), t_tag.YNorm() + 1 );
    EXPECT_STRCASEEQ( tag.Value().c_str(), (t_tag.Value() + "_test").c_str() );
}

TEST_F(MantisNewAPITest_N, eapiGetNextTag_N) {
    externalAnalysis::Tag t_tag = eapi.GetNextTag();

    EXPECT_NE( aqt_STATUS_OKAY, eapi.GetStatus() );
    EXPECT_EQ( tag.XNorm(), t_tag.XNorm() );
    EXPECT_EQ( tag.YNorm(), t_tag.YNorm() );
    EXPECT_STRCASEEQ( tag.Value().c_str(), t_tag.Value().c_str() );
}

TEST_F(MantisNewAPITest, eapiGetNextFloatArray_P) {
    externalAnalysis::FloatArray t_fa = eapi.GetNextFloatArray();

    EXPECT_EQ( aqt_STATUS_OKAY, eapi.GetStatus() );
    EXPECT_EQ( fa.Value().size(), t_fa.Value().size() );
}

TEST_F(MantisNewAPITest_N, eapiGetNextFloatArray_N) {
    externalAnalysis::FloatArray t_fa = eapi.GetNextFloatArray();

    EXPECT_NE( aqt_STATUS_OKAY, eapi.GetStatus() );
    EXPECT_EQ( fa.Value().size(), t_fa.Value().size() );
}

TEST_F(MantisNewAPITest, eapiGetNextU8Array_P) {
    externalAnalysis::U8Array t_ua = eapi.GetNextU8Array();

    EXPECT_EQ( aqt_STATUS_OKAY, !eapi.GetStatus() ); 
    EXPECT_EQ( ua.Value(), t_ua.Value() );
}

TEST_F(MantisNewAPITest_N, eapiGetNextU8Array_N) {
    externalAnalysis::U8Array t_ua = eapi.GetNextU8Array();

    EXPECT_NE( aqt_STATUS_OKAY, eapi.GetStatus() ); 
    EXPECT_EQ( ua.Value(), t_ua.Value() );
}

TEST_F(MantisNewAPITest, eapiGetNextCameraModel_P) {
    externalAnalysis::CameraModel t_cm = eapi.GetNextCameraModel();

    EXPECT_EQ( aqt_STATUS_OKAY, eapi.GetStatus() ); 
    EXPECT_EQ( cm.Value(), t_cm.Value() );
}

TEST_F(MantisNewAPITest_N, eapiGetNextCameraModel_N) {
    externalAnalysis::CameraModel t_cm = eapi.GetNextCameraModel();

    EXPECT_NE( aqt_STATUS_OKAY, eapi.GetStatus() ); 
    EXPECT_EQ( cm.Value(), t_cm.Value() );
}

TEST_F(MantisNewAPITest, eapiGetNextThumbnail_P) {
    externalAnalysis::Thumbnail t_thumb = eapi.GetNextThumbnail();

    EXPECT_EQ( aqt_STATUS_OKAY, eapi.GetStatus() );                    
    EXPECT_EQ( thumb.XNorm(), t_thumb.XNorm() );
    EXPECT_EQ( thumb.YNorm(), t_thumb.YNorm() );
    EXPECT_EQ( thumb.WidthNorm(), t_thumb.WidthNorm() );
    EXPECT_EQ( thumb.HeightNorm(), t_thumb.HeightNorm() );
}

TEST_F(MantisNewAPITest_N, eapiGetNextThumbnail_N) {
    externalAnalysis::Thumbnail t_thumb = eapi.GetNextThumbnail();

    EXPECT_NE( aqt_STATUS_OKAY, eapi.GetStatus() );                    
    EXPECT_EQ( thumb.XNorm(), t_thumb.XNorm() );
    EXPECT_EQ( thumb.YNorm(), t_thumb.YNorm() );
    EXPECT_EQ( thumb.WidthNorm(), t_thumb.WidthNorm() );
    EXPECT_EQ( thumb.HeightNorm(), t_thumb.HeightNorm() );
}

TEST_F(MantisNewAPITest, eapiInsertRectangle_P) {
    ::externalAnalysis::Rectangle r;

    eapi.InsertRectangle(r);

    EXPECT_EQ( aqt_STATUS_OKAY, eapi.GetStatus() );
}

TEST_F(MantisNewAPITest_N, eapiInsertRectangle_N) {
    ::externalAnalysis::Rectangle r;

    eapi.InsertRectangle(r);

    EXPECT_EQ( aqt_STATUS_OKAY, eapi.GetStatus() );
}

TEST_F(MantisNewAPITest, eapiInsertTag_P) {
    ::externalAnalysis::Tag t;

    eapi.InsertTag(t);

    EXPECT_EQ( aqt_STATUS_OKAY, eapi.GetStatus() );
}

TEST_F(MantisNewAPITest, eapiInsertFloatArray_P) {
    ::externalAnalysis::FloatArray fa;

    eapi.InsertFloatArray(fa);

    EXPECT_EQ( aqt_STATUS_OKAY, eapi.GetStatus() );
}

TEST_F(MantisNewAPITest_N, eapiInsertFloatArray_N) {
    EXPECT_NE( aqt_STATUS_OKAY, eapi.InsertFloatArray(fa) );
}

TEST_F(MantisNewAPITest, eapiInsertU8Array_P) {
    ::externalAnalysis::U8Array ua;

    eapi.InsertU8Array(ua);

    EXPECT_EQ( aqt_STATUS_OKAY, eapi.GetStatus() );
}

TEST_F(MantisNewAPITest, eapiInsertCameraModel_P) {
    eapi.InsertCameraModel(cm);

    EXPECT_EQ( aqt_STATUS_OKAY, eapi.GetStatus() );
}

TEST_F(MantisNewAPITest_N, eapiInsertCameraModel_N) {
    EXPECT_NE( aqt_STATUS_OKAY, eapi.InsertCameraModel(cm) );
}

TEST_F(MantisNewAPITest, eapiInsertThumbnail_P) {
    eapi.InsertThumbnail(thumb);

    EXPECT_EQ( aqt_STATUS_OKAY, eapi.GetStatus() );
}

TEST_F(MantisNewAPITest_N, eapiInsertThumbnail_N) {
    EXPECT_NE( aqt_STATUS_OKAY, eapi.InsertThumbnail(thumb) );
}

TEST_F(MantisNewAPITest, eapiSetStartTime_P) {
    eapi.SetStartTime(zeroTime);

    EXPECT_EQ( aqt_STATUS_OKAY, eapi.GetStatus() );
}

TEST_F(MantisNewAPITest_N, eapiSetStartTime_N) {
    EXPECT_NE( aqt_STATUS_OKAY, eapi.SetStartTime(zeroTime) );
}

TEST_F(MantisNewAPITest, eapiSetImageTypes_P) {
    eapi.SetImageTypes(itypes);

    EXPECT_EQ( aqt_STATUS_OKAY, eapi.GetStatus() );
}

TEST_F(MantisNewAPITest_N, eapiSetImageTypes_N) {
    EXPECT_NE( aqt_STATUS_OKAY, eapi.SetImageTypes(itypes) );
}

TEST_F(MantisNewAPITest, eapiSetMinSize_P) {
    eapi.SetMinSize(0, 0);

    EXPECT_EQ( aqt_STATUS_OKAY, eapi.GetStatus() );
}

TEST_F(MantisNewAPITest_N, eapiSetMinSize_N) {
    EXPECT_NE( aqt_STATUS_OKAY, eapi.SetMinSize(0, 0) );
}

TEST_F(MantisNewAPITest, eapiSetMaxSize_P) {
    eapi.SetMaxSize(10000, 10000);

    EXPECT_EQ( aqt_STATUS_OKAY, eapi.GetStatus() );
}

TEST_F(MantisNewAPITest_N, eapiSetMaxSize_N) {
    EXPECT_NE( aqt_STATUS_OKAY, eapi.SetMaxSize(10000, 10000) );
}

TEST_F(MantisNewAPITest, GetNextImage_P) {
    eapi.SetImageTypes(itypes);
    eapi.SetMinSize(0, 0);
    eapi.SetMaxSize(10000, 10000);

    Image t_img = eapi.GetNextImage();
    aqt_Image aqt_t_img = t_img.RawImage();

    EXPECT_TRUE( aqt_STATUS_OKAY == eapi.GetStatus() );
    EXPECT_EQ( t_img.Time().tv_sec, t_img.Time().tv_sec );
    EXPECT_EQ( t_img.Width(), t_img.Width() );
    EXPECT_EQ( t_img.Height(), t_img.Height() );
    EXPECT_EQ( (int)t_img.Type(), (int)t_img.Type() );
    EXPECT_STRCASEEQ( t_img.Data(), t_img.Data() );
    EXPECT_EQ( t_img.Size(), t_img.Size() );

    t_img.ReleaseData();
}

TEST_F(MantisNewAPITest_N, GetNextImage_N) {
    Image t_img = eapi.GetNextImage();
    
    EXPECT_NE( aqt_STATUS_OKAY, eapi.GetStatus() );
    EXPECT_EQ( t_img.Width(), t_img.Width() );
    EXPECT_EQ( t_img.Height(), t_img.Height() );

    t_img.ReleaseData();
}

TEST_F(MantisNewAPITest, SetNameFilter_P) {
    eapi.SetNameFilter("");

    EXPECT_TRUE( aqt_STATUS_OKAY == eapi.GetStatus() );
}

TEST_F(MantisNewAPITest, GetAvailableCameras_P) {
    vector<aqt::SingleCOPCameraDescription> cams = api.GetAvailableCameras();

    EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );
    EXPECT_EQ( cams.size(), num_of["cams"] );
}

TEST_F(MantisNewAPITest_N, GetAvailableCameras_NL) {
    vector<aqt::SingleCOPCameraDescription> cams = api.GetAvailableCameras();

    EXPECT_NE( aqt_STATUS_OKAY, api.GetStatus() );
    EXPECT_EQ( cams.size(), num_of["cams"] );
}

TEST_F(MantisNewAPITest, AvailableCameras_Name_P) {
    vector<aqt::SingleCOPCameraDescription> cams = api.GetAvailableCameras();

    for (int i = 0; i < cams.size(); i++) {
        EXPECT_STRCASEEQ(cams[i].Name().c_str(), ("aqt:Camera:" + to_string(i + 1)).c_str()); 
        EXPECT_STRCASEEQ(cams[i].Name("test_camera").c_str(), "test_camera");    
    }
}

TEST_F(MantisNewAPITest, ExtrinsicCalibration_P) {
    vector<aqt::SingleCOPCameraDescription> cams = api.GetAvailableCameras();

    for (size_t i = 0; i < cams.size(); i++) {        
        ASSERT_TRUE( cams[i].Extrinsic() != aqt::UNDEFINED_EXTRINSIC );
        aqt::ExtrinsicCalibration t_ec = cams[i].Extrinsic();
            
        EXPECT_EQ( ec.Latitude(), t_ec.Latitude() );
        EXPECT_EQ( ec.Longitude(), t_ec.Longitude() );
        EXPECT_EQ( ec.Altitude(), t_ec.Altitude() );
        EXPECT_EQ( ec.Roll(), t_ec.Roll() );
        EXPECT_EQ( ec.Pitch(), t_ec.Pitch() );
        EXPECT_EQ( ec.Yaw(), t_ec.Yaw() );    
    }
}

TEST_F(MantisNewAPITest_N, ExtrinsicCalibration_N) {
    vector<aqt::SingleCOPCameraDescription> cams = api.GetAvailableCameras();

    for (size_t i = 0; i < cams.size(); i++) {        
        ASSERT_TRUE( cams[i].Extrinsic() != aqt::UNDEFINED_EXTRINSIC );
        aqt::ExtrinsicCalibration t_ec = cams[i].Extrinsic();
            
        EXPECT_EQ( ec.Latitude(), t_ec.Latitude() );
        EXPECT_EQ( ec.Longitude(), t_ec.Longitude() );
        EXPECT_EQ( ec.Altitude(), t_ec.Altitude() );
        EXPECT_EQ( ec.Roll(), t_ec.Roll() );
        EXPECT_EQ( ec.Pitch(), t_ec.Pitch() );
        EXPECT_EQ( ec.Yaw(), t_ec.Yaw() );    
    }
}

TEST_F(MantisNewAPITest, IntrinsicCalibration_P) {
    vector<aqt::SingleCOPCameraDescription> cams = api.GetAvailableCameras();

    for (size_t i = 0; i < cams.size(); i++) {
        for (size_t j = 0; j < cams[i].Intrinsics().size(); j++) { 
            ASSERT_TRUE( cams[i].Intrinsics()[j] != aqt::UNDEFINED_INTRINSIC );           
            aqt::IntrinsicCalibration t_ic = cams[i].Intrinsics()[j];
    
            EXPECT_EQ( ic.WidthDegrees(), t_ic.WidthDegrees() );
            EXPECT_EQ( ic.HeightDegrees(), t_ic.HeightDegrees() );
            EXPECT_EQ( ic.PixelSizeDegrees(), t_ic.PixelSizeDegrees() );
        }      
    }
}

TEST_F(MantisNewAPITest, IntrinsicCalibration_N) {
    vector<aqt::SingleCOPCameraDescription> cams = api.GetAvailableCameras();

    for (size_t i = 0; i < cams.size(); i++) {
        for (size_t j = 0; j < cams[i].Intrinsics().size(); j++) { 
            ASSERT_TRUE( cams[i].Intrinsics()[j] != aqt::UNDEFINED_INTRINSIC );           
            aqt::IntrinsicCalibration t_ic = cams[i].Intrinsics()[j];
    
            EXPECT_EQ( ic.WidthDegrees(), t_ic.WidthDegrees() );
            EXPECT_EQ( ic.HeightDegrees(), t_ic.HeightDegrees() );
            EXPECT_EQ( ic.PixelSizeDegrees(), t_ic.PixelSizeDegrees() );
        }      
    }
}

TEST_F(MantisNewAPITest, GetAvailableRenderers_P) {
    vector<RendererDescription> renderers = api.GetAvailableRenderers();

    EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );
    EXPECT_EQ( renderers.size(), num_of["renderers"] );
}

TEST_F(MantisNewAPITest, GetAvailableRenderers_N) {
    vector<RendererDescription> renderers = api.GetAvailableRenderers();

    EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );
    EXPECT_EQ( renderers.size(), num_of["renderers"] );
}

TEST_F(MantisNewAPITest, AvailableRenderers_Name_P) {
    vector<RendererDescription> renderers = api.GetAvailableRenderers();
    
    for (int i = 0; i < renderers.size(); i++) {
        EXPECT_STRCASEEQ(renderers[i].Name().c_str(), ("aqt:Renderer:" + to_string(i + 1)).c_str()); 
        EXPECT_STRCASEEQ(renderers[i].Name("test_renderer").c_str(), "test_renderer");    
    }
}

TEST_F(MantisNewAPITest, GetAvailableStorage_P) {
    vector<StorageDescription> storages = api.GetAvailableStorage();

    EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );
    EXPECT_EQ( storages.size(), num_of["storages"] );
}

TEST_F(MantisNewAPITest, GetAvailableStorage_N) {
    vector<StorageDescription> storages = api.GetAvailableStorage();

    EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );
    EXPECT_EQ( storages.size(), num_of["storages"] );
}

TEST_F(MantisNewAPITest, AvailableStorages_Name_P) {
    vector<StorageDescription> storages = api.GetAvailableStorage();
    
    for (int i = 0; i < storages.size(); i++) {
        EXPECT_STRCASEEQ(storages[i].Name().c_str(), ("aqt:Storage:" + to_string(i + 1)).c_str()); 
        EXPECT_STRCASEEQ(storages[i].Name("test_storage").c_str(), "test_storage");    
    }
}

TEST_F(MantisNewAPITest, GetCurrentSystemTime_P) {
    timeval time = api.GetCurrentSystemTime();
    
    EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );
    //EXPECT_EQ( time.tv_sec,  );
    //EXPECT_EQ( time.tv_usec,  );
}

TEST_F(MantisNewAPITest, GetDetailedStatus_P) {
    string entityName = "";
    string d_status = api.GetDetailedStatus(entityName);
    
    EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );
}

TEST_F(MantisNewAPITest, GetDetailedStatus_N) {
    string entityName = "";
    string d_status = api.GetDetailedStatus(entityName);
    
    EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );;
    EXPECT_STRCASEEQ(d_status.c_str(), "{}");
}

TEST_F(MantisNewAPITest, CreateIssueReport_P) {
    string fileNameToWrite, summary, description;
    aqt_Status status = api.CreateIssueReport(fileNameToWrite, summary, description);    
    
    EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );
}

TEST_F(MantisNewAPITest, CreateIssueReport_N) {
    string fileNameToWrite, summary, description;
    aqt_Status status = api.CreateIssueReport(fileNameToWrite, summary, description);    
    
    EXPECT_EQ( aqt_STATUS_BAD_PARAMETER, api.GetStatus() );
}

TEST_F(MantisNewAPITest, test1_P) {
    render::TimeState ts(api, "test");
    //cout << ts.GetRawState() << endl;
    cout << ts.GetStatus() << endl;
    cout << ts.Time().tv_sec << endl;
    cout << ts.PlaySpeed() << endl;
    
    EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );
}



TEST_F(MantisNewAPITest_viewstate, viewstatePanDegrees_P) {
    double value = getRnd(0, 25);
    EXPECT_DOUBLE_EQ( vs.PanDegrees(), t_vs.PanDegrees() );
    
    vs.PanDegrees(value);
    EXPECT_DOUBLE_EQ( vs.PanDegrees(), value );
}

TEST_F(MantisNewAPITest_viewstate, viewstateMinPanDegrees_P) {
    double value = getRnd(0, 25);
    EXPECT_DOUBLE_EQ( vs.MinPanDegrees(), t_vs.MinPanDegrees() );
    
    vs.MinPanDegrees(value);
    EXPECT_DOUBLE_EQ( vs.MinPanDegrees(), value );
}

TEST_F(MantisNewAPITest_viewstate, viewstateMaxPanDegrees_P) {
    double value = getRnd(0, 25);
    EXPECT_DOUBLE_EQ( vs.MaxPanDegrees(), t_vs.MaxPanDegrees() );
    
    vs.MaxPanDegrees(value);
    EXPECT_DOUBLE_EQ( vs.MaxPanDegrees(), value );
}

TEST_F(MantisNewAPITest_viewstate, viewstatePanSpeedDegrees_P) {
    double value = getRnd(0, 25);
    EXPECT_DOUBLE_EQ( vs.PanSpeedDegrees(), t_vs.PanSpeedDegrees() );
    
    vs.PanSpeedDegrees(value);
    EXPECT_DOUBLE_EQ( vs.PanSpeedDegrees(), value );
}

TEST_F(MantisNewAPITest_viewstate, viewstateTiltDegrees_P) {
    double value = getRnd(0, 25);
    EXPECT_DOUBLE_EQ( vs.TiltDegrees(), t_vs.TiltDegrees() );
    
    vs.TiltDegrees(value);
    EXPECT_DOUBLE_EQ( vs.TiltDegrees(), value );
}

TEST_F(MantisNewAPITest_viewstate, viewstateMinTiltDegrees_P) {
    double value = getRnd(0, 25);
    EXPECT_DOUBLE_EQ( vs.MinTiltDegrees(), t_vs.MinTiltDegrees() );
    
    vs.MinTiltDegrees(value);
    EXPECT_DOUBLE_EQ( vs.MinTiltDegrees(), value );
}

TEST_F(MantisNewAPITest_viewstate, viewstateMaxTiltDegrees_P) {
    double value = getRnd(0, 25);
    EXPECT_DOUBLE_EQ( vs.MaxTiltDegrees(), t_vs.MaxTiltDegrees() );
    
    vs.MaxTiltDegrees(value);
    EXPECT_DOUBLE_EQ( vs.MaxTiltDegrees(), value );
}

TEST_F(MantisNewAPITest_viewstate, viewstateTiltSpeedDegrees_P) {
    double value = getRnd(0, 25);
    EXPECT_DOUBLE_EQ( vs.TiltSpeedDegrees(), t_vs.TiltSpeedDegrees() );
    
    vs.TiltSpeedDegrees(value);
    EXPECT_DOUBLE_EQ( vs.TiltSpeedDegrees(), value );
}

TEST_F(MantisNewAPITest_viewstate, viewstateZoom_P) {
    double value = getRnd(0, 25);
    EXPECT_DOUBLE_EQ( vs.Zoom(), t_vs.Zoom() );
    
    vs.Zoom(value);
    EXPECT_DOUBLE_EQ( vs.Zoom(), value );
}

TEST_F(MantisNewAPITest_viewstate, viewstateMinZoom_P) {
    double value = getRnd(0, 25);
    EXPECT_DOUBLE_EQ( vs.MinZoom(), t_vs.MinZoom() );
    
    vs.MinZoom(value);
    EXPECT_DOUBLE_EQ( vs.MinZoom(), value );
}

TEST_F(MantisNewAPITest_viewstate, viewstateMaxZoom_P) {    
    double value = getRnd(0, 25);
    EXPECT_DOUBLE_EQ( vs.MaxZoom(), t_vs.MaxZoom() );
    
    vs.MaxZoom(value);
    EXPECT_DOUBLE_EQ( vs.MaxZoom(), value );
}

TEST_F(MantisNewAPITest_viewstate, viewstateZoomSpeed_P) {
    double value = getRnd(0, 25);
    EXPECT_DOUBLE_EQ( vs.ZoomSpeed(), t_vs.ZoomSpeed() );
    
    vs.ZoomSpeed(value);
    EXPECT_DOUBLE_EQ( vs.ZoomSpeed(), value );
}

TEST_F(MantisNewAPITest_viewstate, viewstateHorizontalFOVDegrees_P) {
    double value = getRnd(0, 25);
    EXPECT_DOUBLE_EQ( vs.HorizontalFOVDegrees(), t_vs.HorizontalFOVDegrees() );
    
    vs.HorizontalFOVDegrees(value);
    EXPECT_DOUBLE_EQ( vs.HorizontalFOVDegrees(), value );
}

TEST_F(MantisNewAPITest_viewstate, viewstateVerticalFOVDegrees_P) {
    double value = getRnd(0, 25);
    EXPECT_DOUBLE_EQ( vs.VerticalFOVDegrees(), t_vs.VerticalFOVDegrees() );
    
    vs.VerticalFOVDegrees(value);
    EXPECT_DOUBLE_EQ( vs.VerticalFOVDegrees(), value );
}



TEST_F(MantisNewAPITest, posestateLatitude_P) {
  ::render::PoseState ps(api, "test", false);
  ::render::PoseState t_ps(api, "test", false);

  double value = getRnd(0, 25);
  EXPECT_DOUBLE_EQ( ps.Latitude(), t_ps.Latitude() );
  EXPECT_DOUBLE_EQ( ps.Longitude(), t_ps.Longitude() );
  EXPECT_DOUBLE_EQ( ps.Altitude(), t_ps.Altitude() );
  EXPECT_DOUBLE_EQ( ps.Roll(), t_ps.Roll() );
  EXPECT_DOUBLE_EQ( ps.Pitch(), t_ps.Pitch() );
  EXPECT_DOUBLE_EQ( ps.Yaw(), t_ps.Yaw() );

  
  ps.Latitude(value);
  EXPECT_DOUBLE_EQ( ps.Latitude(), value );
}

TEST_F(MantisNewAPITest, imagesubsetstateMinX_P) {
  ::render::ImageSubsetState iss(api, "test", false);
  ::render::ImageSubsetState t_iss(api, "test", false);

  double value = getRnd(0, 25);
  EXPECT_DOUBLE_EQ( iss.MinX(), t_iss.MinX() );
  EXPECT_DOUBLE_EQ( iss.MaxX(), t_iss.MaxX() );
  EXPECT_DOUBLE_EQ( iss.MinY(), t_iss.MinY() );
  EXPECT_DOUBLE_EQ( iss.MaxY(), t_iss.MaxY() );
  
  iss.MinX(value);
  EXPECT_DOUBLE_EQ( iss.MinX(), value );
}


TEST_F(MantisNewAPITest_stream, SetStreamCallback_P) {
  int act_res = 0;

  stream->SetStreamCallback(HandleImageCallback, &act_res);
  EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );
  sleep(1);
  stream->SetStreamCallback(nullptr, nullptr);
  EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );

  EXPECT_EQ(act_res, 1);
}

TEST_F(MantisNewAPITest_stream, reSetStreamCallback_P) {
  int act_res = 0;

  stream->SetStreamCallback(HandleImageCallback, NULL);
  EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );
  sleep(1);
  stream->SetStreamCallback(HandleImageCallback, &act_res);
  EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );
  sleep(1);
  stream->SetStreamCallback(nullptr, nullptr);
  EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );

  EXPECT_EQ(act_res, 1);
}

TEST_F(MantisNewAPITest_stream, GetNextFrame_P) {
  size_t count = 10;
  do {
    render::RenderFrame frame = stream->GetNextFrame();
    if (aqt_STATUS_OKAY == stream->GetStatus()) {

      if (frame.Type() == aqt_H264_I_FRAME) {
            cout << "__Received H264 I Frame" << std::endl;
      } else if (frame.Type() == aqt_H264_P_FRAME) {
            cout << "__Received H264 P Frame" << std::endl;
      } else {
            cerr << "__Unexpected image type." << std::endl;          
      }

      frame.ReleaseData();

      count--;
    }

  } while (count > 0);

  EXPECT_EQ(count, 0);
}

TEST_F(MantisNewAPITest_stream, AddCamera_P) {
  vector<SingleCOPCameraDescription> cams = api.GetAvailableCameras();
  
  for (int i = 0; i < 10; i++) {
    if (i % 2 == 0) stream->AddCamera(cams[0].Name());
    else stream->AddCamera("test_cam_" + to_string(i));

    EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );
  }
}

TEST_F(MantisNewAPITest_stream, RemoveCamera_P) {
  stream->AddCamera("test_cam");
  stream->RemoveCamera("test_cam");
  EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );

  stream->RemoveCamera("test_cam");
  EXPECT_NE( aqt_STATUS_OKAY, api.GetStatus() );
}

TEST_F(MantisNewAPITest_stream, SetStreamingState_P) {
  stream->SetStreamingState(false);
  EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );

  for (int i = 0;i < 1e6; i++) {
    render::RenderFrame frame = stream->GetNextFrame();
    if (aqt_STATUS_OKAY == stream->GetStatus()) FAIL();
  }

  stream->SetStreamingState(true);
  EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );

  for (int i = 0;i < 1e6; i++) {
    render::RenderFrame frame = stream->GetNextFrame();
    if (aqt_STATUS_OKAY == stream->GetStatus()) SUCCEED();     
  }
}

TEST_F(MantisNewAPITest_stream, GetFloatParameterRange_P) {
  aqt_RenderFloatShaderParamType which = aqt_RFSP_GAIN;
  float returnMin; float returnMax;
  stream->GetFloatParameterRange(which, returnMin, returnMax);

  EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );
  EXPECT_NEAR( returnMin, 0.1, 1e4);
  EXPECT_NEAR( returnMax, 10, 1e4);
}

TEST_F(MantisNewAPITest_stream, FloatParameter_P) {
  aqt_RenderFloatShaderParamType which = aqt_RFSP_GAIN;
  float res = stream->FloatParameter(which);

  EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );
  EXPECT_EQ( res, 1 );
}

TEST_F(MantisNewAPITest_stream, BoolParameter_P) {
  aqt_RenderBoolShaderParamType which = aqt_RBSP_DENOISE;
  bool res = stream->BoolParameter(which);

  EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );
  EXPECT_EQ( res, 0 );
}
// -------------

TEST_F(MantisNewAPITest_stream, Recording_P) {
  ::camera::Camera r_cam(api, "test_cam");

  EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );
  EXPECT_FALSE( r_cam.Recording() );

  r_cam.Recording(true);

  EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );
  EXPECT_TRUE( r_cam.Recording() );
}

TEST_F(MantisNewAPITest_stream, SetStorageDevice_P) {
  ::camera::Camera r_cam(api, "test_cam");

  r_cam.SetStorageDevice("test_storage");

  EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );
}

TEST_F(MantisNewAPITest_stream, GetCanStreamLiveNow_P) {
  ::camera::Camera r_cam(api, "test_cam");

  cout << r_cam.GetCanStreamLiveNow() << endl;

  EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );
}

TEST_F(MantisNewAPITest_stream, GetStoredDataRanges_P) {
  ::camera::Camera r_cam(api, "test_cam");

  vector<aqt_Interval> ivals = r_cam.GetStoredDataRanges();

  EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );
  EXPECT_EQ( ivals[0].start.tv_sec, 1000 );
  EXPECT_EQ( ivals[0].end.tv_sec, 0 );
}

TEST_F(MantisNewAPITest_stream, DeleteStoredDataRange_P) {
  ::camera::Camera r_cam(api, "test_cam");

  vector<aqt_Interval> ivals = r_cam.GetStoredDataRanges();

  aqt_Interval ival = ivals[0];

  uint16_t f_size = ivals.size();  
  r_cam.DeleteStoredDataRange(ival, dtypes);
  
  EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );

  uint16_t s_size = r_cam.GetStoredDataRanges().size();

  EXPECT_EQ( f_size, s_size + 1 );
}

TEST_F(MantisNewAPITest_stream, SetStreamingMode_P) {
  ::camera::Camera r_cam(api, "test_cam");

  for (int i = 0; i <= 10; i++) {
    r_cam.SetStreamingMode(i);
    
    EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );
  }
}

TEST_F(MantisNewAPITest_stream, SetStreamingMode_JSON_P) {
  ::camera::Camera r_cam(api, "test_cam");

  string JSONConfiguration = "{}";

  r_cam.SetStreamingMode(JSONConfiguration);
  
  EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );
}

// -------------

TEST_F(MantisNewAPITest, DeleteStoredDataRange2_P) {
  ::storage::Storage storage(api, "test_storage");

  string entityName = "";
  aqt_Interval ival;

  storage.DeleteStoredDataRange(entityName, ival, dtypes);
  
  EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );
}

TEST_F(MantisNewAPITest, DeleteStoredDataRange2_N) {
  ::storage::Storage storage(api, "test_storage");

  string entityName = "";
  aqt_Interval ival;

  storage.DeleteStoredDataRange(entityName, ival, dtypes);
  
  EXPECT_EQ( aqt_STATUS_BAD_PARAMETER, api.GetStatus() );
}

TEST_F(MantisNewAPITest, CopyStoredDataRange_P) {
  ::storage::Storage storage(api, "test_storage");

  string entityName = "";
  aqt_Interval ival;

  storage.CopyStoredDataRange(storage, entityName, ival, dtypes);
  
  EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );
}

TEST_F(MantisNewAPITest, CopyStoredDataRange_N) {
  ::storage::Storage storage(api, "test_storage");

  string entityName = "";
  aqt_Interval ival;

  storage.CopyStoredDataRange(storage, entityName, ival, dtypes);
  
  EXPECT_EQ( aqt_STATUS_BAD_PARAMETER, api.GetStatus() );
}

TEST_F(MantisNewAPITest, ExportStoredDataRange_P) {
  ::storage::Storage storage(api, "test_storage");

  string outputURL = "";
  string entityName = "";
  aqt_Interval ival;

  storage.ExportStoredDataRange(outputURL, aqt_EXTERNAL_FORMAT_ZIP, entityName, ival, dtypes);
  
  EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );
}

TEST_F(MantisNewAPITest, ExportStoredDataRange_N) {
  ::storage::Storage storage(api, "test_storage");

  string outputURL = "";
  string entityName = "";
  aqt_Interval ival;

  storage.ExportStoredDataRange(outputURL, aqt_EXTERNAL_FORMAT_ZIP, entityName, ival, dtypes);
  
  EXPECT_EQ( aqt_STATUS_BAD_PARAMETER, api.GetStatus() );
}

TEST_F(MantisNewAPITest, ImportStoredDataRange_P) {
  ::storage::Storage storage(api, "test_storage");

  string inputURL = "";
  string entityName = "";
  aqt_Interval ival;

  storage.ImportStoredDataRange(inputURL, aqt_EXTERNAL_FORMAT_ZIP, entityName, ival, dtypes);
  
  EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );
}

TEST_F(MantisNewAPITest, ImportStoredDataRange_N) {
  ::storage::Storage storage(api, "test_storage");

  string inputURL = "";
  string entityName = "";
  aqt_Interval ival;

  storage.ImportStoredDataRange(inputURL, aqt_EXTERNAL_FORMAT_ZIP, entityName, ival, dtypes);
  
  EXPECT_EQ( aqt_STATUS_BAD_PARAMETER, api.GetStatus() );
}

// ------------

TEST_F(MantisNewAPITest, GetSoftwareVersion_P) {
  ::update::Update update(api, "test_update");

  string version = update.GetSoftwareVersion();

  EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );
  EXPECT_STRCASEEQ(version.c_str(), "00.00.00");
}

TEST_F(MantisNewAPITest, GetSoftwareVersion_N) {
  ::update::Update update(api, "test_update");

  string version = update.GetSoftwareVersion();

  EXPECT_EQ( aqt_STATUS_BAD_PARAMETER, api.GetStatus() );
  EXPECT_STRCASEEQ(version.c_str(), "00.00.00");
}

TEST_F(MantisNewAPITest, Install_P) {
  ::update::Update update(api, "test_update");

  string data = "";
  string checksum = "";
  
  update.Install(data, checksum);

  EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );
}

TEST_F(MantisNewAPITest, Install_N) {
  ::update::Update update(api, "test_update");

  string data = "";
  string checksum = "";
  
  update.Install(data, checksum);

  EXPECT_EQ( aqt_STATUS_BAD_PARAMETER, api.GetStatus() );
}

TEST_F(MantisNewAPITest, InstallFromURL_P) {
  ::update::Update update(api, "test_update");

  string dataURL = "";
  string checksumURL = "";
  
  update.Install(dataURL, checksumURL);

  EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );
}

TEST_F(MantisNewAPITest, InstallFromURL_N) {
  ::update::Update update(api, "test_update");

  string dataURL = "";
  string checksumURL = "";
  
  update.Install(dataURL, checksumURL);

  EXPECT_EQ( aqt_STATUS_BAD_PARAMETER, api.GetStatus() );
}

// ------------

TEST_F(MantisNewAPITest, imgTime_P) {
  Image img = eapi.GetNextImage();

  timeval tv = img.Time();
  cout << "tv " << tv.tv_sec << endl;
  EXPECT_EQ( aqt_STATUS_OKAY, api.GetStatus() );
}



int main(int argc, char **argv) {
  ::testing::InitGoogleTest( &argc, argv );
	
	::testing::GTEST_FLAG(filter) = "*_P";
	RUN_ALL_TESTS();

	return 0;
}