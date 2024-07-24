#!/bin/bash

# Update system and install dependencies
apt-get update
apt-get install -y python3 python3-pip nginx docker.io
pip3 install psutil docker prettytable

# Copy the devopsfetch script to /usr/local/bin
cp devopsfetch.py /usr/local/bin/devopsfetch
chmod +x /usr/local/bin/devopsfetch

# Create systemd service file
cat <<EOL > /etc/systemd/system/devopsfetch.service
[Unit]
Description=DevOps Fetch Service
After=network.target

[Service]
ExecStart=/usr/local/bin/devopsfetch -d
Restart=always
User=root
Group=root
Environment=PYTHONUNBUFFERED=1
StandardOutput=append:/var/log/devopsfetch.log
StandardError=append:/var/log/devopsfetch_error.log
SyslogIdentifier=devopsfetch

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd, enable and start the service
systemctl daemon-reload
systemctl enable devopsfetch
systemctl start devopsfetch
