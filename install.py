#!/usr/bin/python3

import sys
import os
import time
import urllib.request
from lxml import etree
import argparse


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

def is_integer(v):
    try:
        int(v)
        return True
    except:
        return False

def custom_action(c_arg):
    class CustomAction(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            setattr(args, self.dest, values)
    return CustomAction

parser = argparse.ArgumentParser()
parser.add_argument("--cam",  help="camera id", required=False)
parser.add_argument("--acos", help="branch_name/build_number", required=False, default="dev")
parser.add_argument("--asis", help="branch_name/build_number", required=False, action=custom_action("dev"))
parser.add_argument("--debug", help="debug/release", required=False, action='store_true')
parser.add_argument("--noinstall", help="just download", required=False, action='store_true')
parser.add_argument("--norestart", help="no daemon restart on render/tegras", required=False, action='store_true')
args = parser.parse_args()

if all(v is None for v in vars(args).values()):
    parser.print_help(sys.stdout)
    print("\nexample: ./install.py --cam 7 --acos beta/280 --asis dev/149 --noinstall\n")
    exit(0)

cam_ip = ''
if args.cam is not None:
    if not is_integer(args.cam):
        print("cam id should be integer")
        exit(1)

    cam_ip = '10.1.{}.'.format(args.cam)

    start_ip = 1

    if args.cam in [str(id) for id in [4, 9, 12]]:
        num_of_tegras = 9
    elif args.cam in [str(id) for id in [66]]:
        num_of_tegras = 3
    else:
        num_of_tegras = 10


res = []
files = {}
for proj in (["acos"] + (["asis"] if getattr(args, "asis") is not None else [])):
    base_url = "http://10.0.0.10/repositories/" + proj

    if getattr(args, proj) is not None:
        arr = getattr(args, proj).split("/") 
        branch_name, build = (arr[0], arr[1] if len(arr) > 1 else -1)

        if not is_integer(build):
            print("build should be integer")
            exit(1)
    else:
        branch_name, build = ("dev", -1)

    try:
        urllib.request.urlopen(base_url)
    except:
        print("server is unavailable")
        exit(1)

    try:
        urllib.request.urlopen(base_url + '/' + branch_name)
    except:
        print("branch not found")
        exit(1)

    if build == -1:
        page = urllib.request.urlopen(base_url + '/' + branch_name)            
        tree = etree.HTML(page.read())
        bres = tree.xpath('//h2//a')
        build = get_max(bres)

    try:
        page = urllib.request.urlopen(base_url + '/' + branch_name + '/' + str(build))
    except Exception:
        print("build not found")
        exit(1)

    tree = etree.HTML(page.read())

    folder_path = "builds/{}/{}/".format(branch_name, str(build))
    os.system("mkdir -p {}".format(folder_path))
    
    for e in tree.xpath('//a'):
        if ".deb" in e.text:
            if args.debug:
                if 'debug' not in e.text:
                    continue
            else:
                if 'debug' in e.text:
                    continue
            
            if "Daemon" in e.text:
                if "x86_64" in e.text:
                    if '-application' in e.text:
                        files["daemon_x86-app"] = folder_path + e.text
                    elif '-daemon' in e.text:
                        files["daemon_x86-d"] = folder_path + e.text
                else:
                    files["daemon_aarch64"] = folder_path + e.text
            elif "ACI" in e.text:
                files["aci"] = folder_path + e.text
            elif "API" in e.text:
                files["api"] = folder_path + e.text
            elif "CalibrationTools" in e.text:
                files["ctools"] = folder_path + e.text
            elif "ASIS" in e.text:
                files["asis"] = folder_path + e.text
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
    exit(1)

if len(files.keys()) == 0:
    print('No files available')
    exit(1)

if args.noinstall:
    print('Files downloaded')
    exit(0)


if cam_ip != '':
    for tegra_ip in [cam_ip + str(i + start_ip) for i in range(num_of_tegras)]:
        d_str = "".join(["-" for i in range(16)])
        print("\n{}\n{}\n{}\n".format(d_str, tegra_ip, d_str))

        for package in ['aci', 'daemon_aarch64']:
            cmd = "scp {} nvidia@{}:./".format(files[package], tegra_ip)
            os.system(cmd)
            pack_name = "aci" if package == "aci" else "aquetidaemon"
            cmd = "ssh nvidia@{} 'sudo dpkg -r {}'".format(tegra_ip, pack_name)
            os.system(cmd)
            cmd = "ssh nvidia@{} 'sudo dpkg -i {}'".format(tegra_ip, files[package][files[package].rindex('/') + 1:])
            os.system(cmd)

        cmd = "ssh nvidia@{} 'rm *.deb 2>/dev/null'".format(tegra_ip)
        os.system(cmd)


if 'daemon_x86-app' in files.keys():
    os.system("sudo pkill -9 AquetiDaemon; sudo service Aqueti-Daemon stop")

    os.system("sudo dpkg -r aquetidaemon-daemon")
    os.system("sudo dpkg -r aquetidaemon-application")
    os.system("sudo dpkg -i " + files["daemon_x86-app"])
    os.system("sudo dpkg -i " + files["daemon_x86-d"])
if 'api' in files.keys():
    os.system("sudo dpkg -r aquetiapi")
    os.system("sudo dpkg -i " + files["api"])
if 'ctools' in files.keys():
    os.system("sudo dpkg -r calibrationtools")
    os.system("sudo dpkg -i " + files["ctools"])

if 'asis' in files.keys():
    os.system("sudo dpkg -r asis")
    os.system("sudo dpkg -i " + files["asis"])

if not args.norestart:
    print("\nRestarting service\n")

    if 'daemon_x86-app' in files.keys():
        os.system("sudo pkill -9 Aqueti; sudo service Aqueti-Daemon restart")

    if cam_ip != '':
        for i in range(start_ip, num_of_tegras + start_ip):
            os.system("ssh nvidia@" + cam_ip + str(i) + " 'sudo pkill -9 AquetiDaemon'")

    if any(s in files.keys() for s in ('daemon_x86-app', 'asis')):
        os.system("sudo service asisd restart")

print("***** Done *****")