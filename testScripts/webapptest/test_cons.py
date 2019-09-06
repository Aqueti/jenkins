from BaseTest import BaseTest
import pytest
import time
import os
from datetime import datetime
from datetime import timedelta


class TestConsoleApps(BaseTest):
    browser = None

    cam_ip = "10.1.7."
    num_of_tegras = 10

    cam_id = 7
    data_dir_path = "/home/astepenko/Downloads/"
    zero_dir_path = data_dir_path + "0"

    def is_path_exists(self, path):
        if os.path.exists(path):
            return True
        else:
            return False

    def get_size(self, f_name = ""):
        if not self.is_path_exists(self.data_dir_path + f_name):
            self.failure_exception()

        cmd = "du -s " + self.data_dir_path + f_name + " | awk '{print$1}'"
        res = self.exec_cmd(cmd)

        return int(res)

    def get_values(self):
        res = {"hc_files": 0, "hc_docs": 0, "tracks": 0}

        cmd = "find " + self.zero_dir_path + " -name '*.hc' | wc -l"

        res["hc_files"] = int(self.exec_cmd(cmd))
        res["hc_docs"] = len(self.db.query({}, "acos_local", "files"))
        res["tracks"] = len(self.db.query({}, "acos", "tracks"))

        return res

    def get_ssh_str(self, ip, cmd):
        return "ssh nvidia@" + ip + " '" + cmd + "'"

    def clear_data(self):
        cmd = "rm -rf " + self.zero_dir_path
        res = self.exec_cmd(cmd)

        col_arr = [('acos', 'reservations'), ('acos', 'tracks'), ('acos_local', 'files')]
        for db_name, col_name in col_arr:
            self.db.drop(db_name, col_name)

    @pytest.mark.skip(reason="")
    def test_daemon_restart(self):

        for i in range(0, 10):
            for ip_tail in range(1, self.num_of_tegras + 1):
                cmd = self.get_ssh_str(self.cam_ip + str(ip_tail), "sudo pkill -9 Aqueti")
                self.exec_cmd(cmd)

                time.sleep(30)

                cmd = self.get_ssh_str(self.cam_ip + str(ip_tail), "pgrep acosd")
                res = self.exec_cmd(cmd)

                assert res != ''

    @pytest.mark.skip(reason="")
    def test_ei_all(self):
        #add logic to record data
        f_name = "export_all.bin"
        cmd = "AquetiExport -v " + self.data_dir_path + f_name
        res = self.exec_cmd(cmd)

        before = self.get_values()

        assert self.get_size(f_name) > 0

        self.clear_data()

        cmd = "Import -v " + self.data_dir_path + f_name
        res = self.exec_cmd(cmd)

        after = self.get_values()

        assert before == after

    @pytest.mark.skip(reason="")
    def test_export_time(self):
        cmd = "AquetiExport -s " + (datetime.now() - timedelta(minutes=10005)).strftime('%m/%d/%Y-%H:%M:%S') + " -e " + datetime.now().strftime('%m/%d/%Y-%H:%M:%S') + " " + self.data_dir_path + "export_all_se.bin"
        res = self.exec_cmd(cmd)

        assert self.get_size("export_all_se.bin") > 0

    @pytest.mark.skip(reason="")
    def test_export_time_cam(self):
        cmd = "AquetiExport -cam " + str(self.cam_id) + " -s " + (datetime.now() - timedelta(minutes=10005)).strftime('%m/%d/%Y-%H:%M:%S') + " -e " + datetime.now().strftime('%m/%d/%Y-%H:%M:%S') + " " + self.data_dir_path + "export_all_se_cam.bin"
        res = self.exec_cmd(cmd)

        assert self.get_size("export_all_se_cam.bin") > 0

    @pytest.mark.skip(reason="")
    def test_export_nodb(self):
        cmd = "AquetiExport -v -nodb " + self.zero_dir_path + " " + self.data_dir_path + "export_all_nodb.bin"
        res = self.exec_cmd(cmd)

        assert self.get_size("export_all_nodb.bin") > 0
