import time
import paho.mqtt.client as mqtt

def text_to_bits(text):
    return ''.join(format(ord(c), '08b') for c in text)

message = ""  #add message
binary_data = text_to_bits(message)
#Append one dummy bit so that we get one extra publish
binary_data += '0'

#Define delays: short delay encodes '0', long delay encodes '1'
DELAY_ZERO = 0.1
DELAY_ONE  = 0.3

#Create MQTT client with TLS
client = mqtt.Client("TimingStegoTLSStrict")
client.tls_set(
    ca_certs="C:\\Program Files\\mosquitto\\ca.crt",
    certfile="C:\\Program Files\\mosquitto\\client.crt",
    keyfile="C:\\Program Files\\mosquitto\\client.key"
)
client.connect("localhost", 8883, 60)

#Publish one message per bit in the binary string
for bit in binary_data:
    client.publish("test", "TimingStegoStrict")
    if bit == '0':
        time.sleep(DELAY_ZERO)
    else:
        time.sleep(DELAY_ONE)

client.disconnect()
