# course

[mqtt course link](https://munier.perso.univ-pau.fr/tutorial/iot/2022/20220510-mqtt_python/)

# mandatory commands

apt update
apt install -y python3{-pip,-tk}
pip3 install --upgrade pip
pip3 install paho-mqtt

# broker

test.mosquito.org

# notes

2 VMs, pour montrer quelles peuvent communiquer

```python
import random
from paho.mqtt import client as mqtt_client

broker = 'test.mosquitto.org'
port = 1883
topic = "/adehu"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
```

