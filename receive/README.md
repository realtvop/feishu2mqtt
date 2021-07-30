# 接收

## 配置文件格式

文件名：config.json
```json
{
    "mqtt" : {
        "server" : {
            "address" : "127.0.0.1",
            "port" : 1883
        },
    "client" : {
        "topic" : "feishuBot",
        "client_id" : "bot-reciver"
    }
    },
    "feishuBot" : {
        "app_id" : "cli_xxxx",
        "app_secret" : "xxxx",
        "app_verification_token" : "xxxx",
        "port" : 8000
    }
}
```

## MQTT格式

```json
{"msg": "{\"xxx\":\"xxx\"}", "msg_id": "xxx", "sender_union_id": "xxx"}
```

| msg                        | msg_id                                           | sender_union_id                                              |
| -------------------------- | ------------------------------------------------ | ------------------------------------------------------------ |
| 消息内容<br />格式详见下表 | Message_ID<br />消息ID，可以用于判断消息是否重复 | 发送者的Union_ID(企业内雇员ID)<br />可以用于判断发送者，以控制权限或回复消息 |

| 键值                                         | 内容                                       |
| -------------------------------------------- | ------------------------------------------ |
| 接收到的信息类型<br />如纯文本、图片、文件等 | 信息内容<br />如文本内容、图片id、文件id等 |



