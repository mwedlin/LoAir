'''
Configuration parameters for the LoPy client.

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

import pycom

# Known wifi networks to connect to.
known_nets = { # Change these to your own preferences
    'wedlin' : { 'pwd' : 'xxxxxxxxx' },
    'mwe on the move' : { 'pwd' : 'xxxxxx' }
}

# create an OTAA authentication parameters
app_eui = b'XXXXXXXXXXXXXXXX'

# Pycom01
app_key = b'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
# Pycom02
# app_key = app_key = b'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

# How long to sleep in DeepSleep (seconds)
# Default is 1 hour
if pycom.nvs_get('DStime') == None:
    DStime = 3600 # One hour
    pycom.nvs_set('DStime', DStime)
else:
    DStime = pycom.nvs_get('DStime')

# DataRate 0 (slowest) to 5 (fastest)
# Default to 5
if pycom.nvs_get('DataRate') == None:
    DataRate = 5
    pycom.nvs_set('DataRate', DataRate)
else:
    DataRate = pycom.nvs_get('DataRate')


# Set timezone for time referenses
# 3 hours before UTC
if pycom.nvs_get('Timezone') == None:
    Timezone = 7200
    pycom.nvs_set('Timezone', Timezone)
else:
    Timezone = pycom.nvs_get('Timezone')

