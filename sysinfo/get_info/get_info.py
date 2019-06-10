import subprocess
import time
import json

class Info:
    json = {}

    def __init__(self):
        self.update()

    def update(self):
        self.json["ip"] = self.get("ip")
        self.json["sys_name"] = self.get("config", "system")
        self.json["arch"] = self.get("arch")
        self.json["timestamp"] = int(time.time() * 1000)

        if self.json["arch"] == "x86_64":
            self.json["daemon"] = {}
            self.json["api"] = {}
            self.json["ctools"] = {}
            self.json["asis"] = {}

            self.json["daemon"]["app_version"] = self.get("app_version")
            self.json["daemon"]["d_version"] = self.get("version", "aquetidaemon-daemon")
            self.json["daemon"]["status"] = self.get("status", "Aqueti-Daemon")
            self.json["daemon"]["uptime"] = self.get("uptime", "Aqueti-Daemon")

            self.json["api"]["version"] = self.get("version", "aquetiapi")
            self.json["ctools"]["version"] = self.get("version", "aqueticalibrationtools")

            self.json["asis"]["version"] = self.get("version", "asis")
            self.json["asis"]["status"] = self.get("status", "asisd")
            self.json["asis"]["uptime"] = self.get("uptime", "asisd")
        elif self.json["arch"] == "aarch64":
            self.json["daemon"] = {}
            self.json["aci"] = {}

            self.json["daemon"]["app_version"] = self.get("app_version")
            self.json["daemon"]["status"] = self.get("status", "Aqueti-Daemon")
            self.json["daemon"]["uptime"] = self.get("uptime", "Aqueti-Daemon")

            self.json["aci"]["version"] = self.get("version", "aci")
            self.json["aci"]["compression"] = self.get("config", "compression")
        else:
            pass


    def exec_cmd(self, cmd):
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return result.stdout.decode('utf-8')

    def get(self, entity, obj_name = ""):
        archs = ["x86_64", "aarch64"]

        if entity == "arch":
            cmd = "uname -a"

            arch_rs = self.exec_cmd(cmd)
            for arch in archs:
                if arch in arch_rs:
                    return arch

        elif entity == "ip":
            subnet = "10.1"
            cmd = "ifconfig | grep 'inet addr:" + subnet + "'"

            var_rs = self.exec_cmd(cmd)
            if var_rs != "":
                t = var_rs.split()
                var = t[1][t[1].index("addr:") + len("addr:"):]

                return var

            return ""

        elif entity == "config":
            cmd = "grep " + obj_name + " /etc/aqueti/daemonConfiguration.json"

            var_rs = self.exec_cmd(cmd)
            if var_rs != "":
                t = var_rs.split(":")
                var = t[1].replace('"', '').replace(',','').strip()

                return var

            return ""

        elif entity in ("version"):
            cmd = "dpkg -s " + obj_name + " | grep Version"

            var_rs = self.exec_cmd(cmd)
            if var_rs != "":
                t = var_rs.split()
                var = t[1]

                return var

            return ""

        elif entity == "app_version":
            cmd = "AquetiDaemonProcess --version"

            var_rs = self.exec_cmd(cmd)
            if var_rs != "":
                t = var_rs.split()
                var = t[1][1:] + "_" + t[-1]

                return var

            return ""

        elif entity in ("status"):
            cmd = "sudo service " + obj_name + " status | grep Active"

            var_rs = self.exec_cmd(cmd)
            if var_rs != "":
                t = var_rs.split()
                var = t[1]

                return var

            return ""

        elif entity in ("uptime"):
            cmd = "sudo service " + obj_name + " status | grep Active"

            var_rs = self.exec_cmd(cmd)
            if var_rs != "":
                if "ago" in var_rs:
                    t = var_rs[var_rs.rindex(";") + 1:var_rs.index("ago")]
                    var = t.strip()

                    return var

            return ""

        else:
            return "unknown"

info = Info()
print(json.dumps(info.json))
