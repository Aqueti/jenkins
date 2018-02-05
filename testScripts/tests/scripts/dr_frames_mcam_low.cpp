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

  res.push_back({exp_num_of_frames, act_num_of_frames, num_of_mis_frames, num_of_dr_frames});

  if (res[cam_id].size() >= (times - 1)) isCompleted = true;    
}

void newMCamCallback(MICRO_CAMERA mcam, void* data)
{
  static int i = 0;
  MICRO_CAMERA* mcamList = (MICRO_CAMERA*) data;
  mcamList[i++] = mcam;
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
  Env::setUp("frames_mcam_low");

  mCamConnect(mcam_ip, port);

  int num_of_mcams = getNumberOfMCams();

  MICRO_CAMERA mCamList[num_of_mcams];
  NEW_MICRO_CAMERA_CALLBACK mcamCB;
  mcamCB.f = newMCamCallback;
  mcamCB.data = &mCamList;
  setNewMCamCallback(mcamCB);

  MICRO_CAMERA_FRAME_CALLBACK frameCB;
  frameCB.f = frameCallback;

  setMCamFrameCallback(frameCB);

  for (int i = 0; i < num_of_mcams; i++) {
    initMCamFrameReceiver(r_port + i, 1.0);
    startMCamStream(mCamList[i], r_port + i);
    sleep(1);
  }

  while (!isCompleted) sleep(1);
 
  for (int i = 0; i < num_of_mcams; i++) {
    stopMCamStream(mCamList[i], r_port + i);
    closeMCamFrameReceiver(r_port + i);
    sleep(1);
  }

  mCamDisconnect(mcam_ip, port);

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