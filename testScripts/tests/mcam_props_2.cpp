//checking auto properties

#include "tests.h"

using namespace td;

vector<MICRO_CAMERA> mCamList;

void newMCamCallback(MICRO_CAMERA mcam, void* data)
{
    mCamList.push_back(mcam);
}

void mcamFrameCallback(FRAME frame, void* data)
{

}

struct result{
	bool rc;
	bool auto_rc_f;
	bool auto_rc_t;
	double exp;
	double act1; //value that acosd was able to set
	double act2; //value that set by auto funcs
};

int main(int argc, char * argv[])
{
	Env::setUp("mcam_props_2");

	map<string, result> res_map;
	vector<map<string, result> > res;

	mCamConnect(mcam_ip, port);

	NEW_MICRO_CAMERA_CALLBACK mcamCB;
	mcamCB.f = newMCamCallback;
	mcamCB.data = NULL;
	setNewMCamCallback(mcamCB);

	MICRO_CAMERA_FRAME_CALLBACK frameCB;
	frameCB.f = mcamFrameCallback;
	frameCB.data = NULL;
	setMCamFrameCallback(frameCB);

	for (int i = 0; i < getNumberOfMCams(); i++) {
		//initMCamFrameReceiver(r_port + i, 1.0);
		//startMCamStream(mCamList[i], r_port + i);

		res.push_back(res_map);

		res[i]["Exposure"].auto_rc_f = setMCamAutoExposure(mCamList[i], false);
		res[i]["Framerate"].auto_rc_f = setMCamAutoFramerate(mCamList[i], false);
		res[i]["JpegQuality"].auto_rc_f = setMCamAutoJpegQuality(mCamList[i], false);
		res[i]["Gain"].auto_rc_f = setMCamAutoGain(mCamList[i], false);
		res[i]["Saturation"].auto_rc_f = setMCamAutoSaturation(mCamList[i], false);
		res[i]["Shutter"].auto_rc_f = setMCamAutoShutter(mCamList[i], false);
		res[i]["Contrast"].auto_rc_f = setMCamAutoContrast(mCamList[i], false);
		res[i]["Sharpening"].auto_rc_f = setMCamAutoSharpening(mCamList[i], false);
		res[i]["DeNoise"].auto_rc_f = setMCamAutoDeNoise(mCamList[i], false);

		res[i]["Exposure"].exp = 1.0; //getRnd(getMCamExposureRange(mCamList[i]));
		res[i]["Framerate"].exp = getRnd(getMCamFramerateRange(mCamList[i]));
		res[i]["JpegQuality"].exp = getRnd(getMCamJpegQualityRange(mCamList[i]));
		res[i]["Gain"].exp = getRnd(getMCamGainRange(mCamList[i]));
		res[i]["Saturation"].exp = getRnd(getMCamSaturationRange(mCamList[i]));
		res[i]["Shutter"].exp = getRnd(getMCamShutterRange(mCamList[i]));
		res[i]["Contrast"].exp = getRnd(getMCamContrastRange(mCamList[i]));
		res[i]["Sharpening"].exp = getRnd(getMCamSharpeningRange(mCamList[i]));
		res[i]["DeNoise"].exp = getRnd(getMCamDeNoiseRange(mCamList[i]));

		res[i]["Exposure"].rc = setMCamExposure(mCamList[i], res[i]["Exposure"].exp);
		res[i]["Framerate"].rc = setMCamFramerate(mCamList[i], res[i]["Framerate"].exp);
		res[i]["JpegQuality"].rc = setMCamJpegQuality(mCamList[i], res[i]["JpegQuality"].exp);
		res[i]["Gain"].rc = setMCamGain(mCamList[i], res[i]["Gain"].exp);
		res[i]["Saturation"].rc = setMCamSaturation(mCamList[i], res[i]["Saturation"].exp);
		res[i]["Shutter"].rc = setMCamShutter(mCamList[i], res[i]["Shutter"].exp);
		res[i]["Contrast"].rc = setMCamContrast(mCamList[i], res[i]["Contrast"].exp);
		res[i]["Sharpening"].rc = setMCamSharpening(mCamList[i], res[i]["Sharpening"].exp);
		res[i]["DeNoise"].rc = setMCamDeNoise(mCamList[i], res[i]["DeNoise"].exp);

		sleep(2);

		res[i]["Exposure"].act1 = getMCamExposure(mCamList[i]);
		res[i]["Framerate"].act1 = getMCamFramerate(mCamList[i]);
		res[i]["JpegQuality"].act1 = getMCamJpegQuality(mCamList[i]);
		res[i]["Gain"].act1 = getMCamGain(mCamList[i]);
		res[i]["Saturation"].act1 = getMCamSaturation(mCamList[i]);
		res[i]["Shutter"].act1 = getMCamShutter(mCamList[i]);
		res[i]["Contrast"].act1 = getMCamContrast (mCamList[i]);
		res[i]["Sharpening"].act1 = getMCamSharpening(mCamList[i]);
		res[i]["DeNoise"].act1 = getMCamDeNoise(mCamList[i]);
	}

    for (int i = 0; i < getNumberOfMCams(); i++) {
    	res[i]["Exposure"].auto_rc_t = setMCamAutoExposure(mCamList[i], true);
    	res[i]["Framerate"].auto_rc_t = setMCamAutoFramerate(mCamList[i], true);
    	res[i]["JpegQuality"].auto_rc_t = setMCamAutoJpegQuality(mCamList[i], true);
    	res[i]["Gain"].auto_rc_t = setMCamAutoGain(mCamList[i], true);
    	res[i]["Saturation"].auto_rc_t = setMCamAutoSaturation(mCamList[i], true);
    	res[i]["Shutter"].auto_rc_t = setMCamAutoShutter(mCamList[i], true);
    	res[i]["Contrast"].auto_rc_t = setMCamAutoContrast(mCamList[i], true);
    	res[i]["Sharpening"].auto_rc_t = setMCamAutoSharpening(mCamList[i], true);
    	res[i]["DeNoise"].auto_rc_t = setMCamAutoDeNoise(mCamList[i], true);

		sleep(2);

		res[i]["Exposure"].act2 = getMCamExposure(mCamList[i]);
		res[i]["Framerate"].act2 = getMCamFramerate(mCamList[i]);
		res[i]["JpegQuality"].act2 = getMCamJpegQuality(mCamList[i]);
		res[i]["Gain"].act2 = getMCamGain(mCamList[i]);
		res[i]["Saturation"].act2 = getMCamSaturation(mCamList[i]);
		res[i]["Shutter"].act2 = getMCamShutter(mCamList[i]);
		res[i]["Contrast"].act2 = getMCamContrast (mCamList[i]);
		res[i]["Sharpening"].act2 = getMCamSharpening(mCamList[i]);
		res[i]["DeNoise"].act2 = getMCamDeNoise(mCamList[i]);

		//stopMCamStream(mCamList[i], r_port + i);
		//closeMCamFrameReceiver(r_port + i);
    }

    mCamDisconnect(mcam_ip, port);

	for (int i = 0; i <res.size(); i++) {
		cout << "mcamID: " << mCamList[i].mcamID << endl;
		cout << "\t\t" << "exp\t" << "act1\t" << "act2\t" << "rc\t" << "rc_f\t" << "rc_t" << endl;
		map<string, result>::iterator it = res[i].begin();

		while (it != res[i].end())
		{
			cout << setprecision(2)
				 << it->first << "\t"
				 << (it->first.length() < 8 ? "\t" : "")
				 << it->second.exp << "\t"
				 << it->second.act1 << "\t"
				 << it->second.act2 << "\t"
				 << it->second.rc << "\t"
				 << it->second.auto_rc_f << "\t"
				 << it->second.auto_rc_t << "\t"
				 << ((it->second.rc == 1 && it->second.auto_rc_f != 0 && it->second.auto_rc_t != 0) ? ((abs(it->second.act1 - it->second.exp) < 0.01 && ((it->second.act1 - it->second.exp) != 0)) ? "pass" : "fail" ) : "n/a")
				 << endl;
			if(act_res && it->second.rc == 1 && it->second.auto_rc_f != 0 && it->second.auto_rc_t != 0) act_res = (abs(it->second.act1 - it->second.exp) < 0.01 && ((it->second.act1 - it->second.exp) != 0));
			it++;
		}
		cout << endl;
	}

	Env::tearDown();

    return 0;
}
