#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/time.h>
#include <map>
#include <vector>
#include <list>
#include <iterator>

#include "mantis/MantisAPI.h"
#include "gtest/gtest.h"

using namespace std;

void newMCamCallback(MICRO_CAMERA mcam, void* data)
{
    static int i = 0;
    vector<MICRO_CAMERA>* _mcamList = (vector<MICRO_CAMERA>*) data;
    _mcamList->push_back(mcam);  
}

void mcamFrameCallback(FRAME frame, void* data)
{
    list<FRAME> *_frames = (list<FRAME>*)data;
    _frames->push_back(frame);
}

class TestParams {
  public:
    TestParams() {
        ip = "192.168.10.";
        port = 9999;
        r_port = 11001;     
        duration = 10;
        num_of_mcams = 0;
        
        bitrateModes.push_back("High");
        bitrateModes.push_back("Medium");
        bitrateModes.push_back("Low");

        bitrateMapH264["High"] = ATL_BITRATE_H264_HIGH;
        bitrateMapH264["Medium"] = ATL_BITRATE_H264_MEDIUM;
        bitrateMapH264["Low"] = ATL_BITRATE_H264_LOW;
        
        bitrateMapH265["High"] = ATL_BITRATE_H265_HIGH;
        bitrateMapH265["Medium"] = ATL_BITRATE_H265_MEDIUM;
        bitrateMapH265["Low"] = ATL_BITRATE_H265_LOW;
    }

    string ip;
    uint16_t port;
    uint16_t r_port;
    uint16_t duration;
    uint32_t num_of_mcams;
    
    vector<MICRO_CAMERA> mcamList;
    AtlCompressionParameters cp;
    map<string, size_t> res;
    list<FRAME> frames;

    vector<string> bitrateModes;
    map<string, int> bitrateMapH264;
    map<string, int> bitrateMapH265;
};

class NetworkUsage : public TestParams, public ::testing::TestWithParam<int> {
  protected:
    virtual void SetUp() {
        ostringstream ss;
        ss << ip << GetParam();
        ip = ss.str();

        cout << "ip: " << ip << endl;

        mCamConnect(ip.c_str(), port);

        num_of_mcams = getNumberOfMCams();

        NEW_MICRO_CAMERA_CALLBACK mcamCB;
        mcamCB.f = newMCamCallback;
        mcamCB.data = &mcamList;
        setNewMCamCallback(mcamCB);

        MICRO_CAMERA_FRAME_CALLBACK frameCB;
        frameCB.f = mcamFrameCallback;
        frameCB.data = &frames;
        setMCamFrameCallback(frameCB);

        for (int i = 0; i < num_of_mcams; i++) {
            initMCamFrameReceiver(r_port + i, 1.0);          
            startMCamStream(mcamList[i], r_port + i);
        }
    }

    virtual void TearDown() {
        for (int i = 0; i < num_of_mcams; i++) {
            stopMCamStream(mcamList[i], r_port + i);
            closeMCamFrameReceiver(r_port + i);
        }

        mCamDisconnect(ip.c_str(), port);
    }

    double getAvgSize() {
        double size = 0;

        std::list<FRAME>::iterator it = frames.begin();
        while (it != frames.end())
        {
            size += (double)(it++)->m_metadata.m_size;
        }

        return size/frames.size();
    }

    size_t getSize() {
        size_t size = 0;

        for(list<FRAME>::iterator it = frames.begin(); it != frames.end(); it++)      
        {
            size += it->m_metadata.m_size;
        }

        return size;
    }

    void print_result() {
        for (map<string, size_t>::iterator it = res.begin(); it != res.end(); it++)
        {
            cout << it->first << "\t" << it->second << endl;
        }
        cout << endl;
    }
};

INSTANTIATE_TEST_CASE_P(Test, NetworkUsage,
                        ::testing::Range(6, 10));

TEST_P(NetworkUsage, test) {
    for (int i = 0; i < bitrateModes.size(); i++) { 
        for (int j = 0; j < num_of_mcams; j++) {
            cp = getMCamCompressionParameters( mcamList[i] );
          
            if(cp.type == ATL_COMPRESSION_TYPE_H264) {
                cp.target_bitrate = bitrateMapH264[bitrateModes[j]];
            } else if(cp.type == ATL_COMPRESSION_TYPE_H265 ) {
                cp.target_bitrate = bitrateMapH265[bitrateModes[j]];
            }

            setMCamCompressionParameters( mcamList[i], cp);
        }

        frames.clear();
        sleep(duration);
        res[bitrateModes[i]] = getSize();
    }

    print_result();
}

int main(int argc, char *argv[])
{
    ::testing::InitGoogleTest(&argc, argv);

    return RUN_ALL_TESTS();
}
