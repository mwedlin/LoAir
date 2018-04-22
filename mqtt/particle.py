import paho.mqtt.client as mqtt
import json
import pprint
import sys

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Counter\tPort\tCoding Rate\tData Rate\tFrequency\tTime\tLatitude\tLongitude\t2.5 um\t10 um\tGateway\tGtw latitude\tGtw longitude\tGtw Channel\tGtw rf chain\tGtw rssi\tGtwsnr")
    sys.stdout.flush()

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # ***** Change this to match your setup *****
    client.subscribe("myposition/devices/pycom01/up")

pp = pprint.PrettyPrinter(indent=2)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    try:
        print(str(data['counter']) + "\t" + 
              str(data['port']) + '\t' +
              data['metadata']['coding_rate'] + '\t' +
              data['metadata']['data_rate'] + '\t' +
              str(data['metadata']['frequency']) + '\t' +
              data['metadata']['time'] + '\t' +
              str(data['payload_fields']['lat']) + '\t' +
              str(data['payload_fields']['lon']) + '\t' +
              str(data['payload_fields']['pm25']) + '\t' +
              str(data['payload_fields']['pm10']) + '\t' +
              data['metadata']['gateways'][0]['gtw_id'] + '\t' +
              str(data['metadata']['gateways'][0]['latitude']) + '\t' +
              str(data['metadata']['gateways'][0]['longitude']) + '\t' +
              str(data['metadata']['gateways'][0]['channel']) + '\t' +
              str(data['metadata']['gateways'][0]['rf_chain']) + '\t' +
              str(data['metadata']['gateways'][0]['rssi']) + '\t' +
              str(data['metadata']['gateways'][0]['snr']))
    except:
        pass

    sys.stdout.flush()
 

    # pp.pprint(data)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Change theese to your credentials (Application name, default key)
client.username_pw_set('myposition', '')
client.connect("eu.thethings.network", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
