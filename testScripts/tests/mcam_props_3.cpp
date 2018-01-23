/**
 * Checking:
 * properties are independent, if one is changed it shouldn't effect on others
 * 
 **/

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
	double exp;
	vector<bool> act;
	PAIR_DOUBLE range;
};

int main(int argc, char * argv[])
{
	Env::setUp("mcam_props_3");

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

		setMCamAutoExposure(mCamList[i], false);
		setMCamAutoFramerate(mCamList[i], false);
		setMCamAutoJpegQuality(mCamList[i], false);
		setMCamAutoGain(mCamList[i], false);
		setMCamAutoSaturation(mCamList[i], false);
		setMCamAutoShutter(mCamList[i], false);
		setMCamAutoContrast(mCamList[i], false);
		setMCamAutoSharpening(mCamList[i], false);
		setMCamAutoDeNoise(mCamList[i], false);

		res[i]["Exposure"].range = getMCamExposureRange(mCamList[i]);
		res[i]["Framerate"].range = getMCamFramerateRange(mCamList[i]);
		res[i]["JpegQuality"].range = getMCamJpegQualityRange(mCamList[i]);
		res[i]["Gain"].range = getMCamGainRange(mCamList[i]);
		res[i]["Saturation"].range = getMCamSaturationRange(mCamList[i]);
		res[i]["Shutter"].range = getMCamShutterRange(mCamList[i]);
		res[i]["Contrast"].range = getMCamContrastRange(mCamList[i]);
		res[i]["Sharpening"].range = getMCamSharpeningRange(mCamList[i]);
		res[i]["DeNoise"].range = getMCamDeNoiseRange(mCamList[i]);

		res[i]["JpegQuality"].range.first = 1;
		res[i]["Shutter"].range.first = 0.014999;
		res[i]["Exposure"].range.first = 0;

		cout << "mcamID " << mCamList[i].mcamID << endl;

		int num_of_steps = 2;
		map<string, result>::iterator it = res[i].begin();
		while (it != res[i].end()) {
			setMCamExposure(mCamList[i], res[i]["Exposure"].range.first);
			setMCamFramerate(mCamList[i], res[i]["Framerate"].range.first);
			setMCamJpegQuality(mCamList[i], res[i]["JpegQuality"].range.first);
			setMCamGain(mCamList[i], res[i]["Gain"].range.first);
			setMCamSaturation(mCamList[i], res[i]["Saturation"].range.first);
			setMCamShutter(mCamList[i], res[i]["Shutter"].range.first);
			setMCamContrast(mCamList[i], res[i]["Contrast"].range.first);
			setMCamSharpening(mCamList[i], res[i]["Sharpening"].range.first);
			setMCamDeNoise(mCamList[i], res[i]["DeNoise"].range.first);

			double step = it->second.range.first;
			while ((step - it->second.range.second) < 0.01) {
				if(it->first == "Exposure") {
					setMCamExposure(mCamList[i], step);
				}
				else if (it->first == "Framerate") {
					setMCamFramerate(mCamList[i], step);
				}
				else if (it->first == "JpegQuality") {
					setMCamJpegQuality(mCamList[i], round(step));
				}
				else if (it->first == "Gain") {
					setMCamGain(mCamList[i], step);
				}
				else if (it->first == "Saturation") {
					setMCamSaturation(mCamList[i], step);
				}
				else if (it->first == "Shutter") {
					setMCamShutter(mCamList[i], step);
				}
				else if (it->first == "Contrast") {
					setMCamContrast(mCamList[i], step);
				}
				else if (it->first == "Sharpening") {
					setMCamSharpening(mCamList[i], step);
				}
				else if (it->first == "DeNoise") {
					setMCamDeNoise(mCamList[i], step);
				} else {

				}

				sleep(2);

				res[i]["Exposure"].act.push_back(getMCamExposure(mCamList[i]) == res[i]["Exposure"].range.first);
				res[i]["Framerate"].act.push_back(getMCamFramerate(mCamList[i]) == res[i]["Framerate"].range.first);
				res[i]["JpegQuality"].act.push_back(getMCamJpegQuality(mCamList[i]) == res[i]["JpegQuality"].range.first);
				res[i]["Gain"].act.push_back(getMCamGain(mCamList[i]) == res[i]["Gain"].range.first);
				res[i]["Saturation"].act.push_back(getMCamSaturation(mCamList[i]) == res[i]["Saturation"].range.first);
				res[i]["Shutter"].act.push_back(getMCamShutter(mCamList[i]) == res[i]["Shutter"].range.first);
				res[i]["Contrast"].act.push_back(getMCamContrast(mCamList[i]) == res[i]["Contrast"].range.first);
				res[i]["Sharpening"].act.push_back(getMCamSharpening(mCamList[i]) == res[i]["Sharpening"].range.first);
				res[i]["DeNoise"].act.push_back(getMCamDeNoise(mCamList[i]) == res[i]["DeNoise"].range.first);

				res[i][it->first].act[res[i][it->first].act.size() - 1] = true;

				int last_index = res[i][it->first].act.size() - 1;
				cout << it->first << "\t"
					 << (it->first.length() < 8 ? "\t" : "")
					 << step << "\t"
					 << ((res[i]["Exposure"].act[last_index] && res[i]["Framerate"].act[last_index] && res[i]["JpegQuality"].act[last_index] && res[i]["Gain\t"].act[last_index] && res[i]["Saturation"].act[last_index] && res[i]["Shutter\t"].act[last_index] && res[i]["Contrast"].act[last_index] && res[i]["Sharpening"].act[last_index] && res[i]["DeNoise\t"].act[last_index]) ? "pass" : "fail")
					 << endl;

				if(act_res) act_res = (res[i]["Exposure"].act[last_index] && res[i]["Framerate"].act[last_index] && res[i]["JpegQuality"].act[last_index] && res[i]["Gain\t"].act[last_index] && res[i]["Saturation"].act[last_index] && res[i]["Shutter\t"].act[last_index] && res[i]["Contrast"].act[last_index] && res[i]["Sharpening"].act[last_index] && res[i]["DeNoise\t"].act[last_index]);

				step += (res[i][it->first].range.second - res[i][it->first].range.first) / num_of_steps;
			}

			it++;
		}
	}

    mCamDisconnect(mcam_ip, port);

    Env::tearDown();

    return 0;
}
