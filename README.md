### 功能
本项目用于将tg指定群组/频道的消息实时同步到微信的群聊中

### 使用步骤
#### 安装依赖

**版本**：python 3.10.0，其他版本未测试，不保证可行
```cmd
git clone 
cd 
pip install -r requirements.txt
```
#### 配置信息填写
目标：完成config.yml的信息填写
步骤：按下文逐个获取
___
目标：获取tg群组/频道对应的id
命令：**python main.py get_tg_room_id**
![](https://cdn.jsdelivr.net/gh/bainningking/pic_repo@main/img/202402231937274.png)
PS.首次使用需要填写验证信息，按说明来就行
___
目标：获取微信群聊对应的id
命令：**python main.py get_wx_room_id**
![](https://cdn.jsdelivr.net/gh/bainningking/pic_repo@main/img/202402231937277.png)
___
目标：获取tg的api_id和api_hash
命令：**python main.py api_id**
```python
1.登录网址：https://my.telegram.org.
2.进入"API development tools"填写.
3.完成后得到api_id和api_hash，填入config.yml里
PS.首次使用tg2wx 需要填写手机号，注意大陆号码需要加上+86
PPS.验证码会通过tg的官方账号通知你，填写即可，后续使用无需再验证
```
___
目标：获取本机IP
命令：**python main.py get_ip**

如果走的是其他IP的代理，自行填写，不用此命令
___
结果：
![](https://cdn.jsdelivr.net/gh/bainningking/pic_repo@main/img/202402231937278.png)

#### 启动！
命令：**python main.py tg2wx**
关闭：ctrl CCCCC