#ifndef TESTS_H
#define TESTS_H

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
#include <sys/time.h>
#include <map>
#include <list>
#include <iterator>
#include <cmath>
#include <string>
#include <cstring>
#include <sstream>
#include <vector>
#include <iostream>
#include <fstream>
#include "sqlite3.h"

#include "mantis/MantisAPI.h"

using namespace std;

namespace td {
  char *v2_ip = "127.0.0.1";
  char *mcam_ip = "192.168.10.5";
  uint16_t port = 9999;
  uint16_t r_port = 13000;
  char *tbl_name = "test_results";
  char *db_name = "/home/astepenko/scripts/test_res.db";
  char *file_name = "/home/astepenko/scripts/test_results.txt";

  char *enc = V2_ENCODE_H264;
  string storage_path = "/etc/aqueti/mantis_85";
  string cam_folder = "/etc/aqueti/mantis_85 ";
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
};

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
    vector<std::string> tokens;
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

struct tegra {
  static void restart(string ip) {
    string cmd = getSSHStr(ip, "sudo reboot");
    exec(cmd);
  }
  static void waitForRepsonse(string ip) {
    string cmd = getSSHStr(ip, "pgrep systemd | head -1");
    while (exec(cmd) == "") {
      sleep(1);
    }
  }
};

struct acosd {
  static void start(string ip, string mode = "JPEG", bool p = true) {
    string cmd = getSSHStr(ip, "pkill -9 acosd; acosd -R acosdLog -C " + mode + " -s 1");
    if (p) {
      string t_cmd = getSSHStr(ip, "ps aux | grep acosd | head -1");
      if (exec(t_cmd + " | awk '{print$15}'") != mode) {
        exec(cmd);
      }
    } else {
      exec(cmd);
    }
    sleep(1);
  }
  static void stop(string ip) {
    string cmd = getSSHStr(ip, "pkill -9 acosd");
    exec(cmd);
    sleep(1);
  }
  static void restart(string ip, string mode = "JPEG") {
    acosd::stop(ip);
    acosd::start(ip, mode);
  }
};

struct V2 {
  static void start(string camID, string storage_path) {
    string cmd = "V2 --numJpegDecompressors 2 --numH26XDecompressors 2 --prefetchSize 40 --force-gpu-compatibility --dir " + storage_path + " --camera " + camID + " 1>/dev/null &";
    exec(cmd);
    sleep(2);
  }
  static void stop() {
    string cmd = "pkill -9 V2";
    exec(cmd);
    sleep(1);
  }
  static void restart(string camID, string storage_path) {
    V2::stop();
    V2::start(camID, storage_path);
  }
};

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

void writeToFile(string str, char* file_name, bool w_method = true) {
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

long int getTime() {
  struct timeval tp;
  gettimeofday(&tp, NULL);
  long int ms = tp.tv_sec * 1000 + tp.tv_usec / 1000;

  return ms;
}

void write_res(bool act_res, char *script_name) {
  ostringstream sqlss;
  sqlss << "UPDATE " << td::tbl_name << " SET result='" << (act_res ? "pass" : "fail") << "' WHERE script_name='" << script_name << "';";

  execQuery(sqlss.str(), td::db_name);

  ostringstream filess;
  filess << script_name << ": " << act_res << endl;

  writeToFile(filess.str(), file_name);
}

void setupEnv(bool b = false) {
  vector<string> a_ip = split(readFromFile(td::file_path.c_str()), '\n');

  for (int i = 0; i < a_ip.size() - 1; i++) {
    acosd::restart(a_ip[i], td::enc);
  }

  if (b) {
    V2::restart(split(td::cam_folder, '_')[1], td::storage_path);
  } else {
    V2::stop();
  }
}

#endif