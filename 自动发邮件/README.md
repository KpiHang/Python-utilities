## 预警机
事件检测 + 预警（自动发QQ邮件提醒）

```python
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, os
import requests, random, time
from lxml import etree

# 系统变量
# MSG_FROM : 发送方邮箱账号；
# MSG_TO : 接收方邮箱账号；
# AUTHORIZATION_CODE : 邮件登录密码；

class EarlyWarning:
    """
    EarlyWarning : 预警机（检测事件 + 发送提醒）；
    Func detect() -> bool, Info: 监测到事件后返回true, 和发送信息；
    Func sendWarning() : 发送提醒；
    """
    def __init__(self) -> None:
        self.MSG_FROM = os.getenv('MSG_FROM')
        self.MSG_TO = os.getenv('MSG_TO')
        self.AUTHORIZATION_CODE = os.getenv('AUTHORIZATION_CODE')
        self.latest = "" # 记录最新通知的时间
        self.info = {} # 记录更新主要内容
        
    def detect(self):
        # 事件监测，因人而异，因需而异；
    def sendWarning(self): # 一般不变动
    def working(self): # 一般不变动
```

## 部署开启
代码放到服务器上，包括Pipfile，用pipenv重建环境；

同时设置环境变量！

后台运行：
```bash
nohup python autoQQemail.py > autoQQemail.log 2>&1 &
```
这里有一点没写好，代码里的都是print，不是输出到终端，所以日志记录还没实现好。

## 计时器功能
```python
# 每5分钟检测一次；
starttime = time.time()
while True:
    print('Next detect 倒计时: ', round(time.time() - starttime, 0), '秒', end="\r") # /r 回到行首
    time.sleep(1)
    if round(time.time() - starttime, 0) >= 300: 
        break
```