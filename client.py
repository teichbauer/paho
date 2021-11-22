# -----------------------------------------------------------------------------
# Raymond Wei 2021-11-22
# --------------------
# Purpose: test out MQTT sub/pub-client with python/paho library
# --------------------
# Note: a MQTT broker(here: mosquitto) must be running on localhost
#       listening on port 1883
# --------------------
# Usage: python client.py s(ubscribe) / p(ublish) <topic>
# -----------------------------------------------------------------------------

from paho.mqtt import client as mqtt_client
from transformer import Transformer
import json, pdb, sys

# --------------------------------------------
broker = 'localhost'
port = 1883
# --------------------------------------------
D0_name = "datasource-0"    # publishing client 0
P0_name = "processor-0"     # sub/processing client 0
# --------------------------------------------
CONFIG_0 = {
    "topic_root":   "pymqtt",
    "username":     "sng-0",
    "password":     "public"
}
# --------------------------------------------

tx = Transformer()

def _on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)

def _on_message(client, userdata, msg):
    # pdb.set_trace()
    dmsg = msg.payload.decode('utf-8')[9:]
    dd = json.loads(dmsg)
    dat = tx.convert_back_msg(dd)
    ddstr = str(dat)
    # print(f"Received {jmsg} from {msg.topic}` topic")
    print(f"Received from {msg.topic}` topic:")
    print(f"{ddstr}\n")

class MQTTClient:
    def __init__(self, conf, client_id):
        self.client_id = client_id
        self.conf = conf
        self.client = mqtt_client.Client(client_id)
        self.client.username_pw_set(conf["username"], conf["password"])
        self.client.on_connect = _on_connect
        self.client.connect(broker, port)

    def subscribe(self, topic):
        the_topic = self.conf["topic_root"] + f"/{topic}"
        self.client.on_message = _on_message
        self.client.subscribe(the_topic)
        pass

    def publish(self, topic):
        the_topic = self.conf["topic_root"] + f"/{topic}"
        while True:
            m = input("What to send(END for stopping):")
            if m == "END":
                self.client.loop_stop()
                print(f"Stooped. Bye.")
                break
            data = tx.get_sample_data()
            data['input'] = m
            dat = tx.convert_msg2b64(data)
            jmsg = json.dumps(dat)
            msg = f"message: {jmsg}"
            # pdb.set_trace()
            payload = msg.encode('utf-8')
            result = self.client.publish(the_topic, msg)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")

if __name__ == '__main__':
    # argv is the list of input strings (delimitted by space)
    argv = sys.argv  # [0]: "client.py", [1]: "s"/"p", [2]: "<topic>"
    if len(argv) < 3:
        print("usage: python client.py s(ubscribe) / p(ublish) <topic>")
    else:
        # first letter of "s" / "subscribe", or "p" | "publish"
        # should be 's' or 'p'
        client_type = argv[1][0]  # 's' or 'p'
        topic = argv[2]
        if client_type == 's':
            end_point = MQTTClient(CONFIG_0, f"id-{client_type}")
            end_point.subscribe(topic)
            end_point.client.loop_forever()
        elif client_type == 'p':
            end_point = MQTTClient(CONFIG_0, f"id-{client_type}")
            end_point.publish(topic)
            end_point.client.loop_start()
        else:
            print("usage: python client.py s|p <topic>")
