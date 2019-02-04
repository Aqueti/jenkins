import datetime as dt
import os
import time
import subprocess


cam_ip = '10.1.7.'
num_of_tegras = 10
delay = 60

def exec(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.stdout.decode('utf-8') != "":
        return result.stdout.decode('utf-8')
    else:
        return result.stderr.decode('utf-8')

def get_ssh_str(cmd, ip):
    return "ssh nvidia@" + ip + " '" + cmd + "'"


with open('out.txt', 'w') as file:
    file.write('start time: ' + str(dt.datetime.now()) + '\n-------------\n')
    
prev_delta = {cam_ip + str(k): dt.timedelta(0) for k in range(1, num_of_tegras + 1)}
while True:
    for tegra_ip in [cam_ip + str(i) for i in range(1, num_of_tegras + 1)]:               
        ctime = exec(get_ssh_str('sudo service Aqueti-Daemon status | grep Active', tegra_ip))
        try:
            ctime = ctime[ctime.index('2019'): ctime.index('UTC') - 1]
        except ValueError:
            print('error')
            exit(0)
        ntime = dt.datetime.strptime(ctime, '%Y-%m-%d %H:%M:%S')
                
        now = dt.datetime.utcnow()
                
        delta = now - ntime        
        
        if prev_delta[tegra_ip] > delta:
            with open('out.txt', 'a') as file:
                file.write(str(now) + '\t' + tegra_ip + '\t' + str(prev_delta[tegra_ip]) + '\n')

            print("tegra: %s time: %s uptime: %s" % (tegra_ip, now, prev_delta[tegra_ip]))
        else:
            print('.', end='')
        
        prev_delta[tegra_ip] = delta
            
    print()

    time.sleep(delay)
