import random, pdb
import time, json

from paho.mqtt import client as mqtt_client


# broker = 'broker.emqx.io'
broker = 'localhost'
port = 1883
client_id = f'python-mqtt-p100'
topic = f"python/mqtt/{client_id}"
# generate client ID with pub prefix randomly
# client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'emqx'
password = 'public'

data_dic = {
    'name1':112,
    'name2': 'hello',
    'name3': 'aa为坚持',
    'name4': 23.431,
    'name5': b'YWHkuLrlnZrmjIE='
}

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    # pdb.set_trace()
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    while True:
        m = input("What to send(END for stopping):")
        if m == "END":
            client.loop_stop()
            print(f"stooped after {msg_count} messages sent - Bye.")
            break
        data = data_dic.copy()
        data["count"] = msg_count
        data['input'] = m
        jmsg = json.dumps(data)
        msg = f"message: [{msg_count}]: {jmsg}"
        # pdb.set_trace()
        payload = msg.encode('utf-8')
        result = client.publish(topic, msg)
        # result = client.publish(topic, payload)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()