'''
作者：zuoshiwen
完成时间：2022.3.30
针对学校：理论上所有学校都支持，但需要抓包获取新的floor编号和uuid
'''
import requests
import re
import tkinter as tk
import tkinter.messagebox
class SignUpFrame(tk.Frame):#签到
    def __init__(self,user):
        super().__init__(user)
        self.usessid = tk.StringVar()
        self.create_page1()
    def create_page1(self):
        tk.Label(self).grid(row=0, pady=10)  # 网格布局
        tk.Button(self, text='确认信息', command=self.confirm_id).grid(row=4, column=2, pady=10)  # 如果函数后面带括号说明有返回值 即先运行出结果
        tk.Button(self, text='确认签到', command=self.sign).grid(row=5, column=2, pady=10)
        tk.Label(self, text='请输入您的Sessid:').grid(row=1, column=1, pady=10)
        tk.Entry(self, textvariable=self.usessid).grid(row=1, column=2, pady=20)
    def sign(self):
        sign_url = 'https://wechat.laixuanzuo.com/index.php/wxapp/sign.html'
        datas = {
            't':self.input_ID,#sessid
            'devices': '[{"uuid":"fda50693-a4e2-4fb1-afcf-c6eb07647825","major":10202,"minor":17010,"proximity":0,"accuracy":17.35089180456413,"rssi":-79}]'
        }               #更改此处uuid的值，后面参数不用改
        print(datas)
        headers = {
            'Host': 'wechat.laixuanzuo.com',
            'Connection': 'keep-alive',
            'Content-Length': '232',
            'charset': 'utf-8',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G977B Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3195 MMWEBSDK/20220105 Mobile Safari/537.36 MMWEBID/3552 MicroMessenger/8.0.19.2080(0x2800133D) Process/appbrand2 WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64 MiniProgramEnv/android',
            'content-type': 'application/x-www-form-urlencoded',
            'Accept-Encoding': 'gzip,compress,br,deflate',
            'Referer': 'https://servicewechat.com/wx8d0a841273a124b1/5/page-frame.html',

        }
        response = requests.post(url=sign_url, data=datas, headers=headers)
        print(response)
        signup_detail = response.text
        ex = 'msg":"(.*?)"'
        signup = re.findall(ex,signup_detail,re.S)
        signup_result = tkinter.messagebox.askokcancel(title='签到状态', message=signup)
        return signup_result
    def confirm_id(self):  # 获取登录账号信息
        self.user_id = self.usessid.get()
        self.input_ID= self.user_id
        return self.input_ID

