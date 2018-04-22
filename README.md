# LoAir
LoPy interface to the particle concentration sensor SDS011.
This is a poorly documented development version and I would strongly suggest that is is only used as a template for your own experimentation.

-- Warning --

First a short warning. This is code under development and not intended for a production environment. It has none of the security meassures that is needed for that and all codes and passwords put in the files are trivially obtainable. You have been warned.

-- Hardware --

The base of LoAir is a LoPy4 (https://pycom.io/product/lopy4/) on top of a Pytrack (https://pycom.io/product/pytrack/) expansion board.
The SDS011 is fed 5V from a 3.3V to 5V board, PowerBoost 1000 Basic (https://www.adafruit.com/product/2030). Connect "Bat" to 3V3_Sensors on Pytrack.
The last connection is the TX output pin on SDS011 that should be connected to EXT_IO3 on Pytrack.

-- Lib --

Find the following Libraris fron the lopy github and put them in /flash/lib:

L76GNSS.py

LIS2HH12.py

pycoproc.py

pytrack.py

Copy the following libs from this github (directory lopy) to /flash/lib:

node.py

SDS011.py

-- Client --

The rest of the files in directory lopy should be copied to /flash.
All configuration is put in file config.py. Dont forget to update these before copying this file. Boot.py and main.py is the main program as usual.

The client wakes up regulary, sends a value and goes back to deepsleep. To wake it for reconfiguration just wake it with the Pytrack button. It will connect to any configured wifi and stay in command mode on the USB UART. To restart it again just give it the command sleep() at the command prompt.

To change the sleep time go into command mode and send the following:

import pycom

pycom.mvs_set('DStime', x)

where x is the number of seconds you want between the meassurements.

-- TTN payload format --

Use this code in the TTN console PayloadFormat:

function Decoder(bytes, port) {

  // Decode an uplink message from a buffer

  // (array) of bytes to an object of fields.

  var decoded = {};

  // if (port === 1) decoded.led = bytes[0];

  var time = new Date((bytes[3] << 24 | bytes[2] << 16 | bytes[1] << 8 | bytes[0]) * 1000);

  var lat = (bytes[7] << 24 | bytes[6] << 16 | bytes[5] << 8 | bytes[4]) / 11930464

  var lon = (bytes[11] << 24 | bytes[10] << 16 | bytes[9] << 8 | bytes[8]) / 11930464


  decoded.time = time.toString();

  decoded.lon = lon;

  decoded.lat = lat;

  
  // Check for particle sensor data

  if (bytes.length >= 16) {

    var pm25 = (bytes[13] << 8 | bytes[12]) / 10;

    var pm10 = (bytes[15] << 8 | bytes[14]) / 10;
    
    decoded.pm25 = pm25;

    decoded.pm10 = pm10;

  }
  
  return decoded;

}

-- MQTT client --

To subscribe to the data with paho you can look in the file mqtt/particle.py

