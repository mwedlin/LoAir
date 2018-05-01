'''
main.py

LoAir - version 0.1

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

from network import LoRa
import ustruct
import time
import binascii
import socket
from L76GNSS import L76GNSS
from node import LoRaWANNode
from sds011 import SDS011
import config

print('Waiting for LoRa.', flush=True)
node = LoRaWANNode(config.app_eui, config.app_key, dr=config.DataRate)

#
# Find current position
#
print('Waiting for GPS.', flush=True)
l76 = L76GNSS(py, timeout=30)
coord = l76.coordinates()

if coord[0] == None: # Could not find any fixed coordinates
    coord = (0.0, 0.0)

# Take a meassurement of particle levels
print('Waiting for particle sensor.', '(', 60 - (time.ticks_ms()/1000), 'seconds )', flush=True)
time.sleep(60 - (time.ticks_ms()/1000)) # Give it a minute to settle
sds = SDS011()
particles = sds.values()

#
# Current time
#

now = rtc.now()

print("{}-{}-{} {}:{} {}, {}\n".format(now[0], now[1], now[2], now[3], now[4], coord[0], coord[1]))

txb = ustruct.pack("LllHH", utime.mktime(now),
                   int(coord[0] * 11930464),
                   int(coord[1] * 11930464),
                   particles[0], particles[1])

if not isInteractive:
    node.send(txb)
    sleep()
else:
    print('Waiting for command:')
