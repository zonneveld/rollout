#!/bin/sh
apt-get update -y &&
apt-get install python3-pip -y &&
apt-get install i2c-tools -y &&
pip install netifaces &&
pip install adafruit-circuitpython-motorkit &&
pip install adafruit-circuitpython-ssd1306 &&
pip install adafruit-circuitpython-servokit &&
#we doen i2c handmatig

#services:
cp server_start.service  /lib/systemd/system/server_start.service &&
chmod 644 /lib/systemd/system/server_start.service &&
systemctl daemon-reload &&
systemctl enable server_start.service &&
echo "done!"
