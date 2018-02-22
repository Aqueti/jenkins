#include "newapitest.h"



TestParams::TestParams() {
    zeroTime = {};
    vector<float> data = { };

    rect.Time(zeroTime);
    rect.Name("test");
    rect.XNorm(0.4); //0.5
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

    types.push_back(aqt_EMPTY_IMAGE);
    types.push_back(aqt_H264_I_FRAME);
    types.push_back(aqt_H264_P_FRAME);

    num_of_cams = 2;

    ec.Latitude(1);
    ec.Longitude(2);
    ec.Altitude(3);
    ec.Roll(4);
    ec.Pitch(5);
    ec.Yaw(6);

    ic.WidthDegrees(90);
    ic.HeightDegrees(50);
    ic.PixelSizeDegrees(0.1);
 }

TestParams::~TestParams() {

}

AquetiAPI api;
externalAnalysis::ExternalAnalysis eapi(api, "/aqt/SCOP/mantis1/microcamera2");

TEST_F(MantisNewAPITest, eapiGetNextRectangle_P) {
    externalAnalysis::Rectangle t_rect = eapi.GetNextRectangle();

    EXPECT_TRUE( aqt_STATUS_OKAY == eapi.GetStatus() );
    EXPECT_EQ( rect.XNorm(), t_rect.XNorm() );
    EXPECT_EQ( rect.YNorm(), t_rect.YNorm() );
    EXPECT_EQ( rect.WidthNorm(), t_rect.WidthNorm() );
    EXPECT_EQ( rect.HeightNorm(), t_rect.HeightNorm() );  
}

TEST_F(MantisNewAPITest_N, eapiGetNextRectangle_N) {
    externalAnalysis::Rectangle t_rect = eapi.GetNextRectangle();

    EXPECT_TRUE( aqt_STATUS_OKAY == eapi.GetStatus() );
    EXPECT_EQ( rect.XNorm(), t_rect.XNorm() );
    EXPECT_EQ( rect.YNorm(), t_rect.YNorm() );
    EXPECT_EQ( rect.WidthNorm(), t_rect.WidthNorm() );
    EXPECT_EQ( rect.HeightNorm(), t_rect.HeightNorm() );  
}

TEST_F(MantisNewAPITest, eapiGetNextTag_P) {
    externalAnalysis::Tag t_tag = eapi.GetNextTag();

    EXPECT_TRUE( aqt_STATUS_OKAY == eapi.GetStatus() );
    EXPECT_EQ( tag.XNorm(), t_tag.XNorm() );
    EXPECT_EQ( tag.YNorm(), t_tag.YNorm() );
    EXPECT_EQ( tag.Value(), t_tag.Value() );
}

TEST_F(MantisNewAPITest_N, eapiGetNextTag_N) {
    externalAnalysis::Tag t_tag = eapi.GetNextTag();

    EXPECT_FALSE( aqt_STATUS_OKAY == eapi.GetStatus() );
    EXPECT_EQ( tag.XNorm(), t_tag.XNorm() );
    EXPECT_EQ( tag.YNorm(), t_tag.YNorm() );
    EXPECT_EQ( tag.Value(), t_tag.Value() );
}

TEST_F(MantisNewAPITest, eapiGetNextFloatArray_P) {
    externalAnalysis::FloatArray t_fa = eapi.GetNextFloatArray();

    EXPECT_TRUE( aqt_STATUS_OKAY == eapi.GetStatus() );
    EXPECT_EQ( fa.Value().size(), t_fa.Value().size() );
}

TEST_F(MantisNewAPITest_N, eapiGetNextFloatArray_N) {
    externalAnalysis::FloatArray t_fa = eapi.GetNextFloatArray();

    EXPECT_FALSE( aqt_STATUS_OKAY == eapi.GetStatus() );
    EXPECT_EQ( fa.Value().size(), t_fa.Value().size() );
}

TEST_F(MantisNewAPITest, eapiGetNextU8Array_P) {
    externalAnalysis::U8Array t_ua = eapi.GetNextU8Array();

    EXPECT_TRUE( aqt_STATUS_OKAY == eapi.GetStatus() ); 
    EXPECT_EQ( ua.Value(), t_ua.Value() );
}

TEST_F(MantisNewAPITest_N, eapiGetNextU8Array_N) {
    externalAnalysis::U8Array t_ua = eapi.GetNextU8Array();

    EXPECT_FALSE( aqt_STATUS_OKAY == eapi.GetStatus() ); 
    EXPECT_EQ( ua.Value(), t_ua.Value() );
}

TEST_F(MantisNewAPITest, eapiGetNextCameraModel_P) {
    externalAnalysis::CameraModel t_cm = eapi.GetNextCameraModel();

    EXPECT_TRUE( aqt_STATUS_OKAY == eapi.GetStatus() ); 
    EXPECT_EQ( cm.Value(), t_cm.Value() );
}

TEST_F(MantisNewAPITest_N, eapiGetNextCameraModel_N) {
    externalAnalysis::CameraModel t_cm = eapi.GetNextCameraModel();

    EXPECT_FALSE( aqt_STATUS_OKAY == eapi.GetStatus() ); 
    EXPECT_EQ( cm.Value(), t_cm.Value() );
}

TEST_F(MantisNewAPITest, eapiGetNextThumbnail_P) {
    externalAnalysis::Thumbnail t_thumb = eapi.GetNextThumbnail();

    EXPECT_TRUE( aqt_STATUS_OKAY == eapi.GetStatus() );                    
    EXPECT_EQ( thumb.XNorm(), t_thumb.XNorm() );
    EXPECT_EQ( thumb.YNorm(), t_thumb.YNorm() );
    EXPECT_EQ( thumb.WidthNorm(), t_thumb.WidthNorm() );
    EXPECT_EQ( thumb.HeightNorm(), t_thumb.HeightNorm() );
}

TEST_F(MantisNewAPITest_N, eapiGetNextThumbnail_N) {
    externalAnalysis::Thumbnail t_thumb = eapi.GetNextThumbnail();

    EXPECT_FALSE( aqt_STATUS_OKAY == eapi.GetStatus() );                    
    EXPECT_EQ( thumb.XNorm(), t_thumb.XNorm() );
    EXPECT_EQ( thumb.YNorm(), t_thumb.YNorm() );
    EXPECT_EQ( thumb.WidthNorm(), t_thumb.WidthNorm() );
    EXPECT_EQ( thumb.HeightNorm(), t_thumb.HeightNorm() );
}

TEST_F(MantisNewAPITest, eapiInsertRectangle_P) {
    EXPECT_EQ( aqt_STATUS_OKAY, eapi.InsertTag(tag) );
}

TEST_F(MantisNewAPITest_N, eapiInsertRectangle_N) {
    EXPECT_EQ( aqt_STATUS_OKAY, eapi.InsertTag(tag) );
}

TEST_F(MantisNewAPITest, eapiInsertFloatArray_P) {
    EXPECT_EQ( aqt_STATUS_OKAY, eapi.InsertFloatArray(fa) );
}

TEST_F(MantisNewAPITest_N, eapiInsertFloatArray_N) {
    EXPECT_EQ( aqt_STATUS_OKAY, eapi.InsertFloatArray(fa) );
}

TEST_F(MantisNewAPITest, eapiInsertCameraModel_P) {
    EXPECT_EQ( aqt_STATUS_OKAY, eapi.InsertCameraModel(cm) );
}

TEST_F(MantisNewAPITest_N, eapiInsertCameraModel_N) {
    EXPECT_EQ( aqt_STATUS_OKAY, eapi.InsertCameraModel(cm) );
}

TEST_F(MantisNewAPITest, eapiInsertThumbnail_P) {
    EXPECT_EQ( aqt_STATUS_OKAY, eapi.InsertThumbnail(thumb) );
}

TEST_F(MantisNewAPITest_N, eapiInsertThumbnail_N) {
    EXPECT_EQ( aqt_STATUS_OKAY, eapi.InsertThumbnail(thumb) );
}

TEST_F(MantisNewAPITest, eapiSetStartTime_P) {
    EXPECT_EQ( aqt_STATUS_OKAY, eapi.SetStartTime(zeroTime) );
}

TEST_F(MantisNewAPITest_N, eapiSetStartTime_N) {
    EXPECT_EQ( aqt_STATUS_OKAY, eapi.SetStartTime(zeroTime) );
}

TEST_F(MantisNewAPITest, eapiSetImageTypes_P) {
    EXPECT_EQ( aqt_STATUS_OKAY, eapi.SetImageTypes(types) );
}

TEST_F(MantisNewAPITest_N, eapiSetImageTypes_N) {
    EXPECT_EQ( aqt_STATUS_OKAY, eapi.SetImageTypes(types) );
}

TEST_F(MantisNewAPITest, eapiSetMinSize_P) {
    EXPECT_EQ( aqt_STATUS_OKAY, eapi.SetMinSize(0, 0) );
}

TEST_F(MantisNewAPITest_N, eapiSetMinSize_N) {
    EXPECT_EQ( aqt_STATUS_OKAY, eapi.SetMinSize(0, 0) );
}

TEST_F(MantisNewAPITest, eapiSetMaxSize_P) {
    EXPECT_EQ( aqt_STATUS_OKAY, eapi.SetMaxSize(10000, 10000) );
}

TEST_F(MantisNewAPITest_N, eapiSetMaxSize_N) {
    EXPECT_EQ( aqt_STATUS_OKAY, eapi.SetMaxSize(10000, 10000) );
}

TEST_F(MantisNewAPITest, GetNextImage_P) {
    eapi.SetImageTypes(types);
    eapi.SetMinSize(0, 0);
    eapi.SetMaxSize(10000, 10000);

    Image t_img = eapi.GetNextImage();

    EXPECT_TRUE( aqt_STATUS_OKAY == eapi.GetStatus() );
    EXPECT_EQ( t_img.Width(), t_img.Width() );
    EXPECT_EQ( t_img.Height(), t_img.Height() );

    t_img.ReleaseData();
}

TEST_F(MantisNewAPITest_N, GetNextImage_N) {
    Image t_img = eapi.GetNextImage();
    
    EXPECT_FALSE( aqt_STATUS_OKAY == eapi.GetStatus() );
    EXPECT_EQ( t_img.Width(), t_img.Width() );
    EXPECT_EQ( t_img.Height(), t_img.Height() );

    t_img.ReleaseData();
}

TEST_F(MantisNewAPITest, GetAvailableCameras_P) {
    vector<aqt::SingleCOPCameraDescription> cams = api.GetAvailableCameras();

    EXPECT_TRUE( aqt_STATUS_OKAY == eapi.GetStatus() );
    EXPECT_EQ( cams.size(), num_of_cams );
}

TEST_F(MantisNewAPITest_N, GetAvailableCameras_N) {
    vector<aqt::SingleCOPCameraDescription> cams = api.GetAvailableCameras();

    EXPECT_FALSE( aqt_STATUS_OKAY == eapi.GetStatus() );
    EXPECT_EQ( cams.size(), num_of_cams );
}

TEST_F(MantisNewAPITest, Extrinsic_P) {
    vector<aqt::SingleCOPCameraDescription> cams = api.GetAvailableCameras();

    for (size_t i = 0; i < cams.size(); i++) {        
        ASSERT_TRUE( cams[i].Extrinsic() != aqt::UNDEFINED_EXTRINSIC );
        aqt::ExtrinsicCalibration t_ec = cams[i].Extrinsic();
            
        EXPECT_EQ( ec.Latitude(), ec.Latitude() );
        EXPECT_EQ( ec.Longitude(), ec.Longitude() );
        EXPECT_EQ( ec.Altitude(), ec.Altitude() );
        EXPECT_EQ( ec.Roll(), ec.Roll() );
        EXPECT_EQ( ec.Pitch(), ec.Pitch() );
        EXPECT_EQ( ec.Yaw(), ec.Yaw() );

        for (size_t j = 0; j < cams[i].Intrinsics().size(); j++) { 
            ASSERT_TRUE( cams[i].Intrinsics()[j] != aqt::UNDEFINED_INTRINSIC );           
            aqt::IntrinsicCalibration t_ic = cams[i].Intrinsics()[j];
    
            EXPECT_EQ( ic.WidthDegrees(), t_ic.WidthDegrees() );
            EXPECT_EQ( ic.HeightDegrees(), t_ic.HeightDegrees() );
            EXPECT_EQ( ic.PixelSizeDegrees(), t_ic.PixelSizeDegrees() );
        }      
    }
}

TEST_F(MantisNewAPITest_N, ExtrinsicIntrinsic_N) {
    vector<aqt::SingleCOPCameraDescription> cams = api.GetAvailableCameras();

    for (size_t i = 0; i < cams.size(); i++) {        
        ASSERT_TRUE( cams[i].Extrinsic() != aqt::UNDEFINED_EXTRINSIC );
        aqt::ExtrinsicCalibration t_ec = cams[i].Extrinsic();
            
        EXPECT_EQ( ec.Latitude(), ec.Latitude() );
        EXPECT_EQ( ec.Longitude(), ec.Longitude() );
        EXPECT_EQ( ec.Altitude(), ec.Altitude() );
        EXPECT_EQ( ec.Roll(), ec.Roll() );
        EXPECT_EQ( ec.Pitch(), ec.Pitch() );
        EXPECT_EQ( ec.Yaw(), ec.Yaw() );

        for (size_t j = 0; j < cams[i].Intrinsics().size(); j++) { 
            ASSERT_TRUE( cams[i].Intrinsics()[j] != aqt::UNDEFINED_INTRINSIC );           
            aqt::IntrinsicCalibration t_ic = cams[i].Intrinsics()[j];
    
            EXPECT_EQ( ic.WidthDegrees(), t_ic.WidthDegrees() );
            EXPECT_EQ( ic.HeightDegrees(), t_ic.HeightDegrees() );
            EXPECT_EQ( ic.PixelSizeDegrees(), t_ic.PixelSizeDegrees() );
        }      
    }
}



int main(int argc, char **argv) {
    ::testing::InitGoogleTest( &argc, argv );
	
	::testing::GTEST_FLAG(filter) = "*_P";
	RUN_ALL_TESTS();

	return 0;
}
