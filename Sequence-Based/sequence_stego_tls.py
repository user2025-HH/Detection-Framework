import time
import paho.mqtt.client as mqtt

def text_to_bits(text):
    return ''.join(format(ord(c), '08b') for c in text)

message = ""  #add message
binary_data = text_to_bits(message)

#Choose size
SIZE_MSG1 = 50
SIZE_MSG2 = 70

client = mqtt.Client("SequenceStegoTLS")
client.tls_set(
    ca_certs="C:\\Program Files\\mosquitto\\ca.crt",
    certfile="C:\\Program Files\\mosquitto\\client.crt",
    keyfile="C:\\Program Files\\mosquitto\\client.key"
)
client.connect("localhost", 8883, 60)

topic = "test"

for bit in binary_data:
    payload_small = "X" * SIZE_MSG1
    payload_large = "X" * SIZE_MSG2
    if bit == '0':
        #normal order => small, then large
        client.publish(topic, payload_small)
        time.sleep(0.1)
        client.publish(topic, payload_large)
    else:
        #swapped => large, then small
        client.publish(topic, payload_large)
        time.sleep(0.1)
        client.publish(topic, payload_small)

    time.sleep(0.2)

client.disconnect()
