# !/usr/bin/python3

import subprocess
import re
import os
import sys
import time
import platform
import queue
import shutil
import unittest

from ipaddress import ip_network


class TestNWEnv(unittest.TestCase):
    server = []
    tegras = []

    hosts = tegras + server

    @staticmethod
    def exec_cmd(cmd):
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PI
PE)

        return result.stdout.decode('utf-8') + result.stderr.decode('utf-8')

    @staticmethod
    def exec_cmd_async(cmd):
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=Tr
ue)

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

    def test_4(self):
        """hosts are in the same subnet"""
        subnets = set([ip_network(ip+"/23", strict=False).network_address for ip in self.host
s])

        self.assertTrue(len(subnets) == 1, msg="Some hosts are not in the same subnet")      

    def test_5(self):
        """opened server ports"""
        ports = set((22, 5353))

        for ip in self.server:
            cmd = "sudo nmap -sUT -p{} -O {}".format(",".join(map(str, ports)), ip)
            rt = self.exec_cmd(cmd)

            rs = [re.search(r"{}/(tcp|udp)\s+open".format(port), rt) for port in ports]      

            self.assertTrue(all(rs), msg="Some hosts ports are not opened")

    #@unittest.skip
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

            rs = [re.search(r"{}/(tcp|udp)\s+open".format(port), rt.decode("utf-8")) for port
 in ports]

            self.assertTrue(all(rs), msg="Some hosts ports are not opened")

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
            
    # OS is correct
    def test_110(self):
        uname = platform.uname()
        rs = uname.system == 'Linux' and uname.machine == 'x86_64' and re.findall('16?8?\.04\.\d+-Ubuntu', uname.version)

        self.assertTrue(rs, msg="OS is not Ubuntu 16.04/18.04")

    # free disk space
    def test_111(self):
        du = shutil.disk_usage("/")
        rs = (du.free / du.total) > 0.05
        
        self.assertTrue(rs, msg="Available disk space is less than 5%")

    # GPU is supported
    def test_112(self):
        cmd = "nvidia-smi -L"
        rt = self.exec_cmd(cmd)
        rs = re.findall('GTX 10\d0', rt)
        
        self.assertTrue(rs, msg="GPU is not in the supported GPU's list. Forced compatibility is required")

    # Proper GPU driver is installed
    def test_113(self):
        cmd = "dpkg -l | grep -i 'NVIDIA binary driver'"
        rt = self.exec_cmd(cmd)
        rs = re.findall('nvidia-4[6-9][05]', rt)
        
        self.assertTrue(rs, msg="It is recommended to install nvidia driver >=460")

    # OpenGL is ok
    def test_114(self):
        cmd = "glxinfo | grep 'server glx vendor'"
        rt = self.exec_cmd(cmd)
        rs = re.findall('NVIDIA', rt)
                
        self.assertTrue(rs, msg="There is issue on OpenGL side, check glew")

    # Render is ok
    def test_115(self):
        cmd = "Fovea_Rendering_Speed_test -iterations 1 -windows 0"
        rt = self.exec_cmd(cmd)
        rs = not re.findall('core dumped', rt)
        
        self.assertTrue(not rs, msg="There is issue on render side, check lightdm config")

    # Limits are correct
    def test_116(self):
        cmd = "ulimit -n"
        rt = self.exec_cmd(cmd)
        rs = rt.strip() == "64000"
        
        self.assertTrue(rs, msg="Open files limit should be 64k, check /etc/security/limits.conf")

    # rmem_max is set
    def test_117(self):
        cmd = "sudo sysctl -p"
        rt = self.exec_cmd(cmd)
        text = 'net.core.rmem_max = 26214400\nnet.core.rmem_default = 26214400'
        rs = text in rt
        
        self.assertTrue(rs, msg="rmem_max=26214400, video will be jerky if not set, check /etc/sysctl.conf")

    # Aqueti software is installed
    def test_118(self):
        cmd = "dpkg -l | grep -i aqueti | awk \'{print$2}\'"
        rt = self.exec_cmd(cmd)
        aqt_apps = {'aquetiapi', 'aqueticalibrationtools', 'aquetidaemon-application', 'aquetidaemon-daemon', 'asis'}
        rs =  aqt_apps & set(rt.split())
        rs = len(rs) == len(aqt_apps)
        
        self.assertTrue(rs, msg="Some software is not installed")

    # Aqueti software dependencies are installed
    def test_119(self):
        cmd = "dpkg -l | grep -iE '(mongodb-org-server|docker-ce|hugin|ntp|lightdm)'"
        rt = self.exec_cmd(cmd)
        aqt_apps = {'mongodb-org-server', 'docker-ce', 'hugin', 'ntp', 'lightdm'}
        rs =  aqt_apps & set(rt.split())
        rs = len(rs) == len(aqt_apps)
        
        self.assertTrue(rs, msg="Some dependencies are not installed")

    # Daemon config is ok
    def test_120(self):
        fpath = '/etc/aqueti/daemonConfiguration.json'
        
        with open(fpath, 'r') as f:
            dconfig = json.load(f)

        keys = {'directoryOfServices', 'globalDatabase', 'localDatabase', 'resource', 'submodule'}

        rs = keys & set(dconfig.keys())
        rs = len(rs) == len(keys)
        
        self.assertTrue(rs, msg="Daemon config has issues")

    # System name is set
    def test_121(self):
        fpath = '/etc/aqueti/daemonConfiguration.json'
        
        with open(fpath, 'r') as f:
            dconfig = json.load(f)

        rs = dconfig['directoryOfServices']['system'] not in ('', 'Aqueti')
        
        self.assertTrue(rs, msg="System name is not set")

    # Lightdm is running
    def test_121_1(self):
        cmd = 'sudo service lightdm status | grep Active'
        rt = self.exec_cmd(cmd)
        rs = 'running' in rt
        
        self.assertTrue(rs, msg="lightdm service is not running")

    # Mongod is running
    def test_122(self):        
        cmd = 'sudo service mongod status | grep Active'
        rt = self.exec_cmd(cmd)
        rs = 'running' in rt
        
        self.assertTrue(rs, msg="mongod service is not running")

    # ADP is running
    def test_123(self):        
        cmd = 'sudo service Aqueti-Daemon status | grep Active'
        rt = self.exec_cmd(cmd)
        rs = 'running' in rt
        
        self.assertTrue(rs, msg="Aqueti-Daemon service is not running")

    # ASIS is running
    def test_124(self):        
        cmd = 'sudo service asisd status | grep Active'
        rt = self.exec_cmd(cmd)
        rs = 'running' in rt
        
        self.assertTrue(rs, msg="asisd service is not running")

    # All ASIS containers are running
    def test_125(self):        
        cmd = 'sudo docker ps -a | grep asis | grep Up | wc -l'
        rt = self.exec_cmd(cmd)
        rs = '7' in rt
        
        self.assertTrue(rs, msg="Some/All ASIS containers are not running")

    # Avahi-daemon is available on port 5353
    def test_126(self):
        cmd = 'sudo lsof -i :5353'
        rt = self.exec_cmd(cmd)
        rs = 'avahi-dae' in rt

        self.assertTrue(rs, msg="Avahi is not available")
        
    # Firewall is disabled
    def test_127(self):
        cmd = 'sudo ufw status'
        rt = self.exec_cmd(cmd)
        rs = 'inactive' in rt

        self.assertTrue(rs, msg="Firewall is running. Make sure it's set up properly or disable it")
    
    # ntp is running
    def test_128(self):
        cmd = 'sudo service asisd status | grep Active'
        rt = self.exec_cmd(cmd)
        rs = 'running' in rt
        
        self.assertTrue(rs, msg="ntp service is not running")

    # ntp config is ok
    def test_129(self):
        cmd = 'cat /etc/ntp.conf | grep -v "#" | grep broadcast | wc -l'
        rt = self.exec_cmd(cmd)
        rs = ('2' == rt)

        self.assertTrue(rs, msg="There is an issue with ntp.conf")

    # ntp server is configured
    def test_130(self):
        cmd = 'ntpq -p'
        rt = self.exec_cmd(cmd)
        rs = 'remote' in rt

        self.assertTrue(rs, msg="ntp server is not configured")
    
    # API and daemon versions match
    def test_131(self):
        cmd = 'AquetiDaemonProcess --version | tail -1; AquetiAPIVersion | tail -1'
        rt = self.exec_cmd(cmd)
        rs = rt[0] == rt[-1]

        self.assertTrue(rs, msg="API and daemon versions mismatch")


if __name__ == '__main__':
    print("Config checker", end="\n")

    if platform.system() == 'Linux':
        unittest.main(verbosity=2)
