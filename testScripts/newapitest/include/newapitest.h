#ifndef MANTISNEWAPITEST_H
#define MANTISNEWAPITEST_H

#include <cstring>
#include <string>
#include <sstream>
#include <fstream>
#include <time.h>
#include <sys/time.h>
#include <sys/stat.h>
#include <cmath>
#include <map>
#include <list>
#include <vector>
#include <iterator>
#include <exception>

#include "gtest/gtest.h"
#include "aqt_api.hpp"

using namespace std;
using namespace aqt;

class TestParams {
public:
    externalAnalysis::Rectangle rect;
    externalAnalysis::Tag tag;
    externalAnalysis::FloatArray fa;
    externalAnalysis::U8Array ua;
    externalAnalysis::CameraModel cm;
    externalAnalysis::Thumbnail thumb;

    struct timeval zeroTime;
    vector<aqt_ImageType> types;
    map<string, int> num_of;

    ExtrinsicCalibration ec;
    IntrinsicCalibration ic;
        
    TestParams();

    ~TestParams();
};

class MantisNewAPITest : public ::testing::Test, public TestParams
{
  protected:
    virtual void SetUp() {}
    virtual void TearDown() {}
};

class MantisNewAPITest_N : public ::testing::Test, public TestParams
{
  protected:
    virtual void SetUp() {}
    virtual void TearDown() {}
};

#endif
