import AQT
import sys
import time
import json
import csv
import os
import datetime as dt
import subprocess
import ctypes
import argparse


def exec_cmd(cmd):
	res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	return res.stdout.decode('utf-8') + res.stderr.decode('utf-8')

def get_ssh_str(cmd, ip, username):
	return "ssh {}@{} '{}'".format(username, ip, cmd)

def get_perf_info(date):
	cmd = "nproc"
	cpu_num = int(exec_cmd(cmd))

	cmd = "ls -A /sys/class/net | wc -l"
	net_num = int(exec_cmd(cmd))

	cmd = "atop -r /var/log/atop/atop_{} > atop.txt".format(date.strftime("%Y%m%d"))	
	rt = exec_cmd(cmd)

	if "No such file or directory" in rt:
		return None

	f_name = ""

	cmd = "cat atop.txt | grep -m 1 -A{}".format(str(cpu_num + net_num + 10)) + " '" + "{}  {}".format(date.strftime("%Y/%m/%d"), date.strftime("%H:%M")) + "' |  grep -E '(CPU \||MEM \||DSK \||NET \|)'"
	rt = exec_cmd(cmd)

	info = {}
	for row in [v for v in rt.split("\n") if v != ""]:
		col_name = ""
		c_info = info

		cols = row.split("|")
		for i in range(len(cols)):
			col = cols[i].strip()
			if col == "":
				continue

			if i == 0:
				col_name = col.split(" ")[0].strip()
				continue
			elif i == 1:
				if i == 1 and col_name in ("NET", "DSK"):
					if col_name not in c_info.keys():
						c_info[col_name] = {}

					c_info = c_info[col_name]
					col_name = col.split(" ")[0].strip()
					c_info[col_name] = {}

					continue

			k, v = [col[:col.index(" ")], col[col.index(" "):].strip()]
			c_info.setdefault(col_name, {}).update({k: v})

	return info


home_path = os.path.join(os.path.expanduser("~"), "stats")
server_logs_path = os.path.join(home_path, "servers")
cam_logs_path = os.path.join(home_path, "cams")

servers_list = {"10.1.1.101": "mosaic", 
				"10.1.1.158": "mosaic", 
				"10.1.1.177": "aqueti", 
				"10.1.1.189": "mosaic", 
				"10.1.1.204": "jenkins", 
				"10.1.1.228": "aqueti"}

cams_list = {"10.1.2": 10, 
			 "10.1.7": 10, 
			 "10.1.9": 9, 
			 "10.1.11": 10, 
			 "10.1.12": 9, 
			 "10.1.77": 10}

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--collect", help="Collects logs", required=False)
parser.add_argument("-a", "--analyze", help="Analyzes logs", required=False)
parser.add_argument("-v", "--visualize", help="Visualizes the result", required=False)
args = parser.parse_args()

if all(v is None for v in vars(args).values()):
    parser.print_help(sys.stdout)

# collecting

if args.collect is not None:
	def create_dir(path):
		if not os.path.exists(path):
			os.makedirs(path)

	def copy_logs(ip, username, c_dir):	
		cmd = "sudo rm /var/log/syslog.0*; sudo -u syslog cp /var/log/syslog /var/log/syslog.0; sudo chown syslog:adm /var/log/syslog.0"
		exec_cmd(get_ssh_str(cmd, ip, username))

		for i in range(2):
			cmd = "sudo -u syslog gzip /var/log/syslog.{}".format(i)			
			exec_cmd(get_ssh_str(cmd, ip, username))			

		cmd = "scp {}@{}:/var/log/syslog.*.gz {}".format(username, ip, c_dir)
		exec_cmd(cmd)


	for ip, username in servers_list.items():
		print("server: {}".format(ip))

		c_dir = "{}/{}".format(server_logs_path, ip)
		create_dir(c_dir)

		copy_logs(ip, username, c_dir)


	for cam, num_of_tegras in cams_list.items():
		print("camera: {}".format(cam))
		
		for i in range(1, num_of_tegras + 1):
			#print("{}".format(i), end=" ")

			c_dir = "{}/{}/{}".format(cam_logs_path, cam, i)
			create_dir(c_dir)
			
			copy_logs("{}.{}".format(cam, i), "nvidia", c_dir)

# analyzing

if args.analyze is not None:
	def add_to_csv(row, path=""):
		with open(os.path.join(path, "out.csv"), "a+", newline="") as f:
			writer = csv.writer(f, delimiter="\t")
			writer.writerow(row)

	def compress(f):
		def wrapper(*args, **kwargs):
			fpath = args[0]

			if ".gz" == os.path.splitext(fpath)[1]:
				fpath = fpath[:fpath.rindex(".")]
				cmd = "gunzip {}".format(fpath)
				exec_cmd(cmd)

			rt = f(fpath)

			if ".gz" == os.path.splitext(fpath)[1]:
				cmd = "gzip {}".format(fpath)
				exec_cmd(cmd)

			return rt

		return wrapper

	@compress
	def analyze(fpath, flag):
		print("analyzing: {}".format(fpath))

		cmd = "cat " + fpath + " | grep -a 'Initializing AquetiDaemonProcess' | awk '{print$1, $2, $3}'"
		rt = exec_cmd(cmd)

		rs = []		
		if rt != "":
			for row in rt.split("\n"):
				if row == "":
					continue

				d = dt.datetime.strptime(row, '%b %d %H:%M:%S')
				d = d.replace(int(time.strftime("%Y")))
				if flag == "tegra":
					d = d.replace(tzinfo=timezone.utc).astimezone(tz=None)
				rs.append(d)

		return rs

	for log_path in (cam_logs_path, server_logs_path):
		for path, directories, files in os.walk(log_path):
			for file in sorted(files):
				fpath = os.path.join(path, file)

				flag = "server" if path == server_logs_path else "tegra"
				t_arr = analyze(fpath, flag)

				if len(t_arr) > 0:
					for row in t_arr:
						if log_path == server_logs_path:
							add_to_csv([row, os.path.basename(path)], home_path)
						elif log_path == cam_logs_path:
							t_path = [i for i in path.split("/") if i != ""]
							add_to_csv([row, "{}.{}".format(t_path[-2], t_path[-1])], home_path)

# visualizing

if args.visualize is not None:
	import pandas as pd

	f_path = args.visualize
	if os. path. exists(f_path):
		pd.read_csv(f_path, sep="\t") 

