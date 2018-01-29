#include "tests.h" 

char *v2_ip = "127.0.0.1"; 
char *mcam_ip = "192.168.10.1";
uint16_t port = 9999;
uint16_t r_port = 13000;
char *file_name = "/home/astepenko/test_res.txt";
char *tbl_name = "test_res";
char *db_name = "/home/astepenko/test_res.db";
string script_name = "na";
bool act_res = true;

char *enc = V2_ENCODE_H264;
string camID = "21";
string cam_folder = "/etc/aqueti/mantis_" + camID;
string storage_path = "/etc/aqueti/mantis_21";
string file_path = cam_folder + "/" + "hostfile";

VIDEO_SOURCE videoSource = {
  1920, //width
  1080  //height
};
VIDEO_ENCODER videoEncoder = {
  1920, //width
  1080, //height
  4,    //quality
  10,   //sessionTimeout
  30,   //framerate
  50,   //encodingInterval
  2048, //bitrateLimit
  V2_ENCODE_H264  //encoding    
};

STREAM_PROFILE profile = {  
  videoSource,
  videoEncoder
};  

/*
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
*/

string readFromFile(const char* file_name) {
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
};

void writeToFile(string str, char* file_name, bool w_method) {
  ofstream fout;

  if (w_method) {
    fout.open(file_name, ios::out | ios::app);
  }
  else {
    fout.open(file_name, ios::out);
  }

  fout << str;
  fout.close();
}

bool fileExists( const string &file_name )
{
  return access( file_name.c_str(), 0 ) == 0;
}

string exec(string cmd) {
  FILE *popen_result;
  char buff[512];
  popen_result = popen(cmd.c_str(), "r");

  ostringstream ss;

	if (popen_result) {
		while (fgets(buff, sizeof(buff), popen_result) != NULL) {
			ss << buff;
		}
	}

  pclose(popen_result);

  return ss.str();
};

vector<string> split(const string &text, char sep) {
  vector<string> tokens;
  size_t start = 0, end = 0;
  while ((end = text.find(sep, start)) != string::npos) {
    tokens.push_back(text.substr(start, end - start));
    start = end + 1;
  }
  tokens.push_back(text.substr(start));
  return tokens;
};

string getSSHStr(string ip, string cmd) {
  return "ssh ubuntu@" + ip + " '" + cmd + "'";
}

int* allocmem(int len) {
  int *buffer = (int*) malloc(len);
  if (buffer != NULL) {
    for (int i = 1; i < len; i++) {
      buffer[i] = 1;
    }
  }
  //free(buffer);

  return buffer;
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

double get_disk_usage(string drive_name) {
	string avail = exec("df -m " + drive_name + " | tail -1 | awk '{print$4}'");
	string used = exec("df -m " + drive_name + " | tail -1 | awk '{print$3}'");

	return ((double)atoi(used.c_str()) / (double)(atoi(avail.c_str()) + atoi(used.c_str()))) * 100;
}

long int getTime() {
  struct timeval tp;
  gettimeofday(&tp, NULL);
  long int ms = tp.tv_sec * 1000 + tp.tv_usec / 1000;

  return ms;
}

double getRnd(PAIR_DOUBLE pd) {
  double value = (pd.second - pd.first) * ( (double)rand() / (double)RAND_MAX ) + pd.first;
  return roundf(value * 100) / 100;
}

int getRnd(AtlRange_32f pd) {
  double value = (pd.max - pd.min) * ( (double)rand() / (double)RAND_MAX ) + pd.min;
  return round(value);
}

int getRnd(AtlRange_64f pd) {
  double value = (pd.max - pd.min) * ( (double)rand() / (double)RAND_MAX ) + pd.min;
  return round(value);
}



void tegra::reboot(string ip) {
  string cmd = getSSHStr(ip, "sudo reboot");
  exec(cmd);
}
void tegra::waitForRepsonse(string ip) {
  string cmd;
  do {
    cmd = getSSHStr(ip, "pgrep systemd | head -1");
    sleep(1);
  } while (exec(cmd) == "");
}

void acosd::start(string ip, string mode, bool p) {
  string cmd = getSSHStr(ip, "pkill -9 acosd; acosd -R acosdLog -C " + mode + " -s 1");
  if (p) {
    string t_cmd = getSSHStr(ip, "ssh ubuntu@192.168.10.1 'ps aux | grep acosd' | head -1 | awk '{print$15}'");
    if (exec(t_cmd) != mode) {
      exec(cmd);
    }
  } else {
    exec(cmd);
  }
  sleep(1);
} 
void acosd::stop(string ip) {
  string cmd = getSSHStr(ip, "pkill -9 acosd");
  exec(cmd);
  sleep(1);
}
void acosd::restart(string ip, string mode) {
  acosd::stop(ip);
  acosd::start(ip, mode);
}

void V2::start(string camID, string storage_path) {
  string cmd = "V2 --cache-size 20000 --maxRecordingLength 3600 --tightPrefetch --force-gpu-compatibility -p 24816 --numJpegDecompressors 16 --numH26XDecompressors 5 --prefetchSize 40 --dir " + storage_path + " --camera " + camID + " 1>/dev/null &";
  exec(cmd);
  sleep(2);
}
void V2::stop() {
  string cmd = "pkill -9 V2";
  exec(cmd);
  sleep(1);
}
void V2::restart(string camID, string storage_path) {
  V2::stop();
  V2::start(camID, storage_path);
}
void V2::restart() {
  V2::stop();
  V2::start(camID, storage_path);
}

void Env::setUp(string sname, bool isV2started) {
  script_name = sname;

  if (false) {
    vector<string> a_ip = split(readFromFile(file_path.c_str()), '\n');

    for (int i = 0; i < a_ip.size() - 1; i++) {
      acosd::restart(a_ip[i], enc);
    }

    if (isV2started) {
      V2::restart(split(cam_folder, '_')[1], storage_path);
    } else {
      V2::stop();
    }
  }
}
void Env::tearDown(bool isDB) {
  ostringstream fss;
  fss << script_name << "\t" << (act_res ? "pass" : "fail") << endl;
  writeToFile(fss.str(), file_name);
  cout << "\n" << fss.str();

  if (isDB) {
    ostringstream sqlss;
    sqlss << "UPDATE " << tbl_name << " SET result='" << (act_res ? "pass" : "fail") << "' WHERE script_name='" << script_name << "';";

    //execQuery(sqlss.str(), db_name);
  }
}
