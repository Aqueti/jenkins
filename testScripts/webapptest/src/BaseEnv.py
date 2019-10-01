import subprocess
from abc import ABCMeta, abstractmethod


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

    status = {0: "inactive", 1: "active", 2: "unknown"}

    def is_active(self, cmd):
        if cmd is not None:
            if "failed (Result: exit-code)" in cmd:
                return self.status[0]
            elif "active (running)" in cmd:
                return self.status[1]
            else:
                return self.status[2]

    def get_ssh_str(self, ip, cmd, uname="nvidia"):
        return "ssh " + uname + "@" + ip + " '" + cmd + "'"

    def exec_cmd(self, cmd):
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return result.stdout.decode('utf-8') + result.stderr.decode('utf-8')


class Camera(Component):
    def get_ip_list(self, **kwargs):
        ip_list = []
        if "tegra" not in kwargs:
            for ip_end in range(1, self.num_of_tegras + 1):
                ip_list.append(self.start_ip + str(ip_end))
        else:
            keys = [k for k in kwargs.keys() if "tegra" in k]
            for ip_end in kwargs[keys[0]]:
                if ip_end > 0 and ip_end <= self.num_of_tegras:
                    ip_list.append(self.start_ip + str(ip_end))

        return ip_list

    def start(self, **kwargs):
        if "tegra" in kwargs:
            ip_list = [kwargs['tegra']]
        else:
            ip_list = self.get_ip_list(**kwargs)

        for ip in ip_list:
            cmd = self.get_ssh_str(ip, "sudo service Aqueti-Daemon start")
            self.exec_cmd(cmd)

    def stop(self, **kwargs):
        if "tegra" in kwargs:
            ip_list = [kwargs['tegra']]
        else:
            ip_list = self.get_ip_list(**kwargs)

        for ip in ip_list:
            cmd = self.get_ssh_str(ip, "sudo service Aqueti-Daemon stop")
            self.exec_cmd(cmd)

    def restart(self, **kwargs):
        if "tegra" in kwargs:
            ip_list = [kwargs['tegra']]
        else:
            ip_list = self.get_ip_list(**kwargs)

        for ip in ip_list:
            cmd = self.get_ssh_str(ip, "sudo service Aqueti-Daemon restart")
            self.exec_cmd(cmd)

    def reboot(self, **kwargs):
        if "tegra" in kwargs:
            ip_list = [kwargs['tegra']]
        else:
            ip_list = self.get_ip_list(**kwargs)

        for ip in ip_list:
            cmd = self.get_ssh_str(ip, "sudo reboot")
            self.exec_cmd(cmd)

    def get_status(self, **kwargs):
        if "tegra" in kwargs:
            ip_list = [self.start_ip + str(kwargs['tegra'])]
        else:
            ip_list = self.get_ip_list(**kwargs)

        st = []
        for ip in ip_list:
            cmd = self.get_ssh_str(ip, "sudo service Aqueti-Daemon status | grep Active")
            rs = self.exec_cmd(cmd)

            st.append(self.is_active(rs))

        for key in self.status:
            if False not in [self.status[key] == si for si in st]:
                return self.status[key]

        return self.status[2]

    def copy_remote_file(self, **kwargs):
        if "tegra" in kwargs:
            if "to_tegra" in kwargs:
                #cmd = "cat " + kwargs["path_from"] + " | " + self.get_ssh_str(ip, 'sudo sh -c "cat >' + kwargs["path_to"] + '"')
                cmd = "scp " + kwargs["path_from"] + " nvidia@" + kwargs['tegra'] + ":./; " + self.get_ssh_str(kwargs['tegra'], "sudo cp " + kwargs["path_from"][kwargs["path_from"].rfind("/") + 1:] + " " + kwargs["path_to"])
                self.exec_cmd(cmd)
            elif "from_tegra" in kwargs:
                cmd = "scp nvidia@" + kwargs['tegra'] + ":" + kwargs["path_from"] + " " + kwargs["path_to"]
                self.exec_cmd(cmd)

    def read(self, **kwargs):
        if "tegra" in kwargs:
            cmd = self.get_ssh_str(kwargs['tegra'], "cat " + kwargs["f_name"])
            return self.exec_cmd(cmd)

    def exec_cmd(self, **kwargs):
        if "tegra" in kwargs:
            ip_list = [self.start_ip + str(kwargs['tegra'])]
        else:
            ip_list = self.get_ip_list(**kwargs)

        st = []
        for ip in ip_list:
            cmd = self.get_ssh_str(ip, kwargs['cmd'])
            st.append(super(Camera, self).exec_cmd(cmd))

        return st


    def __init__(self, cam_ip):
        self.num_of_tegras = int(cam_ip[cam_ip.rfind('.') + 1:])
        self.start_ip = cam_ip[:cam_ip.rfind('.') + 1]
        self.ip = self.get_ip_list()


class Render(Component):
    def start(self):
        cmd = "sh -c 'sudo service Aqueti-Daemon start'"
        return self.exec_cmd(cmd)

    def stop(self):
        cmd = "sh -c 'sudo service Aqueti-Daemon stop'"
        return self.exec_cmd(cmd)

    def restart(self):
        cmd = "sh -c 'sudo service Aqueti-Daemon restart'"
        return self.exec_cmd(cmd)

    def get_status(self):
        cmd = "sh -c 'sudo service Aqueti-Daemon status | grep Active'"
        rs = self.exec_cmd(cmd)

        return self.is_active(rs)

    def __init__(self, ip):
        self.ip = ip


