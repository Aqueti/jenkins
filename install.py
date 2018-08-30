#!/usr/bin/python3

import sys
import os
import time
import urllib.request
from lxml import etree

def str_to_int(text):
    try:
        val = int(text)
    except ValueError:
        val = 0

    return val

def get_max(res):
    max = 0
    for e in res:
        val = str_to_int(e.text)
        if max < val:
            max = val

    return max

def print_help():
    print("--cam\t\tCamera id")
    print("--branch\tBranch name")
    print("--build\t\tBuild number")
    print("--type\t\tdebug/release")

    exit(1)

base_url = "http://10.0.0.10/repositories"

if "--help" in sys.argv:
    print_help()

if "--cam" in sys.argv:
    cam_id = sys.argv[sys.argv.index("--cam") + 1]

    if cam_id == str(4):
        cam_ip = '10.1.4.'
        start_ip = 1
        num_of_tegras = 10
    elif cam_id == str(7):
        cam_ip = '10.1.7.'
        start_ip = 1
        num_of_tegras = 10
    elif cam_id == str(8):
        cam_ip = '10.0.8.'
        start_ip = 1
        num_of_tegras = 10
    elif cam_id == str(9):
        cam_ip = '10.1.9.'
        start_ip = 1
        num_of_tegras = 9
    elif cam_id == str(11):
        cam_ip = '10.1.11.'
        start_ip = 1
        num_of_tegras = 9
    elif cam_id == str(12):
        cam_ip = '10.1.12.'
        start_ip = 1
        num_of_tegras = 9
    elif cam_id == str(14):
        cam_ip = '10.1.14.'
        start_ip = 1
        num_of_tegras = 10
    elif cam_id == str(15):
        cam_ip = '10.1.4.'
        start_ip = 1
        num_of_tegras = 10
    elif cam_id == str(166):        
        cam_ip = '192.168.10.'
        start_ip = 1       
        num_of_tegras = 5
    elif cam_id == str(159):
        cam_ip = '192.168.10.'
        start_ip = 6
        num_of_tegras = 5
    else:
        cam_ip = ''
else:
    print("cam isn't specified\n")
    cam_ip = ''

if "--type" in sys.argv:
    type = sys.argv[sys.argv.index("--type") + 1]
else:
    type = 'release'

if "--branch" in sys.argv:
    branch_name = sys.argv[sys.argv.index("--branch") + 1]
else:
    branch_name = 'master'

if "--build" in sys.argv:
    build = sys.argv[sys.argv.index("--build") + 1]
else:
    page = urllib.request.urlopen(base_url + '/' + branch_name)

    tree = etree.HTML(page.read())

    res = tree.xpath('//h2//a')

    build = get_max(res)

if "--run" in sys.argv:
    isRun = True  #sys.argv[sys.argv.index("--run") + 1]
else:
    isRun = False

try:
    page = urllib.request.urlopen(base_url + '/' + branch_name + '/' + str(build))
except Exception:
    print("build not found")
    exit(1)

tree = etree.HTML(page.read())
res = tree.xpath('//a')

if len(res) == 0:
    print('no deb packages found')
    exit(1)

folder_path = "builds/" + branch_name + '/' + str(build) + '/'
os.system("mkdir -p " + folder_path)

files = dict()
for e in res:
    if ".deb" in e.text or ".gz" in e.text:
        if "Daemon" in e.text:
            if "x86_64" in e.text:
                if "debug" in e.text:
                    files["daemon_x86_debug"] = e.text
                else:
                    files["daemon_x86"] = e.text
            else:
                files["daemon_aarch64"] = e.text
        elif "ACI" in e.text:
            files["aci"] = e.text
        elif "API" in e.text:
            files["api"] = e.text
        elif "QView" in e.text:
            files["qviewer"] = e.text
        elif "QWebServer" in e.text:
            files["qwebserver"] = e.text
        elif "homunculus" in e.text:
            files["homunculus"] = e.text
        elif "CalibrationTools" in e.text:
            files["ctools"] = e.text

        file = urllib.request.urlopen(base_url + '/' + branch_name + '/' + str(build) + '/' + e.text)
        with open(folder_path + e.text, 'wb') as output:
            output.write(file.read())
            print("saved file: " + folder_path + e.text)

if cam_ip != '':
    for i in range(start_ip, num_of_tegras + start_ip):
        tegra_ip = cam_ip + str(i)
        print('*************')
        print(tegra_ip)
        print('*************')
        os.system("scp " + folder_path + files["daemon_aarch64"] + " nvidia@" + tegra_ip + ":./")
        os.system("ssh nvidia@" + tegra_ip + " 'sudo dpkg -r aquetidaemon 2>/dev/null'")
        os.system("ssh nvidia@" + tegra_ip + " 'sudo dpkg -i " + files["daemon_aarch64"] + " 2>/dev/null'")
        os.system("ssh nvidia@" + tegra_ip + " 'rm *.deb 2>/dev/null'")

        #os.system("scp " + files["aci"] + " nvidia@" + tegra_ip + ":./")
        #os.system("ssh nvidia@" + tegra_ip + " 'sudo dpkg -i " + files["aci"] + "'")

if type == "release":
    if 'daemon_x86' in files.keys():
        os.system("sudo dpkg -r aquetidaemon")
        os.system("sudo dpkg -i " + folder_path + files["daemon_x86"])
else:
    if 'daemon_x86_debug' in files.keys():
        os.system("sudo dpkg -r aquetidaemon")
        os.system("sudo dpkg -i " + folder_path + files["daemon_x86_debug"])

if 'api' in files.keys():
    os.system("sudo dpkg -r aquetiapi")
    os.system("sudo dpkg -i " + folder_path + files["api"])
if 'ctools' in files.keys():
    os.system("sudo dpkg -r calibrationtools")    
    os.system("sudo dpkg -i " + folder_path + files["ctools"])
if 'qviewer' in files.keys():
    os.system("sudo rm /opt/QView* 2>/dev/null")
    os.system("sudo cp " + files["qviewer"] + " /opt")
if 'qwebserver' in files.keys():
    if "dpkg -s docker-ce 1>/dev/null 2>&1" == 0:
        os.system("zcat " + files["qwebserver"] + " | sudo docker load")

print("***** Done *****")
