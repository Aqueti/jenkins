import subprocess
from abc import ABCMeta, abstractmethod
import time


class Environment:
    def run(self):
        self.render.restart()
        self.cam.restart()

    def __init__(self, **args):
        self.render = Render(args["render_ip"])
        self.cam = Camera(args["cam_ip"])


class Component(object):
    __metaclass__ = metaclass=ABCMeta

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def restart(self):
        self.stop()
        self.start()

    @abstractmethod
    def get_status(self):
        pass

    def get_ssh_str(self, ip, cmd, uname="nvidia"):
        return "ssh " + uname + "@" + ip + " '" + cmd + "'"

    def exec(self, cmd):
        #result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(cmd)
        return

        if result.stdout.decode('utf-8') != "":
            return result.stdout.decode('utf-8')
        else:
            return result.stderr.decode('utf-8')


class Camera(Component):
    def get_ip_list(self, **kwargs):
        ip_list = []
        if len(kwargs) == 0:
            for ip_end in range(1, self.num_of_tegras + 1):
                ip_list.append(self.start_ip + str(ip_end))
        else:
            keys = [k for k in kwargs.keys() if "tegra" in k]
            for ip_end in kwargs[keys[0]]:
                if ip_end > 0 and ip_end <= self.num_of_tegras:
                    ip_list.append(self.start_ip + str(ip_end))

        return ip_list

    def start(self, **kwargs):
        for ip in self.get_ip_list(**kwargs):
            cmd = self.get_ssh_str(ip, "sudo service Aqueti-Daemon start")
            self.exec(cmd)

    def stop(self, **kwargs):
        for ip in self.get_ip_list(**kwargs):
            cmd = self.get_ssh_str(ip, "sudo service Aqueti-Daemon stop")
            self.exec(cmd)

    def restart(self, **kwargs):
        for ip in self.get_ip_list(**kwargs):
            cmd = self.get_ssh_str(ip, "sudo service Aqueti-Daemon restart")
            self.exec(cmd)

    def get_status(self, ip):
        cmd = self.get_ssh_str(ip, "sudo service Aqueti-Daemon status | grep Active")
        self.exec(cmd)

    def copy_remote_file(self, **kwargs):
        for ip in self.get_ip_list(**kwargs):
            if "to_tegra" in kwargs:
                cmd = "cat " + kwargs["path_from"] + " | " + self.get_ssh_str(ip, 'sudo sh -c "cat >' + kwargs["path_to"] + '"')
                self.exec(cmd)
            elif "from_tegra" in kwargs:
                cmd = "scp nvidia@" + ip + ":" + kwargs["path_from"] + " " + kwargs["path_to"]
                return self.exec(cmd)

    def __init__(self, cam_ip):
        self.num_of_tegras = int(cam_ip[cam_ip.rfind('.') + 1:])
        self.start_ip = cam_ip[:cam_ip.rfind('.') + 1]


class Render(Component):
    def start(self):
        cmd = self.get_ssh_str(self.render_ip, "sh -c 'AquetiDaemonProcess &'", "mosaic")
        return self.exec(cmd)

    def stop(self):
        cmd = self.get_ssh_str(self.render_ip, "sh -c 'sudo pkill -2 AquetiDaemon'", "mosaic")
        return self.exec(cmd)

    def restart(self):
        self.stop()
        while self.get_status() == '':
            time.sleep(0.25)
        self.start()

    def get_status(self):
        cmd = self.get_ssh_str(self.render_ip, "sh -c 'pgrep AquetiDaemon'", "mosaic")
        return self.exec(cmd)

    def __init__(self, render_ip):
        self.render_ip = render_ip
