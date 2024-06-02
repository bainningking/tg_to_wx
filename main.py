import asyncio
import os
import socket
import sys

import yaml
from pyrogram import Client, filters

from lib import itchat

ENVIRONMENT = os.environ.get("ENVIRONMENT")
config_yml = "config_dev.yml" if ENVIRONMENT == "development" else "config.yml"
# 读取YAML配置信息
with open(config_yml, "r", encoding='utf-8') as stream:
    try:
        config = yaml.safe_load(stream)

        # 访问配置信息
        tg_room_id = config["tg_room_id"]
        wx_room_name = config["wx_room_name"]
        proxy_ip = config["proxy_ip"]
        api_id = config["api_id"]
        api_hash = config["api_hash"]
        proxy_port = config["proxy_port"]

    except yaml.YAMLError as exc:
        print(exc)


# 获取本机IP，因HDCP是动态分配IP给本机，所以代理的IP地址也会变
def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
        print("局域网IP为{}".format(ip))
        return ip


async def get_tg_room_id():
    # 登录手机号需要加上+86
    app = Client(
        "tg_client",
        api_id=api_id,
        api_hash=api_hash,
        proxy={"scheme": "socks5", "hostname": proxy_ip, "port": proxy_port},
    )
    async with app:
        # 获取tg频道/群聊id
        async for dialog in app.get_dialogs():
            print(dialog.chat.title or dialog.chat.first_name)
            print(dialog.chat.id)


def sent_chatroom_msg(name, context):
    userName = name
    iRoom = itchat.search_chatrooms(name)
    for room in iRoom:
        if room["NickName"] == name:
            userName = room["UserName"]
            break
    itchat.send_msg(context, userName)


def tg2wx():
    # 登录手机号需要加上+86
    app = Client(
        "tg_client",
        api_id=api_id,
        api_hash=api_hash,
        proxy={"scheme": "socks5", "hostname": proxy_ip, "port": proxy_port},
    )
    itchat.auto_login()
    itchat.get_chatrooms(update=True)

    @app.on_message(filters.chat(tg_room_id))
    def handle_messages(client, message):
        tg_txt = message.caption if message.caption else message.text
        # print(tg_txt)
        sent_chatroom_msg(name=wx_room_name, context=tg_txt)

    app.run()


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <argument>")
        return

    argument = sys.argv[1]

    if argument == "tg2wx":
        tg2wx()
    elif argument == "get_tg_room_id":
        asyncio.run(get_tg_room_id())
    elif argument == "api_id":
        print(
            """如何获取tg的api_id和api_hash？
              1.登录网址：https://my.telegram.org.
              2.进入"API development tools"填写.
              3.完成后得到api_id和api_hash，填入config.yml里
              PS.首次使用tg2wx 需要填写手机号，注意大陆号码需要加上+86
              PPS.验证码会通过tg的官方账号通知你，填写即可，后续使用无需再验证
              """
        )
    elif argument == "get_ip":
        host_ip = get_host_ip()
        print(f"本机IP地址为{host_ip}", end="\n")
    else:
        print("Invalid argument")


if __name__ == "__main__":
    main()
