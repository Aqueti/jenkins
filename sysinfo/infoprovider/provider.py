import json
import subprocess
import sys
import json
import pymongo
import time
import datetime as dt
import copy

UPDATE_INTERVAL = 300  # seconds
SCRIPT_PATH = "get_info.py"


class DB:
    server_ip = "10.0.0.176"
    port = "27017"
    db_name = "qa"
    col_sysinfo = "sysinfo"

    def __init__(self):
        self.mc = pymongo.MongoClient("mongodb://" + self.server_ip + ":" + self.port)

    def query(self, col_name, query):
        rs = self.mc[self.db_name][col_name].find(query)

        return [row for row in rs]

    def to_mongo_query(self, d, mongo_d={}, p_key=None):
        for key in d.keys():
            if isinstance(d[key], dict):
                return self.to_mongo_query(d[key], mongo_d, key)

            if p_key is not None:
                k = p_key + "." + key
                mongo_d[k] = d[key]
            else:
                mongo_d[key] = d[key]

        return mongo_d

    def store(self, doc):
        q_doc = copy.deepcopy(doc)

        q_doc.pop("timestamp", None)
        q_doc["daemon"].pop("status", None)
        q_doc["daemon"].pop("uptime", None)

        if "asis" in q_doc.keys():
            q_doc["asis"].pop("status", None)
            q_doc["asis"].pop("uptime", None)

        self.mc[self.db_name][self.col_sysinfo].replace_one(self.to_mongo_query(q_doc), doc, upsert=True)

    def get_ip(self, arch):
        rs = self.mc[self.db_name]["nodes"].find({"arch": arch})
        if arch == "aarch64":
            return [(row["ip"] + "." + str(row["tegras_num"])) for row in rs]
        else:
            return [row["ip"] for row in rs]


class Nodes:
    ips = {}
    servers = []
    cameras = []

    def __init__(self):
        self.db = DB()

    def update(self):
        nodes = self.db.query("nodes", {})

        for node in nodes:
            if node["arch"] == "x86_64":
                self.servers.append(node["ip"])
            else:
                self.cameras.append(node["ip"] + '.' + str(node["tegras_num"]))

            # self.nodes.setdefault(node["arch"],[]).append(node["ip"])

        self.ips = {node["ip"]: node["user"] for node in nodes if node["arch"] == "x86_64"}


    def get_username(self, ip):
        if ip in self.ips.keys():
            return self.ips[ip]
        else:
            return "nvidia"


    def exec_cmd(self, cmd):
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return result.stdout.decode('utf-8')


    def is_online(self, ip):
        cmd = "ping -c 1 -W 1 " + ip
        rs = self.exec_cmd(cmd)

        if "1 received" in rs:
            cmd = "ssh " + self.get_username(ip) + "@" + ip + " -o 'BatchMode=yes' -o 'ConnectionAttempts=1' true"
            rs = self.exec_cmd(cmd)

            if rs == "":  #Permission denied
                return True

        return False


    def copy_to(self, ip):
        cmd = "scp " + SCRIPT_PATH + " " + self.get_username(ip) + "@" + ip + ":./"
        self.exec_cmd(cmd)


    def get_ssh(self, cmd, ip):
        return "ssh " + self.get_username(ip) + "@" + ip + " '" + cmd + "'"


    def get_info(self, ip):
        self.copy_to(ip)

        cmd = "python3 " + SCRIPT_PATH
        res = self.exec_cmd(self.get_ssh(cmd, ip))

        return res


nodes = Nodes()

while True:
    nodes.update()

    s_time = dt.datetime.now()

    print(s_time, ": gathering info")

    for ip in nodes.servers:
        if not nodes.is_online(ip):
            continue

        try:
            doc = json.loads(nodes.get_info(ip))
            nodes.db.store(doc)
        except:
            print("failed to get info from " + ip)

    for cam in nodes.cameras:
        cam_ip = cam[:cam.rindex(".") + 1]
        v_ip = int(cam[cam.rindex(".") + 1:])

        for ip in [cam_ip + str(i) for i in range(1, v_ip + 1)]:
            if not nodes.is_online(ip):
                continue

            try:
                doc = json.loads(nodes.get_info(ip))
                nodes.db.store(doc)
            except:
                print("failed to get info from " + ip)

    e_time = dt.datetime.now()
    delta = e_time - s_time
    if delta.seconds < UPDATE_INTERVAL:
        time.sleep(UPDATE_INTERVAL - delta.seconds)
