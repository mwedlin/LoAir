'''
	Reading particle meassurmets with SDS011

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

from machine import UART
import struct

class SDS011:

    def __init__(self, uart=1, rxpin='P11'):
        self.uart = uart
        self.rxpin = rxpin
        self._hasValues = False
        self._uart = UART(uart, pins=(None, rxpin))

    @property
    def has_values(self):
        return self._hasValues

    def values(self):
        b = self._uart.readall() #Empty the uart buffer
        while True:
            while self._uart.read(1) != b'\xaa': # Wait for packet start
                pass
            if self._uart.read(1) != b'\xc0': # Should be C0
                continue
            b = self._uart.read(7) # Data + checksum
            if self._uart.read(1) != b'\xab': # Tail
                continue
            s = struct.unpack('BBBBBBB', b) # Check the checksum
            sum = s[0]+s[1]+s[2]+s[3]+s[4]+s[5]
            if sum % 256 != s[6]:
                continue
            return struct.unpack('<HHBB', b) # (PM2.5x10, PM10x10, ID1, ID2)
