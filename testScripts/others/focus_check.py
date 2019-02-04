import datetime as dt
import os
import time
import subprocess


cam_ip = '10.1.12.'
num_of_tegras = 9

def exec(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stdout.decode('utf-8') != "":
        return result.stdout.decode('utf-8')
    else:
        return result.stderr.decode('utf-8')

def get_ssh_str(cmd, ip):
    return "ssh nvidia@" + ip + " '" + cmd + "'"

def is_working():
    res = []
    for tegra_ip in [cam_ip + str(i) for i in range(1, num_of_tegras + 1)]:
        rc = exec('ping -W 1 -c 1 ' + tegra_ip)
        if '0 received' in rc:
            break            
        else:
            res.append(tegra_ip)            
    if len(res) == num_of_tegras:
        return True
    else:
        return False

home = os.path.expanduser("~")
path = home + '/jpeg'

for tegra_ip in [cam_ip + str(i) for i in range(1, num_of_tegras + 1)]:
    for sensor_id in [str(i) for i in (0, 1)]:
        if not os.path.exists(path + '/' + tegra_ip + '/' + sensor_id):
            exec('mkdir -p ' + path + '/' + tegra_ip + '/' + sensor_id)

res = {cam_ip + str(i): {str(j): [] for j in (0, 1)} for i in range(1, num_of_tegras + 1)}

for cnt in range(1, 1000):
    while not is_working():
        sleep(15)
    
    print('iteration: ', cnt)
    for tegra_ip in [cam_ip + str(i) for i in range(1, num_of_tegras + 1)]:        
        for sensor_id in [str(i) for i in (0, 1)]:            
            exec(get_ssh_str('python /home/nvidia/get_focus_val/get_focus_val.py -id ' + sensor_id + ' > temp.txt', tegra_ip))
            res[tegra_ip][sensor_id].append(exec(get_ssh_str('cat temp.txt | tail -1', tegra_ip)))
            time.sleep(5)
            exec(get_ssh_str('rm *.jpg', tegra_ip))
            #exec(get_ssh_str('/home/nvidia/tegra_multimedia_api/argus/build/samples/yuvJpeg/argus_yuvjpeg -d ' + sensor_id, tegra_ip))
            exec(get_ssh_str('nvgstcapture-1.0 --mode 1 --image-res 8 -A --capture-auto 1 --sensor-id ' + sensor_id, tegra_ip))                 
            time.sleep(5)            
            file_name = exec(get_ssh_str('ls *.JPG | tail -1', tegra_ip)).strip()                       
            exec("scp nvidia@" + tegra_ip + ":./" + file_name + ' ' + home)            
            exec(get_ssh_str('rm *.JPG', tegra_ip))
            date = dt.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            exec("mv " + home + '/' + file_name + " " + path + '/' + tegra_ip + '/' + sensor_id + '/' + str(cnt) + '_' + date + ".jpeg")
            print("tegra: %s sensor: %s" % (tegra_ip, sensor_id))
    
    while is_working():
        sleep(15)
