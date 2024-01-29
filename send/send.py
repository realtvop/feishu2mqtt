###CONFIG###
import json
configfile = open("config.json",)
config = json.load(configfile)
mqttconfig = config["mqtt"]
feishubotconfig = config["feishuBot"]

###Feishu###
from http.server import BaseHTTPRequestHandler, HTTPServer
from os import path
import json
from urllib import request, parse


APP_ID = feishubotconfig["app_id"]
APP_SECRET = feishubotconfig["app_secret"]
APP_VERIFICATION_TOKEN = feishubotconfig["app_verification_token"]

def get_tenant_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
    headers = {
        "Content-Type" : "application/json"
    }
    req_body = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }
    data = bytes(json.dumps(req_body), encoding='utf8')
    req = request.Request(url=url, data=data, headers=headers, method='POST')
    try:
        response = request.urlopen(req)
    except Exception as e:
        print(e.read().decode())
        return ""
    rsp_body = response.read().decode('utf-8')
    rsp_dict = json.loads(rsp_body)
    code = rsp_dict.get("code", -1)
    if code != 0:
        print("get tenant_access_token error, code =", code)
        return ""
    return rsp_dict.get("tenant_access_token", "")

def send_message(union_id, text):
        url = "https://open.feishu.cn/open-apis/message/v4/send/"

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + get_tenant_access_token()
        }
        req_body = {
            "union_id": union_id,
            "msg_type": "text",
            "content": {
                "text": text
            }
        }

        data = bytes(json.dumps(req_body), encoding='utf8')
        req = request.Request(url=url, data=data, headers=headers, method='POST')
        try:
            response = request.urlopen(req)
        except Exception as e:
            print(e.read().decode())
            return

        rsp_body = response.read().decode('utf-8')
        rsp_dict = json.loads(rsp_body)
        code = rsp_dict.get("code", -1)
        if code != 0:
            print("send message error, code = ", code, ", msg =", rsp_dict.get("msg", ""))

###MQTT###
# python3.6

from paho.mqtt import client as mqtt_client


broker = mqttconfig["server"]["address"]   #服务器
port = mqttconfig["server"]["port"]            #端口
topic = mqttconfig["client"]["topic"]         #频道
client_id = mqttconfig["client"]["client_id"]    #连接id


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(msg.payload.decode())              #收到的消息
        msglist = json.loads(msg.payload.decode())
        send_message(msglist["user_union_id"], msglist["text"])
    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()