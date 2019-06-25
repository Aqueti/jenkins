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
    print("--cam\t\tcamera id")
    print("--acos\t\tbranch_name/build_number")
    print("--asis\t\tbranch_name/build_number")
    print("--type\t\tdebug/release")
    print("--noinstall\tjust download")
    print("--norestart\tno daemon restart on render/tegras")
    print()
    print("example: ./install.py --cam 7 --acos dev/65 --asis master/95 --noinstall")

if "--help" in sys.argv:
    print_help()
    exit(0)

if "--cam" in sys.argv:
    cam_id = sys.argv[sys.argv.index("--cam") + 1]

    cam_ip = '10.1.' + cam_id + '.'
    start_ip = 1

    if cam_id in [str(id) for id in (4, 9, 12)]:
        num_of_tegras = 9
    elif cam_id in [str(id) for id in (100, 101, 102, 103)]:
        num_of_tegras = 3
    else:
        num_of_tegras = 10
else:
    print("cam isn't specified\n")
    cam_ip = ''

type = 'release'
if "--type" in sys.argv:
    type = sys.argv[sys.argv.index("--type") + 1]


res = []
projs = ["acos"] + (["asis"] if "--asis" in sys.argv else [])

for proj in projs:    

    base_url = "http://10.0.0.10/repositories/" + proj
        
    branch_name = 'dev'
    build = ""
    if ("--" + proj) in sys.argv:
        if len(sys.argv) > sys.argv.index("--" + proj) + 1:
            if "--" not in sys.argv[sys.argv.index("--" + proj) + 1]:
                arr = sys.argv[sys.argv.index("--" + proj) + 1].split("/")
                branch_name = arr[0]
                build = arr[1] if len(arr) > 1 else ""

                if build != "":
                    try:
                        build = str(int(build))
                    except:
                        print("build should be integer")
                        exit(0)

    try:
        urllib.request.urlopen(base_url)
    except:
        print("server is unavailable")
        exit(0)

    try:
        urllib.request.urlopen(base_url + '/' + branch_name)
    except:
        print("branch not found")
        exit(0)


    if build == "":

        page = urllib.request.urlopen(base_url + '/' + branch_name)
            
        tree = etree.HTML(page.read())

        bres = tree.xpath('//h2//a')

        build = get_max(bres)

    try:
        page = urllib.request.urlopen(base_url + '/' + branch_name + '/' + str(build))
    except Exception:
        print("build not found")
        exit(0)

    tree = etree.HTML(page.read())

    folder_path = "builds/" + branch_name + '/' + str(build) + '/'
    os.system("mkdir -p " + folder_path)

    files = dict()
    for e in tree.xpath('//a'):
        if ".deb" in e.text:
            if type == 'debug':
                if 'debug' not in e.text:
                    continue
            else:
                if 'debug' in e.text:
                    continue
            
            if "Daemon" in e.text:
                if "x86_64" in e.text:
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
                files["asis"] = e.text
            else:
                continue
            
            if not os.path.isfile(folder_path + e.text):
                print("saving file: " + folder_path + e.text)
                file = urllib.request.urlopen(base_url + '/' + branch_name + '/' + str(build) + '/' + e.text)                
                with open(folder_path + e.text, 'wb') as output:
                    output.write(file.read())                    

    res += tree.xpath('//a')


if len(res) == 0:
    print('no deb packages found')
    exit(0)

if len(files.keys()) == 0:
    print('No files available')
    exit(0)

if "--noinstall" in sys.argv:
    print('Files downloaded')
    exit(0)

if cam_ip != '':
    for i in range(start_ip, num_of_tegras + start_ip):
        tegra_ip = cam_ip + str(i)
        print('*************')
        print(tegra_ip)
        print('*************')

        if 'aci' in files.keys():
            os.system("scp " + folder_path + files["aci"] + " nvidia@" + tegra_ip + ":./")            
            os.system("ssh nvidia@" + tegra_ip + " 'sudo dpkg -r aci'")  
            os.system("ssh nvidia@" + tegra_ip + " 'sudo dpkg -i " + files["aci"] + "'")
        
        if 'daemon_aarch64' in files.keys():
            os.system("scp " + folder_path + files["daemon_aarch64"] + " nvidia@" + tegra_ip + ":./")            
            os.system("ssh nvidia@" + tegra_ip + " 'sudo dpkg -r aquetidaemon'") 
            os.system("ssh nvidia@" + tegra_ip + " 'sudo dpkg -i " + files["daemon_aarch64"] + "'")

        os.system("ssh nvidia@" + tegra_ip + " 'rm *.deb 2>/dev/null'")


os.system("sudo pkill -9 AquetiDaemon; sudo service Aqueti-Daemon stop")
os.system("sudo dpkg -r aquetidaemon-daemon")
os.system("sudo dpkg -r aquetidaemon-application")
os.system("sudo dpkg -r aquetiapi")
os.system("sudo dpkg -r calibrationtools")

if 'asis' in files.keys():
    os.system("sudo dpkg -r asis")

if 'api' in files.keys():    
    os.system("sudo dpkg -i " + folder_path + files["api"])
if 'ctools' in files.keys():        
    os.system("sudo dpkg -i " + folder_path + files["ctools"])
if 'daemon_x86-app' in files.keys():        
    os.system("sudo dpkg -i " + folder_path + files["daemon_x86-app"])
    os.system("sudo dpkg -i " + folder_path + files["daemon_x86-d"])    
if 'asis' in files.keys():        
    os.system("sudo dpkg -i " + folder_path + files["asis"])


if "--norestart" not in sys.argv:
    print("\nRestarting service\n")

    if 'daemon_x86-app' in files.keys():
        os.system("sudo pkill -9 AquetiDaemon")

    if cam_ip != '':
        for i in range(start_ip, num_of_tegras + start_ip):
            os.system("ssh nvidia@" + cam_ip + str(i) + " 'sudo pkill -9 AquetiDaemon'")

    if 'asis' in files.keys():
        os.system("sudo service asisd restart")

print("***** Done *****")
