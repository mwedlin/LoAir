'''
boot.py -- run on boot-up

PyAir - version 0.1

Copyright (C) 2018  Mikael Wedlin, mwe@wedlin.pp.se

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import machine
import math
import network
import os
import time
import utime
from pytrack import Pytrack
from machine import RTC
from machine import SD
from machine import Timer

import config

# Set up garbage collection
import gc
gc.enable()

# Find reason for boot
py = Pytrack()
if py.get_wake_reason() == 2:
    isInteractive = True
else:
    isInteractive = False

# Prepare for next deepsleep
def sleep():
    print('Setting up a sleeptime of', config.DStime, 'seconds.', flush=True)
    if not isInteractive:
        py.setup_sleep(config.DStime - (time.ticks_ms()/1000))
    else:
        py.setup_sleep(config.DStime)
    py.go_to_sleep()

# Set up the sd card
try:
    sd = SD()
    os.mount(sd, '/sd')
    hasSD = True
except:
    hasSD = False

# Connect to WiFi

# Connect to wlan and stay in cmd prompt if reseted with button on pytrack
if isInteractive:
    wlan = network.WLAN(mode=network.WLAN.STA)
    available_nets = wlan.scan()
    nets = frozenset([e.ssid for e in available_nets])
    known_nets_names = frozenset([key for key in config.known_nets])
    net_to_use = list(nets & known_nets_names)
    try:
        net_to_use = net_to_use[0]
        net_properties = config.known_nets[net_to_use]
        pwd = net_properties['pwd']
        sec = [e.sec for e in available_nets if e.ssid == net_to_use][0]
        wlan.connect(net_to_use, (sec, pwd), timeout=10000)
        # Give it some time to set up
        x = 40
        while x > 0 and not wlan.isconnected():
            time.sleep(1)
            x = x - 1
    except Exception as e:
        pass
    if wlan.isconnected():
        print("Connected to "+net_to_use+" with IP address:" + wlan.ifconfig()[0])
        rtc.ntp_sync("pool.ntp.org")
        utime.sleep_ms(750)
        print('\nRTC Set from NTP to UTC:', rtc.now())
    else:
        print("Not connected to wlan.")

rtc = machine.RTC()

time.timezone(config.Timezone)
print('Adjusted from UTC to EST timezone', time.localtime(), '\n')
