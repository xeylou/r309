#!/usr/bin/python3
import random, time 
from paho.mqtt import client as mqtt_client


# identification

wanted_broker_link = 'test.mosquitto.org'
wanted_broker_port = 1883
wanted_topic = "/adehu"
client_id = f'python-mqtt-{random.randint(0, 1000)}'


# connexion

def broker_connexion() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"[SUCCESS] Connected to broker {wanted_broker_link}:{wanted_broker_port}")
        else:
            print(f"[FATAL] Failed to connect to broker {wanted_broker_link}:{wanted_broker_port}, return code {rc}")

        client = mqtt_client.Client(client_id)
        client.on_connect = on_connect
        client.connect(broker, port)
        return client


# publication

def publish_to_broker(client):
    payload = "testing_message"

    time.sleep(1)
    publish_log = client.publish(topic, payload) # result: [0, 1]
    state = result[0]

    if state == 0:
        print(f"[SUCESS] `{payload}` sended to the topic `{wanted_topic}`")
    else:
        print(f"[ERROR] Failed to send {payload} to the topic {wanted_topic}")


# subscription

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        tmp = str(msg.payload.decode("utf-8"))
        print(f"[SUCCESS] Received `{tmp}` from topic `{msg.wanted_topic}`")

    client.subscribe(wanted_topic)
    client.on_message = on_message


# execution

def run():
    client = broker_connexion()
    subscribe(client)
    client.loop_forever()
    client.loop_start()
    publish_to_broker(client)

if __name__ == '__main__':
    run()