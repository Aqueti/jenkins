#ifndef TESTS_H
#define TESTS_H

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
#include <iomanip>
#include <sys/time.h>
#include <map>
#include <list>
#include <vector>
#include <iterator>
#include <cmath>
#include <string>
#include <cstring>
#include <sstream>
#include <iostream>
#include <fstream>
//#include "sqlite3.h"

#include "mantis/MantisAPI.h"

using namespace std;

extern char *v2_ip; 
extern char *mcam_ip;
extern uint16_t port;
extern uint16_t r_port;
extern char *file_name;
extern char *tbl_name;
extern char *db_name;
extern string script_name;
extern bool act_res;

extern char *enc;
extern string camID;
extern string cam_folder;
extern string storage_path;
extern string file_path;

extern VIDEO_SOURCE videoSource;
extern VIDEO_ENCODER videoEncoder;
extern STREAM_PROFILE profile;

/*
int requestCallback(void *data, int argc, char **argv, char **azColName);

int execQuery(string sql, char *db_name);
*/

string readFromFile(const char* file_name);

void writeToFile(string str, char* file_name, bool w_method = true);

bool fileExists( const string &file_name );

string exec(string cmd);

vector<string> split(const string &text, char sep);

string getSSHStr(string ip, string cmd);

int* allocmem(int len);

string getUsage(string type, string val);

double get_disk_usage(string drive_name);

long int getTime();

double getRnd(PAIR_DOUBLE pd);

int getRnd(AtlRange_32f pd);

int getRnd(AtlRange_64f pd);

class tegra {
public:
  static void reboot(string ip);
  static void waitForRepsonse(string ip);
};

class acosd {
public:
  static void start(string ip, string mode = "JPEG", bool p = true);
  static void stop(string ip);
  static void restart(string ip, string mode = "JPEG");
};

class V2 {
public:
  static void start(string camID, string storage_path);
  static void stop();
  static void restart(string camID, string storage_path);
  static void restart();
};

class Env {
public:
  static void setUp(string sname, bool isV2started = false);
  static void tearDown(bool isDB = false);
};

#endif