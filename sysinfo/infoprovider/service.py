s = """
[Unit]
Description=SysInfo Service
After=syslog.target

[Service]
Type=Simple
User=mosaic
Group=mosaic
WorkingDirectory=/opt/infoprovider
ExecStart=/usr/bin/python3 /opt/infoprovider/provider.py
StandardOutput=syslog
StandardError=syslog
Restart=always
RestartSec=30


[Install]
WantedBy=multi-user.target

"""

with open("/etc/systemd/system/infoprovider.service", "w") as file:
    file.write(s)
