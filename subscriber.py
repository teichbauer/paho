import random, pdb, json

from paho.mqtt import client as mqtt_client


# broker = 'broker.emqx.io'
broker = 'localhost'
port = 1883
topic = "python/mqtt/#"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-S100'
username = 'emqx'
password = 'public'
limit = 10


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        global limit
        pdb.set_trace()
        jmsg = msg.payload.decode('utf-8')
        dd = json.loads(jmsg)
        ddstr = str(dd)
        # print(f"Received {jmsg} from {msg.topic}` topic")
        print(f"Received {ddstr} from {msg.topic}` topic")
        limit -= 1
        print(f"limit: {limit}")
        if limit == 0:
            print(f"subscriber has enough. Stopped")
            mqtt_client.loop_stop()

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
    # client.loop_start()


if __name__ == '__main__':
    run()