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

map<uint32_t, vector<FRAME> > frames;

struct Result {
	uint32_t exp_num_of_frames;
	uint32_t act_num_of_frames;
	uint32_t num_of_mis_frames;
	uint32_t num_of_dr_frames;
};

map<uint16_t, vector<Result> > res;

void add_res(int cam_id) {
  isPushing = false;

  int act_framerate = 30;

  long int delta = 1e6/30 + 5e3;

  long int time = getTime();

  int w_time = frames[cam_id].back().m_metadata.m_timestamp - frames[cam_id].front().m_metadata.m_timestamp;
  int exp_num_of_frames = ceil((w_time/1e6) * act_framerate) + 1;
  int act_num_of_frames = frames[cam_id].size();
  int num_of_mis_frames = exp_num_of_frames - act_num_of_frames;
  num_of_mis_frames = num_of_mis_frames > 0 ? num_of_mis_frames : 0;

  long int c_ts = 0;
  int num_of_dr_frames = 0; 
  for (int i = 0; i < frames[cam_id].size() - 1; i++) {
    c_ts = frames[cam_id][i].m_metadata.m_timestamp - frames[cam_id][i].m_metadata.m_timestamp; c_ts *= -1;

      if (c_ts > delta) num_of_dr_frames++;
  }

  frames[cam_id].clear();

  isPushing = true;

  res[cam_id].push_back({exp_num_of_frames, act_num_of_frames, num_of_mis_frames, num_of_dr_frames});

	if (res[cam_id].size() >= times) isCompleted = true;    
}

void newCameraCallback(ACOS_CAMERA mcam, void* data)
{
    ACOS_CAMERA* _mcam = (ACOS_CAMERA*) data;
    *_mcam = mcam;
}

void frameCallback(FRAME frame, void* data)
{
  if (isPushing) {
    frames[frame.m_metadata.m_camId].push_back(frame);

    if (frames[frame.m_metadata.m_camId].size() == 4000) add_res(frame.m_metadata.m_camId);
  }
}

int main(int argc, char * argv[])
{
  Env::setUp("frames_mcam_high");

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

  FRAME_CALLBACK cb;
  cb.f = frameCallback;

  ACOS_STREAM streams[cam.mcamList.numMCams];

  for (int i = 0; i < cam.mcamList.numMCams; i++) {
     std::cout << i << ' ';
     streams[i] = createMCamStream(cam, cam.mcamList.mcams[i]);
     initStreamReceiver(cb, streams[i], r_port + i, 2.0);
     sleep(1);
  }

  while (!isCompleted) sleep(1);
 
  for (int i = 0; i < cam.mcamList.numMCams; i++) {
      deleteStream(streams[i]);
      closeStreamReceiver(r_port + i);
      sleep(1);
  }

  setCameraConnection(cam, false, 10);

  disconnectFromCameraServer();

  cout << "\texp\t" << "act\t" << "mis\t" << "dr\t" << endl; 
  for (int i = 0; i < times; i++) {
	  for (map<uint16_t, vector<Result> >::iterator it = res.begin(); it != res.end(); it++) {
		cout << it->first << "\t"
			 << it->second[i].exp_num_of_frames << "\t"
			 << it->second[i].act_num_of_frames << "\t"
			 << it->second[i].num_of_mis_frames << "\t"
			 << it->second[i].num_of_dr_frames << "\t"
			 << (it->second[i].num_of_mis_frames <= 1 ? "pass" : "fail")
			 << endl;
		if (act_res) act_res = (it->second[i].num_of_mis_frames <= 1);
	  }
	  cout << endl; 
  }

  Env::tearDown();

  return 0;
}
