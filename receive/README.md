# 配置文件格式
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