import time
import paho.mqtt.client as mqtt

#The message we want to encode:
message = ""

#Convert each character to 8-bit ASCII binary, then join
binary_data = ''.join(format(ord(c), '08b') for c in message)

#Define normal vs. 1-bit payload sizes
NORMAL_SIZE = 10
EXTRA_SIZE  = 20

#Create MQTT client with TLS
client = mqtt.Client("StegoPublisherRealmadrid")

client.tls_set(
    ca_certs="C:\\Program Files\\mosquitto\\ca.crt",
    certfile="C:\\Program Files\\mosquitto\\client.crt",
    keyfile="C:\\Program Files\\mosquitto\\client.key"
)

client.connect("localhost", 8883, 60)

#Publish each bit as a separate PUBLISH
for bit in binary_data:
    if bit == '0':
        payload_length = NORMAL_SIZE
    else:
        payload_length = EXTRA_SIZE

    payload = "X" * payload_length
    client.publish("test", payload)

    #small delay so each bit is its own TLS Application Data
    time.sleep(0.3)

client.disconnect()
