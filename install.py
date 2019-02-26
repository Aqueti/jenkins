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
    print("--noinstall")
    print("--asis")

    exit(1)

base_url = "http://10.0.0.10/repositories"

if "--help" in sys.argv:
    print_help()

if "--cam" in sys.argv:
    cam_id = sys.argv[sys.argv.index("--cam") + 1]

    cam_ip = '10.1.' + cam_id + '.'
    start_ip = 1
    
    if cam_id == str(9) or cam_id == str(12):
        num_of_tegras = 9
    elif cam_id == str(149):
        num_of_tegras = 3
    else:   
        num_of_tegras = 10
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
    if ".deb" in e.text:
        if "Daemon" in e.text:
            if "x86_64" in e.text:
                if type == 'debug':
                    if 'debug' not in e.text:
                        continue
                else:
                    if 'debug' in e.text:
                        continue
                
                if '-application' in e.text:
                    files["daemon_x86-app"] = e.text
                elif '-daemon' in e.text:
                    files["daemon_x86-d"] = e.text
            else:
                files["daemon_aarch64"] = e.text
        elif "ACI" in e.text:
            files["aci"] = e.text
        elif "API" in e.text:
            files["api"] = e.text
        elif "CalibrationTools" in e.text:
            files["ctools"] = e.text
        elif "ASIS" in e.text:
            if "--asis" in sys.argv:
                files["asis"] = e.text
            else:
                continue
        
        if os.path.exists(folder_path + e.text):
            file = urllib.request.urlopen(base_url + '/' + branch_name + '/' + str(build) + '/' + e.text)
            with open(folder_path + e.text, 'wb') as output:
                output.write(file.read())
                print("saved file: " + folder_path + e.text)

if "--noinstall" in sys.argv:
    print('Files downloaded')
    exit(0)

if cam_ip != '':
    for i in range(start_ip, num_of_tegras + start_ip):
        tegra_ip = cam_ip + str(i)
        print('*************')
        print(tegra_ip)
        print('*************')

        if 'daemon_aarch64' in files.keys():
            os.system("scp " + folder_path + files["daemon_aarch64"] + " nvidia@" + tegra_ip + ":./")
            os.system("ssh nvidia@" + tegra_ip + " 'sudo dpkg -r aquetidaemon'")
            os.system("ssh nvidia@" + tegra_ip + " 'sudo dpkg -i " + files["daemon_aarch64"] + "'")

        if 'aci' in files.keys():
            os.system("scp " + folder_path + files["aci"] + " nvidia@" + tegra_ip + ":./")
            os.system("ssh nvidia@" + tegra_ip + " 'sudo dpkg -r aquetiaci'")
            os.system("ssh nvidia@" + tegra_ip + " 'sudo dpkg -i " + files["aci"] + "'")

        os.system("ssh nvidia@" + tegra_ip + " 'rm *.deb 2>/dev/null'")

os.system("sudo dpkg -r aquetidaemon-daemon")
os.system("sudo dpkg -r aquetidaemon-application")
os.system("sudo dpkg -r aquetiapi")
os.system("sudo dpkg -r calibrationtools")
    
if 'daemon_x86-app' in files.keys():        
    os.system("sudo dpkg -i " + folder_path + files["daemon_x86-app"])
    os.system("sudo dpkg -i " + folder_path + files["daemon_x86-d"])
if 'api' in files.keys():    
    os.system("sudo dpkg -i " + folder_path + files["api"])
if 'ctools' in files.keys():        
    os.system("sudo dpkg -i " + folder_path + files["ctools"])
if 'asis' in files.keys():        
    os.system("sudo dpkg -i " + folder_path + files["asis"])

print("***** Done *****")
