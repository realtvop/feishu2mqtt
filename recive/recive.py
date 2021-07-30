###CONFIG###
import json
configfile = open("config.json",)
config = json.load(configfile)
mqttconfig = config["mqtt"]
feishubotconfig = config["feishuBot"]

###MQTT###
# python 3.6

import random
import time

from paho.mqtt import client as mqtt_client


broker = mqttconfig["server"]["address"]   #服务器
port = mqttconfig["server"]["port"]            #端口
topic = mqttconfig["client"]["topic"]         #频道
client_id = mqttconfig["client"]["client_id"]    #连接id


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client, message):
    result = client.publish(topic, message)
    return result[0]


def client():
    client = connect_mqtt()
    client.loop_start()
    return client

###处理###
import json
def json2send(message):
    messages = json.loads(message)
    returns = {
        "msg" : messages["event"]["message"]["content"],
        "msg_id" : messages["event"]["message"]["message_id"],
        "sender_union_id" : messages["event"]["sender"]["sender_id"]["union_id"]
    }
    return json.dumps(returns)

###MQTT_CLIENT###
mqttclient = client()

###Feishu###
from http.server import BaseHTTPRequestHandler, HTTPServer
from os import path
import json
from urllib import request, parse


APP_ID = feishubotconfig["app_id"]
APP_SECRET = feishubotconfig["app_secret"]
APP_VERIFICATION_TOKEN = feishubotconfig["app_verification_token"]

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 解析请求 body
        req_body = self.rfile.read(int(self.headers['content-length']))
        obj = json.loads(req_body.decode("utf-8"))
        print(req_body)
        publish(mqttclient, json2send(req_body))
    

def feishuBotStart():
    port = feishubotconfig["port"]  #端口
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print("start.....")
    httpd.serve_forever()

#用法
feishuBotStart()