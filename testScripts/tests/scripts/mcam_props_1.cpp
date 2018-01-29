/**
 * Checking:
 * properties values after reconnecting
 * 
 **/

#include "tests.h"

using namespace td;

vector<MICRO_CAMERA> mCamList;

void newCameraCallback(ACOS_CAMERA mcam, void* data)
{
    ACOS_CAMERA* _mcam = (ACOS_CAMERA*) data;
    *_mcam = mcam;
}

void mcamFrameCallback(FRAME frame, void* data)
{
    std::cout << frame.m_metadata.m_camId << ": " << frame.m_metadata.m_timestamp << '\n';
}

void newMCamCallback(MICRO_CAMERA mcam, void* data)
{
    mCamList.push_back(mcam);
}

struct Result{
	bool rc;
	double exp;
	double act;
};

int main(int argc, char * argv[])
{
	Env::setUp("mcam_props_1");

	map<string, Result> res_map;
	vector<map<string, Result> > res;

	mCamConnect(mcam_ip, port);

	NEW_MICRO_CAMERA_CALLBACK mcamCB;
	mcamCB.f = newMCamCallback;
	setNewMCamCallback(mcamCB);

	AtlCompressionParameters cp = getMCamCompressionParameters(mCamList[0]);
	cp.qp_iframe = 20;

	for (int i = 0; i < getNumberOfMCams(); i++) {
		res.push_back(res_map);

		setMCamAutoExposure(mCamList[i], false);
		setMCamAutoFocus(mCamList[i], false);
		setMCamAutoFramerate(mCamList[i], false);
		setMCamAutoJpegQuality(mCamList[i], false);
		setMCamAutoGain(mCamList[i], false);
		setMCamAutoSaturation(mCamList[i], false);
		setMCamAutoShutter(mCamList[i], false);
		setMCamAutoContrast(mCamList[i], false);
		setMCamAutoSharpening(mCamList[i], false);
		setMCamAutoDeNoise(mCamList[i], false);

		res[i]["Exposure"].exp = getRnd(getMCamExposureRange(mCamList[i]));
		res[i]["FocusRelative"].exp = getRnd((PAIR_DOUBLE){0, 1});
		res[i]["FocusAbsolute"].exp = getRnd((PAIR_DOUBLE){0, 1});
		res[i]["FocusDefault"].exp = getRnd((AtlRange_32f){0, 1});
		res[i]["Framerate"].exp = getRnd(getMCamFramerateRange(mCamList[i]));
		res[i]["JpegQuality"].exp = round(getRnd(getMCamJpegQualityRange(mCamList[i])));
		res[i]["Gain"].exp = getRnd(getMCamGainRange(mCamList[i]));
		res[i]["Saturation"].exp = getRnd(getMCamSaturationRange(mCamList[i]));
		res[i]["Shutter"].exp = getRnd(getMCamShutterRange(mCamList[i]));
		res[i]["Contrast"].exp = getRnd(getMCamContrastRange(mCamList[i]));
		res[i]["Sharpening"].exp = getRnd(getMCamSharpeningRange(mCamList[i]));
		res[i]["DeNoise"].exp = getRnd(getMCamDeNoiseRange(mCamList[i]));
		res[i]["WB_red"].exp = getRnd(getMCamWhiteBalanceRange(mCamList[i]));
		res[i]["CParameters"].exp = cp.qp_iframe;
		res[i]["WBMode"].exp = getRnd((AtlRange_32f){0, 9});
		res[i]["SensorMode"].exp = getRnd((AtlRange_32f){0, 2});
		res[i]["IrFilter"].exp = getRnd((AtlRange_32f){0, 1});
		res[i]["FocalLength"].exp = getRnd((AtlRange_32f){1, 100});

		res[i]["Exposure"].rc = setMCamExposure(mCamList[i], res[i]["Exposure"].exp);
		res[i]["FocusRelative"].rc = setMCamFocusRelative(mCamList[i], res[i]["FocusRelative"].exp);
		res[i]["FocusAbsolute"].rc = setMCamFocusAbsolute(mCamList[i], res[i]["FocusAbsolute"].exp);
		res[i]["FocusDefault"].rc = setMCamFocusDefault(mCamList[i]);
		res[i]["Framerate"].rc = setMCamFramerate(mCamList[i], res[i]["Framerate"].exp);
		res[i]["JpegQuality"].rc = setMCamJpegQuality(mCamList[i], res[i]["JpegQuality"].exp);
		res[i]["Gain"].rc = setMCamGain(mCamList[i], res[i]["Gain"].exp);
		res[i]["Saturation"].rc = setMCamSaturation(mCamList[i], res[i]["Saturation"].exp);
		res[i]["Shutter"].rc = setMCamShutter(mCamList[i], res[i]["Shutter"].exp);
		res[i]["Contrast"].rc = setMCamContrast(mCamList[i], res[i]["Contrast"].exp);
		res[i]["Sharpening"].rc = setMCamSharpening(mCamList[i], res[i]["Sharpening"].exp);
		res[i]["DeNoise"].rc = setMCamDeNoise(mCamList[i], res[i]["DeNoise"].exp);
		res[i]["WB_red"].rc = setMCamWhiteBalance(mCamList[i], {res[i]["WB_red"].exp, 2.0, 1.0});
		res[i]["CParameters"].rc = setMCamCompressionParameters(mCamList[i], cp);
		res[i]["WBMode"].rc = setMCamWhiteBalanceMode(mCamList[i], res[i]["WBMode"].exp);
		res[i]["SensorMode"].rc = setMCamSensorMode(mCamList[i], res[i]["SensorMode"].exp);
		res[i]["IrFilter"].rc = setMCamIrFilter(mCamList[i], res[i]["IrFilter"].exp);
		res[i]["FocalLength"].rc = setMCamFocalLength(mCamList[i], res[i]["FocalLength"].exp);
	}

    mCamDisconnect(mcam_ip, port);

    sleep(2);

    mCamConnect(mcam_ip, port);

    for (int i = getNumberOfMCams(); i < 2*getNumberOfMCams(); i++) {
    	res[i]["Exposure"].act = getMCamExposure(mCamList[i]);
    	res[i]["Framerate"].act = getMCamFramerate(mCamList[i]);
    	res[i]["JpegQuality"].act = getMCamJpegQuality(mCamList[i]);
    	res[i]["Gain"].act = getMCamGain(mCamList[i]);
    	res[i]["Saturation"].act = getMCamSaturation(mCamList[i]);
    	res[i]["Shutter"].act = getMCamShutter(mCamList[i]);
    	res[i]["Contrast"].act = getMCamContrast (mCamList[i]);
    	res[i]["Sharpening"].act = getMCamSharpening(mCamList[i]);
    	res[i]["DeNoise"].act = getMCamDeNoise(mCamList[i]);
    	res[i]["WB_red"].act = getMCamWhiteBalance(mCamList[i]).red;
		res[i]["CParameters"].act = getMCamCompressionParameters(mCamList[i]).qp_iframe;
		res[i]["WBMode"].act = getMCamWhiteBalanceMode(mCamList[i]);
		res[i]["IrFilter"].act = getMCamIrFilter(mCamList[i]);
		res[i]["FocalLength"].act = getMCamFocalLength(mCamList[i]);
    }

	for (int i = 0; i <res.size(); i++) {
		cout << "mcamID: " << mCamList[i].mcamID << endl;
		cout << "\t\t" << "exp\t" << "act\t" << "rc\t" << "res" << endl;
		map<string, Result>::iterator it = res[i].begin();
		while (it != res[i].end())
		{
			cout << it->first << "\t"
				 << (it->first.length() < 8 ? "\t" : "")
				 << it->second.exp << "\t"
				 << it->second.act << "\t"
				 << it->second.rc << "\t"
				 << (it->second.rc ? ((abs(it->second.exp - it->second.act) < 0.01) ? "pass" : "fail") : "n/a")
				 << endl;
			if(act_res) act_res = abs(it->second.exp - it->second.act) < 0.01;
			it++;
		}
		cout << endl;
	}

    mCamDisconnect(mcam_ip, port);

    Env::tearDown();

    return 0;
}
