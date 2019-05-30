import os
import subprocess
import time


def exec_cmd(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.stdout.decode('utf-8') != "":
        return result.stdout.decode('utf-8')
    else:
        return result.stderr.decode('utf-8')


def get_speed(ifname):
    w_time = 2
    cmd = "cat /proc/net/dev | grep " + ifname + " | awk '{print$2}'"
    start = int(exec_cmd(cmd))
    time.sleep(w_time)
    stop = int(exec_cmd(cmd))

    return (stop - start) / (w_time * 1e6)


folder = ""
def checkout():
    def exec_cmd_sp(cmd, ifname):
        global folder
        p = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        err = p.stderr.readline()
        out = p.stdout.readline()
        if b'' != out:
            out = str(out)
            folder = out[out.index("'") + 1:]
            folder = folder[:folder.index("'")]

        print('out', out)
        print('err', err)

        if b"revision" in err:
            exec_cmd("rm -rf " + folder)

            return 1

        while p.poll() is None:
            speed = get_speed(ifname)
            if speed < 5:
                print('speed', speed)
                p.terminate()

                return 1

        if out == err:
            return 0

    cmd = "git submodule update --init --checkout"
    iface = "enp0s31f6"

    return exec_cmd_sp(cmd, iface)


cmd = "git clone https://github.com/aqueti/acos.git"
exec_cmd(cmd)

os.chdir('acos')

r = 1
while r != 0:
    r = checkout()
    time.sleep(2)
