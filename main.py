import os
import sys
import asyncio
import socket
from threading import Thread
from time import sleep
from pyrogram import Client
from wcferry import Wcf
import yaml
import datetime

ENVIRONMENT = os.environ.get('ENVIRONMENT')
config_yml = 'config_dev.yml' if ENVIRONMENT == 'development' else 'config.yml'
# 读取YAML配置信息
with open(config_yml, 'r') as stream:
    try:
        config = yaml.safe_load(stream)

        # 访问配置信息
        tg_room_id = config['tg_room_id']
        wx_room_id = config['wx_room_id']
        proxy_ip = config['proxy_ip']
        api_id = config['api_id']
        api_hash = config['api_hash']
        proxy_port = config['proxy_port']

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
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
        return ip


async def get_tg_room_id():
    # 登录手机号需要加上+86
    app = Client("tg_client", api_id=api_id, api_hash=api_hash, proxy={
        'scheme': "socks5", 'hostname': proxy_ip, 'port': proxy_port})
    async with app:
        # 获取tg频道/群聊id
        async for dialog in app.get_dialogs():
            print(dialog.chat.title or dialog.chat.first_name)
            print(dialog.chat.id)


async def tg2wx():
    # 登录手机号需要加上+86
    app = Client("tg_client", api_id=api_id, api_hash=api_hash, proxy={
        'scheme': "socks5", 'hostname': proxy_ip, 'port': proxy_port})
    wcf = Wcf()
    async with app:
        # 通过tg账号获取消息
        new_msg_time = datetime.datetime.now()
        while True:
            async for message in app.get_chat_history(chat_id=tg_room_id, limit=1):
                    if message.date>new_msg_time:
                        try:
                            tg_txt = message.caption if message.caption else message.text
                            # print(tg_txt)
                            wcf.send_text(msg=tg_txt, receiver=wx_room_id)
                            new_msg_time = message.date
                        except Exception as e:
                            print(e)


def get_wx_room_id():
    # 获取微信群聊id
    print('请用手机向目标群聊发送群消息，通过下面输出的内容得到对应的room_id，格式为 “群聊id 群聊消息”，注意识别自己发送消息所对应的id')
    print('按ctrl C退出')
    wcf = Wcf(debug=True)
    wcf.enable_receiving_msg()

    def innerProcessMsg(wcf: Wcf):
        while wcf.is_receiving_msg():
            try:
                msg = wcf.get_msg()
                print(msg.roomid+'  '+msg.content, end='\n')
            except Exception as e:
                sleep(2)
    Thread(target=innerProcessMsg, name="GetMessageContent",
           args=(wcf,), daemon=True).start()
    wcf.keep_running()


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <argument>")
        return

    argument = sys.argv[1]

    if argument == "tg2wx":
        asyncio.run(tg2wx())
    elif argument == "get_wx_room_id":
        get_wx_room_id()
    elif argument == "get_tg_room_id":
        asyncio.run(get_tg_room_id())
    elif argument == "api_id":
        print("""如何获取tg的api_id和api_hash？
              1.登录网址：https://my.telegram.org.
              2.进入"API development tools"填写.
              3.完成后得到api_id和api_hash，填入config.yml里
              PS.首次使用tg2wx 需要填写手机号，注意大陆号码需要加上+86
              PPS.验证码会通过tg的官方账号通知你，填写即可，后续使用无需再验证
              """)
    elif argument == "get_ip":
        host_ip = get_host_ip()
        print(f'本机IP地址为{host_ip}', end='\n')
    else:
        print("Invalid argument")


if __name__ == "__main__":
    print('请确保config.yml已全部填写，请确保微信版本是3.9.2.23，否则无法正常使用')
    main()
