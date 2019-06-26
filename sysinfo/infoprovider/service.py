s = """
[Unit]
Description=SysInfo Service

[Service]
Type=Simple
WorkingDirectory=/opt/get_info
ExecStart=/usr/bin/python3 /opt/infoprovider/provider.py
Restart=always
RestartSec=30

[Install]
WantedBy=sysinit.target
"""

with open("/etc/systemd/system/sysinfo.service", "w") as file:
    file.write(s)
