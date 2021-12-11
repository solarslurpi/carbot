# Overview
Carbot is part of Doctor GrowBuddy.  It's job is to move the car forward and back on the track.
# Software
Carbot runs on a Raspberry Pi.  It relies on the mosquitto service running on the raspberry pi to receive mqtt commands.
- __mosquitto__ must be up and running. In order to connect to the mosquitto service, the conf file must be modified.  I use the `/etc/mosquitto/conf.d/connect.conf file:
```
listener 1883
protocol mqtt

listener 9000
protocol websockets

allow_anonymous true
```
- added `allow_anonymous true` without this, I could not publish from a terminal on Rasp Pi.
- added `listener 9000` and `protocol websockets` with this, a react client cannot connect.  _Note: I arbitrarily use port 9000_
- `carbot.py`: Python app that handles (subscribes) to the 'carbot/move' commands (forward, backward, stop, faster, and slower).
- `carbot.service`: Systemd service file to start and stop carbot.py running.  To use this file, it must be copied.  `sudo cp carbot.service /lib/systemd/system/.`
## Debugging
- __Status__ provides info on whats going on with the carbot service.
- __Log Statements__ are sprinkled throughout `carbot.py` to help in debugging.
- __mosquitto log file__ provides info on the health of the mosquitto service.

### Status
Use `systemctl status carbot` and you will get info such as:
```
● carbot.service - carbot mqtt Script Service
     Loaded: loaded (/lib/systemd/system/carbot.service; enabled; vendor preset: enabled)
     Active: active (running) since Sat 2021-12-11 06:49:20 PST; 8s ago
   Main PID: 4394 (python3)
      Tasks: 1 (limit: 1597)
        CPU: 641ms
     CGroup: /system.slice/carbot.service
             └─4394 /usr/bin/python3 /home/pi/GrowBuddy/Doctor/carbot/carbot.py

Dec 11 06:49:20 doctorgrowbuddy systemd[1]: Started carbot mqtt Script Service.
Dec 11 06:49:21 doctorgrowbuddy python3[4394]: 2021-12-11 06:49:21,102:DEBUG:starting up!
Dec 11 06:49:21 doctorgrowbuddy python3[4394]: 2021-12-11 06:49:21,159:DEBUG:subscribing
```
We see debug statements are included.

### Log Statements
Additional debug info can be found in the `Journalctl` logfile.  To see the logfiles, notice the PID from the status info (e.g.: 4394 is the PID listed above) and then `Journalctl _PID=4394`
```
$ journalctl _PID=4394
-- Journal begins at Sat 2021-10-30 04:36:50 PDT, ends at Sat 2021-12-11 06:49:21 PST. --
Dec 11 06:49:21 doctorgrowbuddy python3[4394]: 2021-12-11 06:49:21,102:DEBUG:starting up!
Dec 11 06:49:21 doctorgrowbuddy python3[4394]: 2021-12-11 06:49:21,159:DEBUG:subscribing
Dec 11 06:49:21 doctorgrowbuddy python3[4394]: 2021-12-11 06:49:21,160:DEBUG:subscribed
```
There will be additional logging lines when `carbot.py` receives and processes the commands (forward, backward...).

To get the logs into `Journalctl`, `carbot` sends log files to `sys.stdout`.
`carbot.py` sets up logging to be handled by `Journalctl`.
### mosquitto log file
The mosquitto log file is found in `/var/log/mosquitto/mosquitto.log`.  It has records like:
```
1639229562: Config loaded from /etc/mosquitto/mosquitto.conf.
1639229562: Opening ipv4 listen socket on port 1883.
1639229562: Opening ipv6 listen socket on port 1883.
1639229562: Opening websockets listen socket on port 9000.
1639229562: mosquitto version 2.0.11 running
```

