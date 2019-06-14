import json
import subprocess
import sys
import json
import pymongo
import time
import datetime as dt


UPDATE_INTERVAL = 300  #seconds
SCRIPT_PATH = "get_info.py"

class DB:
    server_ip = "10.0.0.176"
    port = "27017"
    db_name = "qa"
    col_name = "sysinfo"

    def __init__(self):
        self.mc = pymongo.MongoClient("mongodb://" + self.server_ip + ":" + self.port)

    def store(self, doc):
        q_doc = doc.copy()
        try:
            del q_doc["timestamp"]
            del q_doc["daemon"]["uptime"]
            del q_doc["daemon"]["status"]
            del q_doc["asis"]["uptime"]
            del q_doc["asis"]["status"]
        except:
            pass

        self.mc[self.db_name]["sysinfo"].replace_one(q_doc, doc, upsert=True)

    def get_ip(self, arch):
        rs = self.mc[self.db_name]["nodes"].find({"arch": arch})
        if arch == "aarch64":
            return [(row["ip"] + "." + str(row["tegras_num"])) for row in rs]
        else:
            return [row["ip"] for row in rs]

def get_username(ip):
    subnet = "10.1."
    tegras = [2, 4, 7, 9, 11, 12, 77, 149]

    ip_arr = [subnet + str(id) for id in tegras]

    if ip[:ip.rindex('.')] in ip_arr:
        return "nvidia"

    if ip in ("10.1.1.177", "10.1.1.232"):
        return "aqueti"
    elif ip in ("10.1.1.204"):
        return "jenkins"
    else:
        return "mosaic"


def exec_cmd(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return result.stdout.decode('utf-8')


def get_ssh(cmd, ip):
    return "ssh " + get_username(ip) + "@" + ip + " '" + cmd + "'"


def is_available(ip):
    cmd = "ping -c 1 -W 1 " + ip
    rs = exec_cmd(cmd)

    if "1 received" in rs:
        return True
    else:
        return False

def copy_to(ip):
    cmd = "scp " + SCRIPT_PATH + " " + get_username(ip)  + "@" + ip + ":./"
    exec_cmd(cmd)

def get_info(ip):
    copy_to(ip)

    cmd = "python3 " + SCRIPT_PATH
    res = exec_cmd(get_ssh(cmd, ip))

    return res


db = DB()

while True:
    s_time = dt.datetime.now()

    print(s_time, ": gathering info")

    servers = db.get_ip("x86_64")
    cameras = db.get_ip("aarch64")

    for ip in servers:
        if not is_available(ip):
            continue
        doc = json.loads(get_info(ip))
        db.store(doc)

    for cam in cameras:
        cam_ip = cam[:cam.rindex(".") + 1]
        v_ip = int(cam[cam.rindex(".") + 1:])

        for ip in [cam_ip + str(i) for i in range(1, v_ip + 1)]:
            if not is_available(ip):
                continue
            doc = json.loads(get_info(ip))
            db.store(doc)

    e_time = dt.datetime.now()
    delta = e_time - s_time
    if delta.seconds < UPDATE_INTERVAL:
        time.sleep(UPDATE_INTERVAL - delta.seconds)
