#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/time.h>
#include <map>
#include <list>
#include <iterator>
#include <cmath>
#include <string>
#include <sstream>
#include <vector>
#include <iostream>
#include <fstream>
#include "sqlite3.h"

#include "mantis/MantisAPI.h"

using namespace std;

char mcam_ip[24] = "127.0.0.1";
int port = 9999;
int r_port = 14000;
int duration = 67*8*1000; //67

map<uint32_t, string> cp;
map<uint32_t, list<FRAME> > frames;
char *file_name = "/home/astepenko/scripts/dropped_frames_v2.txt";
char *db_name = "/home/astepenko/scripts/test_res.db";
char *conn_type = "V2";

int requestCallback(void *data, int argc, char **argv, char **azColName){
   fprintf(stderr, "%s: ", (const char*)data);

   for(int i = 0; i < argc; i++){
      cout << azColName[i] << ": " << (argv[i] ? argv[i] : "NULL") << endl;
   }

   return 0;
}

int execQuery(string sql, char *db_name) {
      sqlite3 *db;
      char *zErrMsg = 0;
      int rc = 0;

      const char* data = "data";

      rc = sqlite3_open(db_name, &db);

      if( rc ) {
         return rc;
      }

      rc = sqlite3_exec(db, strdup(sql.c_str()), requestCallback, (void*)data, &zErrMsg);

      if( rc != SQLITE_OK ) {
        fprintf(stderr, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
      }

      sqlite3_close(db);

      return rc;
}

long int getTime() {
  struct timeval tp;
  gettimeofday(&tp, NULL);
  long int ms = tp.tv_sec * 1000 + tp.tv_usec / 1000;

  return ms;
}

string exec(string cmd) {
    FILE *popen_result;
    char buff[128];
    popen_result = popen(cmd.c_str(), "r");

    ostringstream ss;
    if (popen_result) {
        while (fgets(buff, sizeof(buff), popen_result) != NULL) {
            ss << buff;
        }
        pclose(popen_result);
    }

    return ss.str();
}

vector<string> split(const std::string &text, char sep) {
    vector<std::string> tokens;
    size_t start = 0, end = 0;
    while ((end = text.find(sep, start)) != string::npos) {
        tokens.push_back(text.substr(start, end - start));
        start = end + 1;
    }
    tokens.push_back(text.substr(start));
    return tokens;
}

string getUsage(string type, string val) {
  string output;
  if (type == "cpu") { 
    output = exec("ps -C " + val + " -o %cpu | tail -1");
  } else if (type == "mem") {
    output = exec("ps -C " + val + " -o %mem | tail -1");
  } else if (type == "disk") {
    output = exec("df -m " + val + " | tail -1 | awk '{print $5}'");
  } else {

  } 

  return output;
}

void write_result(int cam_id) {
    ostringstream ss;

    int act_framerate = 30;

    long int delta = 1e6/30 + 5e2;

    long int time = getTime();    

    int w_time = frames[cam_id].back().m_metadata.m_timestamp - frames[cam_id].front().m_metadata.m_timestamp;
    int exp_num_of_frames = ceil((w_time/1e6) * act_framerate);
    int act_num_of_frames = frames[cam_id].size();
    cout << "act_num_of_frames: " << act_num_of_frames << endl;
    int num_of_mis_frames = exp_num_of_frames - act_num_of_frames;    
    num_of_mis_frames = num_of_mis_frames > 0 ? num_of_mis_frames : 0;

    long int c_ts = 0;
    int d_frames = 0;
    list<FRAME>::iterator it = frames[cam_id].begin();
    for (int i = 0; i < frames[cam_id].size() - 1; i++) {
      c_ts = it->m_metadata.m_timestamp - (++it)->m_metadata.m_timestamp; c_ts *= -1;

        if (c_ts > delta) {    
            d_frames++;
        }
    }    

    ostringstream sqlss;
    sqlss   << "INSERT INTO dropped_frames_v2('time', 'cam_id', 'exp_num', 'act_num', 'mis_num', 'dr_num', 'cpu', 'mem', 'disk', 'conn_type', 'encoding') VALUES("
			<< time << ", "
			<< cam_id << ", "
			<< exp_num_of_frames << ", "
			<< act_num_of_frames << ", "
			<< num_of_mis_frames << ", "
			<< d_frames << ", "
      << '"' << getUsage("cpu", "V2") << '"' << ", "
      << '"' << getUsage("mem", "V2") << '"' << ", "
      << '"' << getUsage("disk", "/dev/sda1") << '"' << ", "
      << '"' << conn_type << '"' << ", "
      << '"' << cp[cam_id] << '"' << ");";

    //cout << sqlss.str() << endl;

    execQuery(sqlss.str(), db_name);
}

void newCameraCallback(ACOS_CAMERA mcam, void* data)
{
    ACOS_CAMERA* _mcam = (ACOS_CAMERA*) data;
    *_mcam = mcam;
}

void frameCallback(FRAME frame, void* data)
{    
    frames[frame.m_metadata.m_camId].push_back(frame);

    //std::cout << frame.m_metadata.m_camId << ": " << frames[frame.m_metadata.m_camId].size() << '\n';

    if (frames[frame.m_metadata.m_camId].size() == 4000) {
        write_result(frame.m_metadata.m_camId);
        frames[frame.m_metadata.m_camId].clear();
    }
}

int main(int argc, char * argv[])
{
  ACOS_CAMERA cam;
  NEW_CAMERA_CALLBACK camCB;
  camCB.f = newCameraCallback;
  camCB.data = &cam;
  setNewCameraCallback(camCB);

  connectToCameraServer(mcam_ip, port);

  if(isCameraConnected(cam) != 110) {
      setCameraConnection(cam, true, 5);
  }

  fillCameraMCamList(&cam);

  AtlCompressionParameters t_cp;
  for (int i = 0; i < cam.mcamList.numMCams; i++) {
    t_cp = getMCamCompressionParameters(cam.mcamList.mcams[i]);

    uint32_t id = cam.mcamList.mcams[i].mcamID;
    if (t_cp.type == 1) {
      cp[id] = "JPEG";
    } else if (t_cp.type == 2) {
      cp[id] = "H264";
    } else if (t_cp.type == 3) {
      cp[id] = "H265";
    } else {
      cp[id] = "Unknown";
    }
  }

  FRAME_CALLBACK cb;
  cb.f = frameCallback;
  cb.data = &frames;

  ACOS_STREAM streams[cam.mcamList.numMCams];

  for (int i = 0; i < cam.mcamList.numMCams; i++) {
     std::cout << i << ' ';
     streams[i] = createMCamStream(cam, cam.mcamList.mcams[i]);
     initStreamReceiver(cb, streams[i], r_port + i, 2.0);
     sleep(1);
  }

  sleep(duration);

  for (int i = 0; i < cam.mcamList.numMCams; i++) {     
      deleteStream(streams[i]);
      closeStreamReceiver(r_port + i);
      sleep(1);
  }

  setCameraConnection(cam, false, 10);

  disconnectFromCameraServer();

  return 0;
}
