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
        UAs = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
            "User-Agent:Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "User-Agent:Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "User-Agent:Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        ]

        url = "http://www7.zzu.edu.cn/xjy/index/tzgg.htm"

        response = requests.get(url=url, headers={"User-Agent" : random.choice(UAs)})
        text = response.content.decode("utf-8", "ignore")

        # 目标数据提取
        html = etree.HTML(text)
        self.info["subject"] = "先研院发布新通知，及时查看！" # 邮件主题
        self.info["target_title"] = html.xpath("/html/body/div[4]/div[2]/div[2]/div/ul/li[1]/a/text()")[0] # 邮件内容题目；
        self.info["target_time"] = html.xpath("/html/body/div[4]/div[2]/div[2]/div/ul/li[1]/span/text()")[0] #  2022-05-26
        self.info["target_url"] = html.xpath("/html/body/div[4]/div[2]/div[2]/div/ul/li[1]/a/@href")[0].replace('..', 'http://www7.zzu.edu.cn/xjy')

        if self.info.get("target_time") == self.latest:
            print("当前未发布新通知：{}".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
            return False
        else: # 网站发生更新
            self.latest = self.info["target_time"]
            return True

    def sendWarning(self):
        # 设置邮件内容
        msg = MIMEMultipart()
        content = """
        <p>{}</p>
        <p><a href="{}">{}</a></p>
        """.format(self.info["target_title"], self.info["target_url"], self.info["target_url"])
        msg.attach(MIMEText(content, 'html','utf-8'))

        # 设置邮件主题
        msg['Subject'] = self.info["subject"]

        # 发送方
        msg['From'] = self.MSG_FROM

        # 发送邮件
        try:
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)
            s.login(self.MSG_FROM, self.AUTHORIZATION_CODE) # 登录邮箱；
            s.sendmail(self.MSG_FROM, self.MSG_TO, msg.as_string())
            print("检测到事件，邮件发送成功！")
        except smtplib.SMTPException:
            print("ERROR: 无法发送邮件！")

        # 参考文章：
        # https://blog.csdn.net/MATLAB_matlab/article/details/106240424
        # https://www.runoob.com/python3/python3-smtp.html

    def working(self):
        while True:
            if self.detect():
                self.sendWarning()
            
            # 每5分钟检测一次；
            starttime = time.time()
            while True:
                print('Next detect 倒计时: ', round(time.time() - starttime, 0), '秒', end="\r") # /r 回到行首
                time.sleep(1)
                if round(time.time() - starttime, 0) >= 300: 
                    break

if __name__ == '__main__':
    earlyWarning = EarlyWarning()
    earlyWarning.working()