s = """
[Unit]
Description=SysInfo Service
After=multi-user.target

[Service]
Type=idle
WorkingDirectory=/opt/infoprovider
ExecStart=/usr/bin/python3 /opt/infoprovider/provider.py
Restart=always
StandardOutput=syslog
StandardError=syslog

[Install]
WantedBy=multi-user.target
"""

with open("/etc/systemd/system", "w") as file:
    file.write(s)
