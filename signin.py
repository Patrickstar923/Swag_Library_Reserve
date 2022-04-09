'''
作者：zuoshiwen
使用说明：点击运行，再点菜单栏上的签到，要不然为空白页。如果你是河南财大的，运行此程序输入sessid，确认信息，确认签到。
        可无视距离签到，别的学校需要重新抓包修改参数即可。
'''
import tkinter as tk
from packing_func import SignUpFrame
class UserPage():
    def __init__(self,master2):
        self.user = master2
        self.user.title('签到系统')
        self.user.geometry('700x610')
        self.create_page_u()
    def create_page_u(self):
        self.sign_up_frame = SignUpFrame(self.user)
        menubar = tk.Menu(self.user)
        menubar.add_command(label='签到', command=self.show_signup)
        self.user['menu']=menubar
    def show_signup(self):
        self.sign_up_frame.pack()
if __name__ == '__main__':
    user = tk.Tk()
    UserPage(master2=user)
    user.mainloop()


