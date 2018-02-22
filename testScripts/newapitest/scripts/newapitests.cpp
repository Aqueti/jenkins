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
 }

TestParams::~TestParams() {

}

AquetiAPI api;
externalAnalysis::ExternalAnalysis eapi(api, "/aqt/SCOP/mantis1/microcamera2");

TEST_F(MantisNewAPITest, eapiGetNextRectangle_P) {
    externalAnalysis::Rectangle t_rect = eapi.GetNextRectangle();
    bool act_res = (aqt_STATUS_OKAY == eapi.GetStatus() &&
                    rect.XNorm() == t_rect.XNorm() && 
                    rect.YNorm() == t_rect.YNorm() &&
                    rect.WidthNorm() == t_rect.WidthNorm() &&
                    rect.HeightNorm() == t_rect.HeightNorm());

    EXPECT_TRUE(act_res);   
}

TEST_F(MantisNewAPITest, eapiGetNextRectangle_N) {
    externalAnalysis::Rectangle t_rect = eapi.GetNextRectangle();
    bool act_res = (aqt_STATUS_OKAY == eapi.GetStatus() ||
                    rect.XNorm() == t_rect.XNorm() || 
                    rect.YNorm() == t_rect.YNorm() ||
                    rect.WidthNorm() == t_rect.WidthNorm() ||
                    rect.HeightNorm() == t_rect.HeightNorm());

    EXPECT_FALSE(act_res);
}

TEST_F(MantisNewAPITest, eapiGetNextTag_P) {
    externalAnalysis::Tag t_tag = eapi.GetNextTag();
    bool act_res = (aqt_STATUS_OKAY == eapi.GetStatus() &&
                    tag.XNorm() == t_tag.XNorm() && 
                    tag.YNorm() == t_tag.YNorm() &&
                    tag.Value() == t_tag.Value());

    EXPECT_TRUE(act_res);
}

TEST_F(MantisNewAPITest, eapiGetNextTag_N) {
    externalAnalysis::Tag t_tag = eapi.GetNextTag();
    bool act_res = (aqt_STATUS_OKAY == eapi.GetStatus() ||
                    tag.XNorm() == t_tag.XNorm() || 
                    tag.YNorm() == t_tag.YNorm() ||
                    tag.Value() == t_tag.Value());

    EXPECT_FALSE(act_res);
}

TEST_F(MantisNewAPITest, eapiGetNextFloatArray_P) {
    externalAnalysis::FloatArray t_fa = eapi.GetNextFloatArray();
    bool act_res = (aqt_STATUS_OKAY == eapi.GetStatus() &&
                    fa.Value().size() == t_fa.Value().size());

    EXPECT_TRUE(act_res);
}

TEST_F(MantisNewAPITest, eapiGetNextFloatArray_N) {
    externalAnalysis::FloatArray t_fa = eapi.GetNextFloatArray();
    bool act_res = (aqt_STATUS_OKAY == eapi.GetStatus() ||
                    fa.Value().size() == t_fa.Value().size());

    EXPECT_FALSE(act_res);
}

TEST_F(MantisNewAPITest, eapiGetNextU8Array_P) {
    externalAnalysis::U8Array t_ua = eapi.GetNextU8Array();
    bool act_res = (aqt_STATUS_OKAY == eapi.GetStatus() &&
                    ua.Value().size() == t_ua.Value().size());

    EXPECT_TRUE(act_res);
}

TEST_F(MantisNewAPITest, eapiGetNextU8Array_N) {
    externalAnalysis::U8Array t_ua = eapi.GetNextU8Array();
    bool act_res = (aqt_STATUS_OKAY == eapi.GetStatus() ||
                    ua.Value().size() == t_ua.Value().size());

    EXPECT_FALSE(act_res);
}

TEST_F(MantisNewAPITest, eapiGetNextCameraModel_P) {
    externalAnalysis::CameraModel t_cm = eapi.GetNextCameraModel();
    bool act_res = (aqt_STATUS_OKAY == eapi.GetStatus() && 
                    cm.Value() == t_cm.Value());

    EXPECT_TRUE(act_res);
}

TEST_F(MantisNewAPITest, eapiGetNextCameraModel_N) {
    externalAnalysis::CameraModel t_cm = eapi.GetNextCameraModel();
    bool act_res = (aqt_STATUS_OKAY == eapi.GetStatus() || 
                    cm.Value() == t_cm.Value());

    EXPECT_FALSE(act_res);
}

TEST_F(MantisNewAPITest, eapiGetNextThumbnail_P) {
    externalAnalysis::Thumbnail t_thumb = eapi.GetNextThumbnail();
    bool act_res = (aqt_STATUS_OKAY == eapi.GetStatus() &&                    
                    thumb.XNorm() == t_thumb.XNorm() && 
                    thumb.YNorm() == t_thumb.YNorm() &&
                    thumb.WidthNorm() == t_thumb.WidthNorm() &&
                    thumb.HeightNorm() == t_thumb.HeightNorm());

    EXPECT_TRUE(act_res);
}

TEST_F(MantisNewAPITest, eapiGetNextThumbnail_N) {
    externalAnalysis::Thumbnail t_thumb = eapi.GetNextThumbnail();
    bool act_res = (aqt_STATUS_OKAY == eapi.GetStatus() ||                    
                    thumb.XNorm() == t_thumb.XNorm() ||
                    thumb.YNorm() == t_thumb.YNorm() ||
                    thumb.WidthNorm() == t_thumb.WidthNorm() ||
                    thumb.HeightNorm() == t_thumb.HeightNorm());

    EXPECT_FALSE(act_res);
}

TEST_F(MantisNewAPITest, eapiInsertRectangle_P) {
    bool act_res = (aqt_STATUS_OKAY == eapi.InsertTag(tag));

    EXPECT_TRUE(act_res);
}

TEST_F(MantisNewAPITest, eapiInsertRectangle_N) {
    bool act_res = (aqt_STATUS_OKAY == eapi.InsertTag(tag));

    EXPECT_FALSE(act_res);
}

TEST_F(MantisNewAPITest, eapiInsertFloatArray_P) {
    bool act_res = (aqt_STATUS_OKAY == eapi.InsertFloatArray(fa));

    EXPECT_TRUE(act_res);
}

TEST_F(MantisNewAPITest, eapiInsertFloatArray_N) {
    bool act_res = (aqt_STATUS_OKAY == eapi.InsertFloatArray(fa));

    EXPECT_FALSE(act_res);
}

TEST_F(MantisNewAPITest, eapiInsertCameraModel_P) {
    bool act_res = (aqt_STATUS_OKAY == eapi.InsertCameraModel(cm));

    EXPECT_TRUE(act_res);
}

TEST_F(MantisNewAPITest, eapiInsertCameraModel_N) {
    bool act_res = (aqt_STATUS_OKAY == eapi.InsertCameraModel(cm));

    EXPECT_FALSE(act_res);
}

TEST_F(MantisNewAPITest, eapiInsertThumbnail_P) {
    bool act_res = (aqt_STATUS_OKAY == eapi.InsertThumbnail(thumb));

    EXPECT_TRUE(act_res);
}

TEST_F(MantisNewAPITest, eapiInsertThumbnail_N) {
    bool act_res = (aqt_STATUS_OKAY == eapi.InsertThumbnail(thumb));

    EXPECT_FALSE(act_res);
}

TEST_F(MantisNewAPITest, eapiSetStartTime_P) {
    bool act_res = (aqt_STATUS_OKAY == eapi.SetStartTime(zeroTime));

    EXPECT_TRUE(act_res);
}

TEST_F(MantisNewAPITest, eapiSetStartTime_N) {
    bool act_res = (aqt_STATUS_OKAY == eapi.SetStartTime(zeroTime));

    EXPECT_FALSE(act_res);
}

TEST_F(MantisNewAPITest, eapiSetImageTypes_P) {
    bool act_res = (aqt_STATUS_OKAY == eapi.SetImageTypes(types));

    EXPECT_TRUE(act_res);
}

TEST_F(MantisNewAPITest, eapiSetImageTypes_N) {
    bool act_res = (aqt_STATUS_OKAY == eapi.SetImageTypes(types));

    EXPECT_FALSE(act_res);
}

TEST_F(MantisNewAPITest, eapiSetMinSize_P) {
    bool act_res = (aqt_STATUS_OKAY == eapi.SetMinSize(0, 0));

    EXPECT_TRUE(act_res);
}

TEST_F(MantisNewAPITest, eapiSetMinSize_N) {
    bool act_res = (aqt_STATUS_OKAY == eapi.SetMinSize(0, 0));

    EXPECT_FALSE(act_res);
}

TEST_F(MantisNewAPITest, eapiSetMaxSize_P) {
    bool act_res = (aqt_STATUS_OKAY == eapi.SetMaxSize(10000, 10000));

    EXPECT_TRUE(act_res);
}

TEST_F(MantisNewAPITest, eapiSetMaxSize_N) {
    bool act_res = (aqt_STATUS_OKAY == eapi.SetMaxSize(10000, 10000));

    EXPECT_FALSE(act_res);
}

TEST_F(MantisNewAPITest, GetNextImage_P) {
    eapi.SetImageTypes(types);
    eapi.SetMinSize(0, 0);
    eapi.SetMaxSize(10000, 10000);

    Image t_img = eapi.GetNextImage();
    bool act_res = (aqt_STATUS_OKAY == eapi.GetStatus() &&
                    t_img.Width() == t_img.Width() &&
                    t_img.Height() == t_img.Height());

    t_img.ReleaseData();

    EXPECT_TRUE(act_res);
}

TEST_F(MantisNewAPITest, GetNextImage_N) {
    Image t_img = eapi.GetNextImage();
    bool act_res = (aqt_STATUS_OKAY == eapi.GetStatus() ||
                    t_img.Width() == t_img.Width() ||
                    t_img.Height() == t_img.Height());

    t_img.ReleaseData();

    EXPECT_FALSE(act_res);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest( &argc, argv );
	
	::testing::GTEST_FLAG(filter) = "*_P";
	RUN_ALL_TESTS();

	return 0;
}
