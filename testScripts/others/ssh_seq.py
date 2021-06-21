import paramiko
import subprocess
import json


servers = []

ssh_conns = {}
for ip in servers:
  ssh_conns[ip] = paramiko.SSHClient()
  ssh_conns[ip].load_system_host_keys()
  ssh_conns[ip].set_missing_host_key_policy(paramiko.AutoAddPolicy())

  server, port, username, password = ip, "22", "aqueti", None
  ssh_conns[ip].connect(server, port, username=username, password=password, timeout=999999999)


for ip, ssh_conn in ssh_conns.items():
  cmd = 'hostname'
  ssh_stdin, ssh_stdout, ssh_stderr = ssh_conn.exec_command(cmd, bufsize=-1, timeout=None, get_pty=False)

  print(ssh_stdout.read().decode('utf-8'))


for ip, ssh_conn in ssh_conns.items():
  ssh_conn.close()
