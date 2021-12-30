# !/usr/bin/python3

import subprocess
import re
import os
import grp
import pwd
import sys
import time
import json
import platform
import queue
import shutil
import unittest
import pymongo
import base64
import paramiko
import numpy as np

from pathlib import Path
from ipaddress import ip_network


class TestNWEnv(unittest.TestCase):
    server = ['10.1.1.204']
    tegras = ['10.1.7.{}'.format(i+1) for i in range(10)]

    hosts = tegras + server

    @staticmethod
    def exec_cmd(cmd):
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return result.stdout.decode('utf-8') + result.stderr.decode('utf-8')

    @staticmethod
    def exec_cmd_async(cmd):
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        return proc

    def __init__(self, *args, **kwargs):
        super(TestNWEnv, self).__init__(*args, **kwargs)

    def get_ips(self):
        cmd = "ip addr | grep -o --regexp='[0-9]\{1,3\}[\.][0-9]\{1,3\}[\.][0-9]\{1,3\}[\.][0-9]\{1,3\}\/[1-3]\?[0-9]'"
        rt = self.exec_cmd(cmd)
        if rt:
            return rt.split()

    def test_11(self):
        """state of host tcp/ip stack"""
        cmd = "sudo sysctl -p"
        rt = self.exec_cmd(cmd)

        self.assertTrue(rt)

    def test_1(self):
        """state of host tcp/ip stack"""
        cmd = "ping 127.0.0.1 -c 1 -W 1 | grep '1 received'"
        rt = self.exec_cmd(cmd)

        self.assertTrue(rt)

   
    def test_2(self):
        """/etc/hosts file content"""
        cmd = "cat /etc/hosts | grep $(hostname).local"
        rt = self.exec_cmd(cmd)

        self.assertTrue(rt, msg="hostname.local should be in /etc/hosts")

    def test_3(self):
        """hosts reach"""
        que = queue.Queue()
        for ip in self.hosts:
            cmd = "ping {} -c 1 -W 1 | grep '1 received'".format(ip, ip)
            que.put(self.exec_cmd_async(cmd))

        while not que.empty():
            e = que.get()
            if e.poll() is None:
                que.put(e)
                continue
            rt, _ = e.communicate()

            self.assertTrue(rt.decode("utf-8").strip(), msg="Some hosts are not reachable")  

    @unittest.skip
    def test_4(self):
        """hosts are in the same subnet"""
        subnets = set([ip_network(ip+"/23", strict=False).network_address for ip in self.hosts])

        self.assertTrue(len(subnets) == 1, msg="Some hosts are not in the same subnet")      

    @unittest.skip
    def test_5(self):
        """opened server ports"""
        ports = set((22, 5353))

        for ip in self.server:
            cmd = "sudo nmap -sUT -p{} -O {}".format(",".join(map(str, ports)), ip)
            rt = self.exec_cmd(cmd)

            rs = [re.search(r"{}/(tcp|udp)\s+open".format(port), rt) for port in ports]      

            self.assertTrue(all(rs), msg="Some hosts ports are not opened")

    @unittest.skip
    def test_6(self):
        """opened tergas ports"""
        ports = set((22, 5353))

        que = queue.Queue()
        for ip in self.tegras:
            cmd = "sudo nmap -sUT -p{} -O {}".format(",".join(map(str, ports)), ip)
            que.put(self.exec_cmd_async(cmd))

        while not que.empty():
            e = que.get()
            if e.poll() is None:
                que.put(e)
                continue
            rt, _ = e.communicate()

            rs = [re.search(r"{}/(tcp|udp)\s+open".format(port), rt.decode("utf-8")) for port in ports]

            self.assertTrue(all(rs), msg="Some hosts ports are not opened")

    @unittest.skip
    def test_7(self):
        """multicast traffic is not filtered"""
        # iperf -s -u -B 224.0.0.22 -i 1
        # iperf -c 224.0.0.22 -u -T 32 -t 1 -i 1
        cmd = "sleep 7; sudo pkill -9 tcpdump"
        pp = self.exec_cmd_async(cmd)

        cmd = "sudo tcpdump -i any udp port 5353 | grep '224.0.0.251'"
        p = self.exec_cmd_async(cmd)
        time.sleep(5)
        rt, _ = p.communicate()
        pp.communicate()

        rs = set(re.findall(r"[0-9]+(?:\.[0-9]+){3}", rt.decode("utf-8"))) & set(self.tegras)
        # print("\nfound: ", rs)

        self.assertTrue(rs, msg="Multicast traffic is being filtered")

    @unittest.skip
    def test_8(self):
        """name resolution on server"""

        que = queue.Queue()
        for ip in self.tegras:
            cmd = "avahi-resolve-address {}".format(ip)
            que.put(self.exec_cmd_async(cmd))

        while not que.empty():
            e = que.get()
            if e.poll() is None:
                que.put(e)
                continue
            rt, _ = e.communicate()

            rs = rt.decode("utf-8")

            self.assertTrue(rs, msg="Some tegras ip's cannot be resolved to hostnames")      

    @unittest.skip
    def test_9(self):
        """name resolution on tegras"""
        # keys should be copied first
        que = queue.Queue()
        for ip in self.tegras:
            cmd = "ssh nvidia@{} 'avahi-resolve-address {}'".format(ip, self.server[0])      
            que.put(self.exec_cmd_async(cmd))

        while not que.empty():
            e = que.get()
            if e.poll() is None:
                que.put(e)
                continue
            rt, _ = e.communicate()

            rs = rt.decode("utf-8")

            self.assertTrue(rs, msg="Some tegras cannot resolve server ip to hostname")


class TestServerConfig(unittest.TestCase):
    daemon_config = None

    @staticmethod
    def exec_cmd(cmd):
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return result.stdout.decode('utf-8') + result.stderr.decode('utf-8')

    def __init__(self, *args, **kwargs):
        super(TestServerConfig, self).__init__(*args, **kwargs)

        with open('/etc/aqueti/daemonConfiguration.json', 'r') as f:
            self.daemon_config = json.load(f)

    def test_110(self):
        """
        OS is correct
        """

        uname = platform.uname()
        rs = uname.system == 'Linux' and uname.machine == 'x86_64' and re.findall('16?8?\.04\.\d+-Ubuntu', uname.version)

        self.assertTrue(rs, msg="OS is not Ubuntu 16.04/18.04")

    def test_111(self):
        """
        there is free disk space
        """

        du = shutil.disk_usage("/")
        rs = (du.free / du.total) > 0.05
        
        self.assertTrue(rs, msg="Available disk space is less than 5%")

    def test_112(self):
        """
        GPU is supported
        """

        cmd = "nvidia-smi -L"
        rt = self.exec_cmd(cmd)
        rs = re.findall('GTX 10\d0', rt)
        
        self.assertTrue(rs, msg="GPU is not in the supported GPU's list. Forced compatibility is required")

    def test_113(self):
        """
        Proper GPU driver is installed
        """

        cmd = "dpkg -l | grep -i 'NVIDIA binary driver'"
        rt = self.exec_cmd(cmd)
        rs = re.findall('nvidia-4[6-9][05]', rt)

        self.assertTrue(rs, msg="It is recommended to install nvidia driver >=460")

    def test_114(self):
        """
        OpenGL is ok
        """

        cmd = "glxinfo | grep 'server glx vendor'"
        rt = self.exec_cmd(cmd)
        rs = re.findall('NVIDIA', rt)
                
        self.assertTrue(rs, msg="There is issue on OpenGL side, check glew")

    def test_115(self):
        """
        Render is ok
        """

        cmd = "Fovea_Rendering_Speed_test -iterations 1 -windows 0"
        rt = self.exec_cmd(cmd)
        rs = not re.findall('core dumped', rt)
        
        self.assertTrue(not rs, msg="There is issue on render side, check lightdm config")

    def test_116(self):
        """
        Limits are correct
        """
        cmd = "ulimit -n"
        rt = self.exec_cmd(cmd)
        rs = rt.strip() == "64000"
        
        self.assertTrue(rs, msg="Open files limit should be 64k, check /etc/security/limits.conf")

    def test_117(self):
        """
        rmem_max is set
        """

        cmd = "sudo sysctl -p"
        rt = self.exec_cmd(cmd)
        text = 'net.core.rmem_max = 26214400\nnet.core.rmem_default = 26214400'
        rs = text in rt
        
        self.assertTrue(rs, msg="rmem_max=26214400, video will be jerky if not set, check /etc/sysctl.conf")

    def test_118(self):
        """
        Aqueti software is installed
        """

        cmd = "dpkg -l | grep -i aqueti | awk \'{print$2}\'"
        rt = self.exec_cmd(cmd)
        aqt_apps = {'aquetiapi', 'aqueticalibrationtools', 'aquetidaemon-application', 'aquetidaemon-daemon', 'asis'}
        rs =  aqt_apps & set(rt.split())
        rs = len(rs) == len(aqt_apps)
        
        self.assertTrue(rs, msg="Some software is not installed")

    def test_119(self):
        """
        Aqueti software dependencies are installed
        """

        cmd = "dpkg -l | grep -iE '(mongodb-org-server|docker-ce|hugin|ntp|lightdm)'"
        rt = self.exec_cmd(cmd)
        aqt_apps = {'mongodb-org-server', 'docker-ce', 'hugin', 'ntp', 'lightdm'}
        rs =  aqt_apps & set(rt.split())
        rs = len(rs) == len(aqt_apps)
        
        self.assertTrue(rs, msg="Some dependencies are not installed")

    def test_120(self):
        """
        Daemon config is ok
        """

        keys = {'directoryOfServices', 'globalDatabase', 'localDatabase', 'resource', 'submodule'}

        rs = keys & set(self.daemon_config.keys())
        rs = len(rs) == len(keys)
        
        self.assertTrue(rs, msg="Daemon config has issues")

    def test_1201(self):
        """
        Daemon config submodules
        """

        keys = {'Coeus', 'ModelHandler', 'Mnemosyne', 'Hyperion', 'Cronus', 'SCOPController', 'ImportExportControl'}

        rs = set([k['type'] for k in self.daemon_config['submodule']]) & set(self.daemon_config.keys())
        rs = len(rs) == len(keys)
        
        self.assertTrue(rs, msg="Missing submodule")

    def test_121(self):
        """
        System name is set
        """

        rs = self.daemon_config['directoryOfServices']['system'] not in ('', 'Aqueti')
        
        self.assertTrue(rs, msg="System name is not set")

    def test_1261(self):
        """
        Avahi-daemon is available on port 5353
        """

        cmd = 'sudo lsof -i :5353'
        rt = self.exec_cmd(cmd)
        rs = 'avahi-dae' in rt

        self.assertTrue(rs, msg="Avahi is not available")

    def test_1262(self):
        """
        Avahi name->ip resolution works
        """

        cmd = 'avahi-resolve-host-name $(hostname).local'
        rt = self.exec_cmd(cmd)
        rs = '172.16.' in rt

        self.assertTrue(rs, msg="There is an issue with avahi name resolution")

    def test_1263(self):
        """
        Avahi ip->name resolution works
        """

        cmd = 'avahi-resolve-address 127.0.0.1 | grep $(hostname).local'
        rt = self.exec_cmd(cmd)
        rs = len(rt) > 0

        self.assertTrue(rs, msg="There is an issue with avahi name resolution")

    def test_127(self):
        """
        Firewall is disabled
        """

        cmd = 'sudo ufw status'
        rt = self.exec_cmd(cmd)
        rs = 'inactive' in rt

        self.assertTrue(rs, msg="Firewall is running. Make sure it's set up properly or disable it")

    def test_128(self):
        """
        ntp is running
        """

        cmd = 'sudo service asisd status | grep Active'
        rt = self.exec_cmd(cmd)
        rs = 'running' in rt
        
        self.assertTrue(rs, msg="ntp service is not running")

    def test_129(self):
        """
        ntp config is ok
        """

        cmd = 'cat /etc/ntp.conf | grep -v "#" | grep broadcast | wc -l'
        rt = self.exec_cmd(cmd)
        rs = ('2' == rt)

        self.assertTrue(rs, msg="There is an issue with ntp.conf")

    def test_130(self):
        """
        ntp server is configured
        """

        cmd = 'ntpq -p'
        rt = self.exec_cmd(cmd)
        rs = 'remote' in rt

        self.assertTrue(rs, msg="ntp server is not configured")

    def test_131(self):
        """
        API and daemon versions match
        """

        cmd = 'AquetiDaemonProcess --version | tail -1; AquetiAPIVersion | tail -1'
        rt = self.exec_cmd(cmd)
        rs = rt[0] == rt[-1]

        self.assertTrue(rs, msg="API and daemon versions mismatch")

    def test_132(self):
        """
        Storage directory exists
        """

        ind = np.argmax(['storageDirs' in d for d in self.daemon_config['submodule']])
        spath = self.daemon_config['submodule'][ind]['storageDirs'][-1]

        rs = Path(spath).is_dir()
        
        self.assertTrue(rs, msg="Storage directory does not exist")

    def test_1321(self):
        """
        Storage directory permissions are ok
        """

        ind = np.argmax(['storageDirs' in d for d in self.daemon_config['submodule']])
        spath = self.daemon_config['submodule'][ind]['storageDirs'][-1]

        stat_info = os.stat(spath)
        uid, gid = stat_info.st_uid, stat_info.st_gid

        user, group = pwd.getpwuid(uid)[0], grp.getgrgid(gid)[0]
        rs = ('aqueti' == user) and ('aqueti' == group)
        
        self.assertTrue(rs, msg="There is an issue with storage directory permissions")

    def test_134(self):
        """
        AQT directories permissions are ok
        """

        folders = ['/etc/aqueti', '/var/tmp/aqueti', '/var/log/aqueti']

        for spath in folders:
            stat_info = os.stat(spath)
            uid, gid = stat_info.st_uid, stat_info.st_gid

            user, group = pwd.getpwuid(uid)[0], grp.getgrgid(gid)[0]
            rs = ('aqueti' == user) and ('aqueti' == group)
            
            self.assertTrue(rs, msg="There is an issue with storage directory permissions")

    def test_121_1(self):
        """
        Lightdm is running
        """

        cmd = 'sudo service lightdm status | grep Active'
        rt = self.exec_cmd(cmd)
        rs = 'running' in rt
        
        self.assertTrue(rs, msg="lightdm service is not running")

    def test_122(self):
        """
        Mongod is running
        """

        cmd = 'sudo service mongod status | grep Active'
        rt = self.exec_cmd(cmd)
        rs = 'running' in rt
        
        self.assertTrue(rs, msg="mongod service is not running")

    def test_1221(self):
        """
        mongodb: acos database exists
        """

        db_name = self.daemon_config["globalDatabase"]["name"]

        mc = pymongo.MongoClient("mongodb://127.0.0.1:27017")
        db_names = mc.list_database_names()
        rs = db_name in db_names        
        
        self.assertTrue(rs, msg="acos db does not exist")

    def test_1222(self):
        """
        mongodb: asis database exists
        """

        mc = pymongo.MongoClient("mongodb://127.0.0.1:27017")
        db_names = mc.list_database_names()
        rs = 'asis' in db_names        
        
        self.assertTrue(rs, msg="asis db does not exist")

    def test_1223(self):
        """
        mongodb: models collection is not empty
        """

        db_name = self.daemon_config["globalDatabase"]["name"]

        mc = pymongo.MongoClient("mongodb://127.0.0.1:27017")
        models_num = mc[db_name]['models'].count()
        rs = models_num > 0
        
        self.assertTrue(rs, msg="models collection is empty")

    def test_123(self): 
        """
        ADP is running
        """

        cmd = 'sudo service Aqueti-Daemon status | grep Active'
        rt = self.exec_cmd(cmd)
        rs = 'running' in rt
        
        self.assertTrue(rs, msg="Aqueti-Daemon service is not running")

    def test_124(self):
        """
        ASIS is running
        """

        cmd = 'sudo service asisd status | grep Active'
        rt = self.exec_cmd(cmd)
        rs = 'running' in rt
        
        self.assertTrue(rs, msg="asisd service is not running")

    def test_125(self):      
        """
        All ASIS containers are running
        """
         
        cmd = 'sudo docker ps -a | grep asis | grep Up | wc -l'
        rt = self.exec_cmd(cmd)
        rs = '7' in rt
        
        self.assertTrue(rs, msg="Some/All ASIS containers are not running")
    
    def test_1251(self):      
        """
        worker log_level is correct
        """
         
        cmd = 'cat /etc/asis/config/worker/config.py | grep -v '#' | grep LOG_LEVEL'
        rt = self.exec_cmd(cmd)
        rs = 'WARNING' in rt
        
        self.assertTrue(rs, msg="worker LOG_LEVEL is incorrect")

    def test_1252(self):      
        """
        asis log_level is correct
        """
         
        cmd = 'cat /etc/asis/config/asis/config.py | grep -v '#' | grep LOG_LEVEL'
        rt = self.exec_cmd(cmd)
        rs = 'WARNING' in rt
        
        self.assertTrue(rs, msg="asis LOG_LEVEL is incorrect")
        

class TestTegraConfig(unittest.TestCase):
    daemon_config = None

    tegra_ips = ["10.1.7.{}".format(i+1) for i in range(10)]
    ssh_clients = {tegra_ip: None for tegra_ip in tegra_ips}

    @staticmethod
    def exec_cmd(cmd):
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return result.stdout.decode('utf-8') + result.stderr.decode('utf-8')

    def __init__(self, *args, **kwargs):
        super(TestTegraConfig, self).__init__(*args, **kwargs)

        for tegra_ip in self.tegra_ips:
            print(tegra_ip)
            self.ssh_clients[tegra_ip] = paramiko.SSHClient()
            self.ssh_clients[tegra_ip].set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_clients[tegra_ip].connect(tegra_ip, username='nvidia', password='nvidia')

    def exec_cmd_on_tegras(self, cmd, ip=None):        
        # stdin, stdout, stderr = self.client.exec_command(cmd)

        if ip:
            tegra_ips = [ip]
        else:
            tegra_ips = self.tegra_ips

        out = {}
        for tegra_ip in tegra_ips:
            stdin, stdout, stderr = self.ssh_clients[tegra_ip].exec_command(cmd)
            out[tegra_ip] = "".join(list(stdout.readlines()))

        return out

    def assertTrue_on_tegras(self, cmd, func, msg, ip=None):        
        # stdin, stdout, stderr = self.client.exec_command(cmd)

        out = self.exec_cmd_on_tegras(cmd, ip)
        for tegra_ip, stdout in out.items():
            self.assertTrue(func(stdout), msg="{}: {}".format(tegra_ip, msg))
    
    def test_100(self):
        """
        Aqueti software is installed
        """

        cmd = "dpkg -l | grep -i aqueti | awk '{print$2}'"
        func = lambda s: set(s[:-1].split("\n")) == {'aqueti-kernel-updater', 'aqueti-tegra-config', 'aquetidaemon'}

        self.assertTrue_on_tegras(cmd, func, "Aqueti software is not installed")

    def test_101(self):
        """
        Tegra daemon config is ok
        """

        cmd = "python -m json.tool /etc/aqueti/daemonConfiguration.json"
        func = lambda s: set(json.loads(s).keys()) == {'directoryOfServices', 'globalDatabase', 'localDatabase', 'resource', 'submodule'}

        self.assertTrue_on_tegras(cmd, func, "There is an issue with tegra config")


    def test_102(self):
        """
        Compression is correct
        """

        cmd = "python -m json.tool /etc/aqueti/daemonConfiguration.json"
        func = lambda s: json.loads(s)["submodule"][0]["compression"] in {'JPEG', 'H264', 'H265'}

        self.assertTrue_on_tegras(cmd, func, "There is an issue with compression type")

    def test_103(self):
        """
        System name is not empty
        """

        cmd = "python -m json.tool /etc/aqueti/daemonConfiguration.json"
        func = lambda s: json.loads(s)["directoryOfServices"]["system"] != ""

        self.assertTrue_on_tegras(cmd, func, "There is an issue with system name")
    
    def test_1041(self):
        """
        ip v4 is on
        """

        cmd = "cat /etc/avahi/avahi-daemon.conf | grep -v '#' | grep 'use-ipv4'"
        func = lambda s: 'yes' in s

        self.assertTrue_on_tegras(cmd, func, "ip v6 is enabled on tegra")
        
    def test_1042(self):
        """
        ip v6 is off
        """

        cmd = "cat /etc/avahi/avahi-daemon.conf | grep -v '#' | grep 'use-ipv6'"
        func = lambda s: 'no' in s

        self.assertTrue_on_tegras(cmd, func, "ip v6 is enabled on tegra")

    def test_1052(self):
        """
        ntp is configured
        """

        cmd = "cat /etc/ntp.conf | grep -v '#'"
        func = lambda s: 'broadcastclient' in s

        self.assertTrue_on_tegras(cmd, func, "ntp is not configured")

    @unittest.skip("")
    def test_1053(self):
        """
        ntp is ok
        """

        cmd = "ntpq -p"
        func = lambda s: 'remote' in s

        self.assertTrue_on_tegras(cmd, func, "There is an issue with ntp config")

    def test_106(self):
        """
        sensors are connected
        """

        cmd = "sudo i2cdetect -y -r 30 | tail -2"
        func = lambda s: '60' in s

        self.assertTrue_on_tegras(cmd, func, "There is an issue with sensors")

        cmd = "sudo i2cdetect -y -r 31 | tail -2"
        func = lambda s: '40' not in s

        self.assertTrue_on_tegras(cmd, func, "There is an issue with sensors")

    def test_1071(self):
        """
        Factory model is copied to tegra config
        """

        cmd = "python -m json.tool /etc/aqueti/config.json | grep Slot | wc -l"
        func = lambda s: int(s) > 12 

        self.assertTrue_on_tegras(cmd, func, "Factory model is not copied to tegra config")

    def test_1072(self):
        """
        XX is not doubled in tegra config
        """

        cmd = "python -m json.tool /etc/aqueti/config.json"
        func = lambda s: 'XXXX' not in s

        self.assertTrue_on_tegras(cmd, func, "There is doubled XX in /etc/aqueti/config.json")

    def test_108(self):
        """
        There is available space on /dev/root
        """

        cmd = "df -h / | awk '{print$5}'"
        func = lambda s: '100' not in s

        self.assertTrue_on_tegras(cmd, func, "There is no available space on /dev/root")

    def test_109(self):
        """
        there is available space on /var/log
        """

        cmd = "df -h /var/log | awk '{print$5}'"
        func = lambda s: '100' not in s

        self.assertTrue_on_tegras(cmd, func, "There is no available space on /var/log")

    def test_110(self):
        """
        There are no sensors faults
        """

        cmd = "cat /etc/aqueti/state.json | grep sensor_faults"
        func = lambda s: '0' in s

        self.assertTrue_on_tegras(cmd, func, "There are sensors faults")

    def test_111(self):
        """
        ADP is running
        """

        cmd = "sudo service Aqueti-Daemon status | grep Active"
        func = lambda s: 'running' in s

        self.assertTrue_on_tegras(cmd, func, "ADP is running")

    def test_112(self):
        """
        Data connection with server daemon is established
        """

        cmd = "sudo netstat -np | grep acosd | grep -v unix | wc -l"
        func = lambda s: int(s) >= 20

        self.assertTrue_on_tegras(cmd, func, "Data connection with server daemon is not established")

    def test_113(self):
        """
        avahi-free: /etc/hosts
        """

        server_hostname = ""
        cmd = "cat /etc/hosts"
        func = lambda s: '{}.local'.format(server_hostname) in s

        self.assertTrue_on_tegras(cmd, func, "avahi free: hosts file does not contain server hostname")

    def test_114(self):
        """
        avahi-free: /etc/aqueti/daemonConfiguration.json
        """

        cmd = "cat /etc/aqueti/daemonConfiguration.json"
        func = lambda s: 'serverPort' in s

        self.assertTrue_on_tegras(cmd, func, "avahi-free: tegra daemon config does not contain server port")

    # add tests for ONVIF server config

if __name__ == '__main__':
    print("Config checker", end="\n")

    if platform.system() == 'Linux':
        unittest.main(verbosity=2)

