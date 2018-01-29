/**
 * Checking:
 * checking set/got properties values
 * 
 **/

#include "tests.h"

using namespace td;

struct result{
	bool rc;
	bool cb;
	double exp;
	double act;
};

vector<MICRO_CAMERA> mCamList;
map<string, result> res_map;
vector<map<string, result> > res;
int ind = 0;

void newMCamCallback(MICRO_CAMERA mcam, void* data)
{
    mCamList.push_back(mcam);
}

void colorTempCallback( MICRO_CAMERA mcam, void* data, double o, double n )
{
	res[ind]["ColorTemp"].cb = true;
}

void compressionCallback( MICRO_CAMERA mcam, void* data, AtlCompressionParameters o, AtlCompressionParameters n )
{
	res[ind]["CParameters"].cb = true;
}

void contrastCallback( MICRO_CAMERA mcam, void* data, double o, double n )
{
	res[ind]["Contrast"].cb = true;
}

void deNoiseCallback( MICRO_CAMERA mcam, void* data, double o, double n )
{
	res[ind]["DeNoise"].cb = true;
}

void exposureCallback( MICRO_CAMERA mcam, void* data, double o, double n )
{
	res[ind]["Exposure"].cb = true;
}

void focalLengthCallback( MICRO_CAMERA mcam, void* data, double o, double n )
{
	res[ind]["FocalLength"].cb = true;
}

void focusCallback( MICRO_CAMERA mcam, void* data, double o, double n )
{
	res[ind]["Focus"].cb = true;
}

void focusStateCallback( MICRO_CAMERA mcam, void* data, int o, int n )
{
	res[ind]["FocusState"].cb = true;
}

void framerateCallback( MICRO_CAMERA mcam, void* data, double o, double n )
{
	res[ind]["Framerate"].cb = true;
}

void gainCallback( MICRO_CAMERA mcam, void* data, double o, double n )
{
	res[ind]["Gain"].cb = true;
}

void irFilterCallback( MICRO_CAMERA mcam, void* data, bool o, bool n )
{
	res[ind]["IrFilter"].cb = true;
}

void jpegQualityCallback( MICRO_CAMERA mcam, void* data, double o, double n )
{
	res[ind]["JpegQuality"].cb = true;
}

void saturationCallback( MICRO_CAMERA mcam, void* data, double o, double n )
{
	res[ind]["Saturation"].cb = true;
}

void sharpeningCallback( MICRO_CAMERA mcam, void* data, double o, double n )
{
	res[ind]["Sharpening"].cb = true;
}

void shutterCallback( MICRO_CAMERA mcam, void* data, double o, double n )
{
	res[ind]["Shutter"].cb = true;
}

void whiteBalanceCallback( MICRO_CAMERA mcam, void* data, AtlWhiteBalance o, AtlWhiteBalance n )
{
	res[ind]["WB_red"].cb = true;
}

int main(int argc, char * argv[])
{
	Env::setUp("mcam_props_4");

	mCamConnect(mcam_ip, port);

	NEW_MICRO_CAMERA_CALLBACK mcamCB;
	mcamCB.f = newMCamCallback;
	mcamCB.data = &mCamList;
	setNewMCamCallback(mcamCB);

	AtlCompressionParameters cp = getMCamCompressionParameters(mCamList[0]);
	cp.qp_iframe = 20;

	MICRO_CAMERA_CALLBACKS cbs;
	cbs.colorTempCallback.f = colorTempCallback;
	cbs.compressionCallback.f = compressionCallback;
	cbs.contrastCallback.f = contrastCallback;
	cbs.deNoiseCallback.f = deNoiseCallback;
	cbs.exposureCallback.f = exposureCallback;
	cbs.focalLengthCallback.f = focalLengthCallback;
	cbs.focusCallback.f = focusCallback;
	cbs.focusStateCallback.f = focusStateCallback;
	cbs.framerateCallback.f = framerateCallback;
	cbs.gainCallback.f = gainCallback;
	cbs.irFilterCallback.f = irFilterCallback;
	cbs.jpegQualityCallback.f = jpegQualityCallback;
	cbs.saturationCallback.f = saturationCallback;
	cbs.sharpeningCallback.f = sharpeningCallback;
	cbs.shutterCallback.f = shutterCallback;
	cbs.whiteBalanceCallback.f = whiteBalanceCallback;

	for (int i = 0; i < getNumberOfMCams(); i++) {
		res.push_back(res_map); ind = i;

		setMCamPropertyCallbacks( mCamList[i], cbs );

		res[i]["Exposure"].exp = getRnd(getMCamExposureRange(mCamList[i]));
		res[i]["FocusRelative"].exp = 0.41;
		res[i]["FocusAbsolute"].exp = 0.41;
		res[i]["FocusState"].exp = 0;
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

		setMCamAutoExposure(mCamList[i], false);
		setMCamAutoFramerate(mCamList[i], false);
		setMCamAutoJpegQuality(mCamList[i], false);
		setMCamAutoGain(mCamList[i], false);
		setMCamAutoSaturation(mCamList[i], false);
		setMCamAutoShutter(mCamList[i], false);
		setMCamAutoContrast(mCamList[i], false);
		setMCamAutoSharpening(mCamList[i], false);
		setMCamAutoDeNoise(mCamList[i], false);
		//setMCamAutoFocus(mCamList[i], false);

		res[i]["Exposure"].rc = setMCamExposure(mCamList[i], res[i]["Exposure"].exp);
		res[i]["FocusRelative"].rc = setMCamFocusRelative(mCamList[i], res[i]["FocusRelative"].exp);
		res[i]["Framerate"].rc = setMCamFramerate(mCamList[i], res[i]["Framerate"].exp);
		res[i]["JpegQuality"].rc = setMCamJpegQuality(mCamList[i], res[i]["JpegQuality"].exp);
		res[i]["Gain"].rc = setMCamGain(mCamList[i], res[i]["Gain"].exp);
		res[i]["Saturation"].rc = setMCamSaturation(mCamList[i], res[i]["Saturation"].exp);
		res[i]["Shutter"].rc = setMCamShutter(mCamList[i], res[i]["Shutter"].exp);
		res[i]["Contrast"].rc = setMCamContrast(mCamList[i], res[i]["Contrast"].exp);
		res[i]["Sharpening"].rc = setMCamSharpening(mCamList[i], res[i]["Sharpening"].exp);
		res[i]["DeNoise"].rc = setMCamDeNoise(mCamList[i], res[i]["DeNoise"].exp);
		res[i]["CParameters"].rc = setMCamCompressionParameters(mCamList[i], cp);
		res[i]["WBMode"].rc = setMCamWhiteBalanceMode(mCamList[i], res[i]["WBMode"].exp);
		res[i]["SensorMode"].rc = setMCamSensorMode(mCamList[i], res[i]["SensorMode"].exp);
		res[i]["IrFilter"].rc = setMCamIrFilter(mCamList[i], (bool)res[i]["IrFilter"].exp);
		res[i]["FocalLength"].rc = setMCamFocalLength(mCamList[i], res[i]["FocalLength"].exp);

		sleep(2);

		res[i]["Exposure"].act = getMCamExposure(mCamList[i]);
		res[i]["FocusRelative"].act = getMCamFocus(mCamList[i]);
		res[i]["FocusState"].act = getMCamFocusState(mCamList[i]);
		res[i]["Framerate"].act = getMCamFramerate(mCamList[i]);
		res[i]["JpegQuality"].act = getMCamJpegQuality(mCamList[i]);
		res[i]["Gain"].act = getMCamGain(mCamList[i]);
		res[i]["Saturation"].act = getMCamSaturation(mCamList[i]);
		res[i]["Shutter"].act = getMCamShutter(mCamList[i]);
		res[i]["Contrast"].act = getMCamContrast (mCamList[i]);
		res[i]["Sharpening"].act = getMCamSharpening(mCamList[i]);
		res[i]["DeNoise"].act = getMCamDeNoise(mCamList[i]);
		res[i]["CParameters"].act = getMCamCompressionParameters(mCamList[i]).qp_iframe;
		res[i]["WBMode"].act = getMCamWhiteBalanceMode(mCamList[i]);
		res[i]["ModuleID"].act = getMCamModuleID(mCamList[i]);
		res[i]["IrFilter"].act = getMCamIrFilter(mCamList[i]);
		res[i]["FocalLength"].act = getMCamFocalLength(mCamList[i]);
		res[i]["SensorID"].act = getMCamSensorID(mCamList[i]);
		res[i]["PixelSize"].act = getMCamPixelSize(mCamList[i]);

		setMCamWhiteBalanceMode(mCamList[i], 0);
		res[i]["WB_red"].rc = setMCamWhiteBalance(mCamList[i], {res[i]["WB_red"].exp, 1.0, 2.0});
		res[i]["FocusDefault"].rc = setMCamFocusDefault(mCamList[i]);
		res[i]["FocusAbsolute"].rc = setMCamFocusAbsolute(mCamList[i], res[i]["FocusAbsolute"].exp);

		sleep(2);

		res[i]["WB_red"].act = getMCamWhiteBalance(mCamList[i]).red;
		res[i]["FocusAbsolute"].act = getMCamFocus(mCamList[i]);
		//res["AvailableAnalytics"].act = getMCamAvailableAnalytics(mCamList[i]);
		//res["NumberAvailableAnalytics"].act = getMCamNumberAvailableAnalytics(mCamList[i]);
		//res["CurrentAnalytic"].act = getMCamCurrentAnalytic(mCamList[i]);
	}

	for (int i = 0; i <res.size(); i++) {
		cout << "mcamID: " << mCamList[i].mcamID << endl;
		cout << "\t\t" << "exp\t" << "act\t" << "rc\t" << "cb" << endl;
		map<string, result>::iterator it = res[i].begin();
		while (it != res[i].end())
		{
			cout << setprecision(3)
				 << it->first << "\t"
				 << (it->first.length() < 8 ? "\t" : "")
				 << it->second.exp << "\t"
				 << it->second.act << "\t"
				 << it->second.rc << "\t"
				 << it->second.cb << "\t"
				 << ((it->second.rc == 1) ? (abs(it->second.act - it->second.exp) < 0.01 ? "pass" : "fail" ) : "n/a")
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
