/**
* Checking:
* dropped frames number
*
**/

#include "tests.h"

using namespace td;

uint16_t times = 5;
bool isCompleted = false;
bool isPushing = true;

vector<FRAME> frames;

struct Result {
	uint32_t exp_num_of_frames;
	uint32_t act_num_of_frames;
	uint32_t num_of_mis_frames;
	uint32_t num_of_dr_frames;
};

vector<Result> res;

void add_res() {
  isPushing = false;

  int act_framerate = 30;

  long int delta = 1e6/30 + 5e3;

  long int time = getTime();

  int w_time = frames.back().m_metadata.m_timestamp - frames.front().m_metadata.m_timestamp;
  int exp_num_of_frames = ceil((w_time/1e6) * act_framerate) + 1;
  int act_num_of_frames = frames.size();
  int num_of_mis_frames = exp_num_of_frames - act_num_of_frames;
  num_of_mis_frames = num_of_mis_frames > 0 ? num_of_mis_frames : 0;

  long int c_ts = 0;
  int num_of_dr_frames = 0; 
  for (int i = 0; i < frames.size() - 1; i++) {
    c_ts = frames[i].m_metadata.m_timestamp - frames[i].m_metadata.m_timestamp; c_ts *= -1;

      if (c_ts > delta) num_of_dr_frames++;     
  }

  frames.clear();

  isPushing = true;

  res.push_back({exp_num_of_frames, act_num_of_frames, num_of_mis_frames, num_of_dr_frames});

  if (res.size() >= (times - 1)) isCompleted = true;
}

void newCameraCallback(ACOS_CAMERA mcam, void* data)
{
    ACOS_CAMERA* _mcam = (ACOS_CAMERA*) data;
    *_mcam = mcam;
}

void frameCallback(FRAME frame, void* data)
{
  if (isPushing) {
    frames.push_back(frame);

    if (frames.size() == 4000) add_res();
  }
}

int main(int argc, char * argv[])
{
  Env::setUp("dr_frames_v2");

  ACOS_CAMERA cam;
  NEW_CAMERA_CALLBACK camCB;
  camCB.f = newCameraCallback;
  camCB.data = &cam;
  setNewCameraCallback(camCB);

  connectToCameraServer(v2_ip, port);

  if(isCameraConnected(cam) != 110) {
      setCameraConnection(cam, true, 5);
  }

  fillCameraMCamList(&cam);

  FRAME_CALLBACK fcb;
  fcb.f = frameCallback;

  setCameraReceivingData(cam, true, 5);

  ACOS_STREAM stream = createLiveStream( cam, profile );
  initStreamReceiver( fcb, stream, r_port, 2.0 );
  setStreamGoLive( stream ); sleep(1);

  while(!isCompleted) sleep(1);

  closeStreamReceiver(r_port);
  deleteStream(stream);
 
  setCameraReceivingData(cam, false, 5);

  setCameraConnection(cam, false, 10);

  disconnectFromCameraServer();

  cout << "\texp\t" << "act\t" << "mis\t" << "dr\t" << endl; 
  for (int i = 0; i < res.size(); i++) {   
		cout << i << "\t"
         << res[i].exp_num_of_frames << "\t"
  			 << res[i].act_num_of_frames << "\t"
  			 << res[i].num_of_mis_frames << "\t"
  			 << res[i].num_of_dr_frames << "\t"
         << (res[i].num_of_mis_frames <= 1 ? "pass" : "fail")   
			   << endl;
    if (act_res) act_res = (res[i].num_of_mis_frames <= 1);
  }

  Env::tearDown();

  return 0;
}