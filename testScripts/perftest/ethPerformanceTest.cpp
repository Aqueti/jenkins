#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/time.h>
#include <map>
#include <list>
#include <iterator>

#include "mantis/MantisAPI.h"
#include "gtest/gtest.h"

using namespace std;

void newMCamCallback(MICRO_CAMERA mcam, void* data)
{
    MICRO_CAMERA* _mcam = (MICRO_CAMERA*) data;
    *_mcam = mcam;
}

void mcamFrameCallback(FRAME frame, void* data)
{
    std::list<FRAME> *_frames = (std::list<FRAME>*)data;
    _frames->push_back(frame);
}

size_t getSize(std::list<FRAME> frames) {
    size_t size = 0;

    std::list<FRAME>::iterator it = frames.begin();
    while (it != frames.end())
    {
        size += (it++)->m_metadata.m_size;
    }

    return size;
}

struct PAIR {
    double cm;
    double nw;
};

class mTestParams {
  public:
    mTestParams() {
        ip = "192.168.10.6";
        port = 9999;
        r_port = 11001;
        delta = 5e3;
        avg = (int)1e6/30 + delta;
        num_of_steps = 10;
        c_period = 1; //67
    }

    char *ip;
    int port;
    int r_port;
    int delta;
    int avg;
    int c_period;
    int num_of_steps;
    std::string c_param;
    MICRO_CAMERA mcam;
    std::list<FRAME> frames;
    std::list<PAIR> res;
    std::map<std::string, PAIR_DOUBLE> range;
    std::map<std::string, double> params;
};

class EthPerformanceTest  : public ::testing::Test {
  protected:
    mTestParams *mtp;

    virtual void SetUp() {
        initMCamFrameReceiver(mtp->r_port, 1.0);

        mCamConnect(mtp->ip, mtp->port);

        NEW_MICRO_CAMERA_CALLBACK mcamCB;
        mcamCB.f = newMCamCallback;
        mcamCB.data = &mtp->mcam;
        setNewMCamCallback(mcamCB);

        MICRO_CAMERA_FRAME_CALLBACK frameCB;
        frameCB.f = mcamFrameCallback;
        frameCB.data = &mtp->frames;
        setMCamFrameCallback(frameCB);

        startMCamStream(mtp->mcam, mtp->r_port);

        setMtpRange();

        setMtpParams();

        turnAuto("off");

        setParams("min");
    }

    virtual void TearDown() {
        stopMCamStream(mtp->mcam, mtp->r_port);

        mCamDisconnect(mtp->ip, mtp->port);

        closeMCamFrameReceiver(mtp->r_port);
    }

    EthPerformanceTest() {
        mtp = new mTestParams();
    }

    void turnAuto(std::string str) {
        bool is_on = (str == "on") ? true : false;

        setMCamAutoExposure(mtp->mcam, is_on);
        setMCamAutoFramerate(mtp->mcam, is_on);
        setMCamAutoJpegQuality(mtp->mcam, is_on);
        setMCamAutoGain(mtp->mcam, is_on);
        setMCamAutoSaturation(mtp->mcam, is_on);
        setMCamAutoShutter(mtp->mcam, is_on);
        setMCamAutoContrast(mtp->mcam, is_on);
        setMCamAutoSharpening(mtp->mcam, is_on);
        setMCamAutoDeNoise(mtp->mcam, is_on);
        //setMCamAutoFocus(mtp->mcam, 25.0);
    }

    void setParams(std::string str) {
        AtlWhiteBalance wb;
        wb.red = mtp->range["whitebalance"].first + 1.0; //issue
        wb.blue = wb.red;
        wb.green = wb.red;

        AtlCompressionParameters cp;

        if (str == "min") {
            setMCamGain(mtp->mcam, mtp->range["gain"].first);
            setMCamExposure(mtp->mcam, mtp->range["exposure"].first);
            setMCamShutter(mtp->mcam, mtp->range["shutter"].first);
            setMCamSaturation(mtp->mcam, mtp->range["saturation"].first);
            setMCamFramerate(mtp->mcam, mtp->range["framerate"].first);
            setMCamContrast(mtp->mcam, mtp->range["contrast"].first);
            setMCamDeNoise(mtp->mcam, mtp->range["denoise"].first);
            setMCamSharpening(mtp->mcam, mtp->range["sharpening"].first);
            setMCamJpegQuality(mtp->mcam, 50.0);
            //setMCamWhiteBalance(mtp->mcam, wb);
        }
        else if ("max") {
            setMCamGain(mtp->mcam, mtp->range["gain"].second);
            setMCamExposure(mtp->mcam, mtp->range["exposure"].second);
            setMCamShutter(mtp->mcam, mtp->range["shutter"].second);
            setMCamSaturation(mtp->mcam, mtp->range["saturation"].second);
            setMCamFramerate(mtp->mcam, mtp->range["framerate"].second);
            setMCamContrast(mtp->mcam, mtp->range["contrast"].second);
            setMCamDeNoise(mtp->mcam, mtp->range["denoise"].second);
            setMCamSharpening(mtp->mcam, mtp->range["sharpening"].second);
            setMCamJpegQuality(mtp->mcam, 50.0);
            //setMCamWhiteBalance(mtp->mcam, wb);
        }
        else {
            //
        }
    }

    void setMtpRange() {
        mtp->range["gain"] = getMCamGainRange(mtp->mcam);
        mtp->range["exposure"] = getMCamExposureRange(mtp->mcam);
        mtp->range["shutter"] = getMCamShutterRange(mtp->mcam);
        mtp->range["saturation"] = getMCamSaturationRange(mtp->mcam);
        mtp->range["framerate"] = getMCamFramerateRange(mtp->mcam);
        mtp->range["contrast"] = getMCamContrastRange(mtp->mcam);
        mtp->range["denoise"] = getMCamDeNoiseRange(mtp->mcam);
        mtp->range["sharpening"] = getMCamSharpeningRange(mtp->mcam);
        mtp->range["jpegquality"] = getMCamJpegQualityRange(mtp->mcam);
        mtp->range["whitebalance"] = getMCamWhiteBalanceRange(mtp->mcam);
    }

    void setMtpParams() {
        mtp->params["gain"] = getMCamGain(mtp->mcam);
        mtp->params["exposure"] = getMCamExposure(mtp->mcam);
        mtp->params["shutter"] = getMCamShutter(mtp->mcam);
        mtp->params["saturation"] = getMCamSaturation(mtp->mcam);
        mtp->params["framerate"] = getMCamFramerate(mtp->mcam);
        mtp->params["contrast"] = getMCamContrast(mtp->mcam);
        mtp->params["denoise"] = getMCamDeNoise(mtp->mcam);
        mtp->params["sharpening"] = getMCamSharpening(mtp->mcam);
        mtp->params["jpegquality"] = getMCamJpegQuality(mtp->mcam);
        //mtp->params["whitebalance"] = getMCamWhiteBalance(mtp->mcam);
    }

    void clean() {
        mtp->res.clear();

        setParams("min");

        sleep(1);

        mtp->frames.clear();
    }

    void writeToFile(string str, char* file_name, bool w_method = true) {
        std::ofstream fout;

        if (w_method) {
            fout.open(file_name, ios::out | ios::app);
        }
        else {
            fout.open(file_name, ios::out);
        }

        fout << str;
        fout.close();
    }

    string readFromFile(string file_name) {
        ostringstream ss;
        ifstream fin(file_name);
        if (fin.is_open()) {
            string str;
            ifstream fin(file_name);

            while (getline(fin, str)) {
                ss << str << endl;
            }
            fin.close();
        }

        return ss.str();
    }

    double getAvgFrameSize() {
        double size = 0;

        std::list<FRAME>::iterator it = mtp->frames.begin();
        while (it != mtp->frames.end())
        {
            size += (double)(it++)->m_metadata.m_size;
        }

        return size/mtp->frames.size();
    }

    void addToRes(double val) {
        PAIR pair;
        pair.cm = val;
        pair.nw = getAvgFrameSize();

        mtp->res.push_back(pair);
    }

    void print_params() {
        std::map<std::string, double>::iterator it = mtp->params.begin();
        while (it != mtp->params.end())
        {
            printf("%s: %f\n", it->first, it->second); it++;
        }
    }

    void print_result() {
        printf("%s\t%s\n", mtp->c_param.c_str(), "eth");
        std::list<PAIR>::iterator it = mtp->res.begin();
        while (it != mtp->res.end())
        {
            printf("%.2f\t%.2f\n", it->cm, it->nw); it++;
        }

        printf("\n");
    }

    void write_result() {
        char *file_name = "ethperftest.txt";

        ostringstream ss;

        ss << mtp->c_param.c_str() << '\t'
           << "avg_frame_size" << endl;

        std::list<PAIR>::iterator it = mtp->res.begin();
        while (it != mtp->res.end())
        {
            ss << setprecision(2) << it->cm << it->nw << endl; it++;
        }

        writeToFile(ss.str(), file_name);
    }
};

TEST_F(EthPerformanceTest, test) {
    double pos;
    double step;

    std::map<std::string, PAIR_DOUBLE>::iterator it = mtp->range.begin();
    while (it != mtp->range.end())
    {
        mtp->c_param = it->first;
        pos = it->second.first;
        step = (it->second.second - it->second.first) / mtp->num_of_steps;

        while(pos <= it->second.second) {
            if (mtp->c_param == "gain") {
                setMCamGain(mtp->mcam, pos);
            } else if (mtp->c_param == "exposure") {
                setMCamExposure(mtp->mcam, pos);
            } else if (mtp->c_param == "shutter") {
                setMCamShutter(mtp->mcam, pos);
            } else if (mtp->c_param == "exposure") {
                setMCamExposure(mtp->mcam, pos);
            } else if (mtp->c_param == "saturation") {
                setMCamSaturation(mtp->mcam, pos);
            } else if (mtp->c_param == "framerate") {
                setMCamFramerate(mtp->mcam, pos);
            } else if (mtp->c_param == "contrast") {
                setMCamContrast(mtp->mcam, pos);
            } else if (mtp->c_param == "denoise") {
                setMCamDeNoise(mtp->mcam, pos);
            } else if (mtp->c_param == "sharpening") {
                setMCamSharpening(mtp->mcam, pos);
            }  else if (mtp->c_param == "jpegquality") {
                setMCamJpegQuality(mtp->mcam, pos);
            } else {

            }

            sleep(mtp->c_period);
            addToRes(pos);

            mtp->frames.clear();

            pos += step;
        }

        print_result();
        write_result();

        clean();

        it++;
    }
}



int main(int argc, char *argv[])
{
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
