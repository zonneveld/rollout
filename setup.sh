#!/bin/sh
apt-get update -y &&
apt-get install python3-pip -y &&
apt-get install i2c-tools -y &&
pip install netifaces &&
pip install adafruit-circuitpython-motorkit &&
pip install adafruit-circuitpython-ssd1306 &&
pip install adafruit-circuitpython-servokit &&
#we doen i2c handmatig

#enviroment:
# cp rollout_env.sh /etc/enviroment/rollout_env.sh && <-- niet meer gebruiken!

#services:
cp boot_start.service  /lib/systemd/system/boot_start.service &&
chmod 644 /lib/systemd/system/boot_start.service &&

cp server_start.service  /lib/systemd/system/server_start.service &&
chmod 644 /lib/systemd/system/server_start.service &&

systemctl daemon-reload &&
systemctl enable boot_start.service &&
systemctl enable server_start.service &&


echo "done installing" 
echo "however, some things only work after a reboot!" 
read -p "Do you want to reboot now? Type y for yes" -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    systemctl reboot -i
fi

