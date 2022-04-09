'''
作者：zuoshiwen
邮箱：2580518100@qq.com
使用说明：本程序为今日预约，输入sessid，随机分配楼层座位。如想选择指定座位 请更改 floor = random_floor；
        data_key =random_datakey；例如改成 floor ='10000' data_key ='8,11'

'''
import requests
import re
import urllib3
import ddddocr
from random import choice
from jscode import js_code,js_yzm
urllib3.disable_warnings()
input_ID =input('请输入你的sessid：')
main_page_url ='https://wechat.laixuanzuo.com/index.php/reserve/index.html'
headers = {
            'Cookie':'wechatSESS_ID='+str(input_ID)+''
}
response = requests.get(url=main_page_url,headers=headers)
main_page_detail =response.text
ex2 = '<a href="javascript:;" data-url="/index.php/reserve/layout/libid=(.*?).html.*?<h4 class="list-group-item-heading">.*?<span class="badge.*?>(.*?)/'#匹配3位或2位或1位数字
seat_status = re.findall(ex2,main_page_detail,re.S)#利用正则匹配出当前有空余座位的楼层,此时0也被取出来了
new_seat_status = []#提前定义new_seat_status
#0代表已满，所以将含零的楼层删去，选择非0，所以做循环判断
for i in seat_status:
    if (str(i)[11:12])!='0' and (str(i)[11:17])!='close<':#此处for循环变成了元组类型（不可变），所以将其变成字符串
        new_seat_status.append(i)#将遍历结果封装到一个newlist中
select_floor= choice(new_seat_status)
random_floor= str(select_floor)[2:7]
print('随机楼层为:',random_floor)
floor = random_floor #修改此处成为手动模式
floor_url = 'https://wechat.laixuanzuo.com/index.php/reserve/layout/libid=+'+floor+'+.html'
headers = {
    'Cookie': 'wechatSESS_ID=' + input_ID + '',
    'Referer':'https://wechat.laixuanzuo.com/index.php/reserve/index.html?f=wechat'

}
floor_page = requests.get(url=floor_url, headers=headers).text
ex = '<script src="https://static.wechat.laixuanzuo.com/template/theme2/cache/layout/(.*?).js"></script>'
js_before = str(re.findall(ex, floor_page, re.S))[2:-2]
js_after = js_code[js_before]
ex9 = '<div class="grid_cell grid_1".data-key="(.*?)".style'#利用正则获取剩余座位的data_key
re_datakey = re.findall(ex9,floor_page,re.S)
random_datakey = choice(re_datakey)
print('随机座位为:',random_datakey)
data_key =random_datakey

confirm_url = 'https://wechat.laixuanzuo.com/index.php/reserve/get/libid='+floor+'&'+js_after+'='+data_key+'&yzm='

confirm_headers = {
    'Referer': 'https://wechat.laixuanzuo.com/index.php/reserve/layout/libid=+' + floor + '.html&',
    'Cookie':'wechatSESS_ID=' + input_ID + '',
    }
confirm_page_detail = requests.get(url=confirm_url,headers=confirm_headers).text
print(confirm_page_detail)
if '"code":1000' in confirm_page_detail:
    headers = {
        'Cookie': 'wechatSESS_ID=' +input_ID + ''
    }
    img_data = requests.get('https://wechat.laixuanzuo.com/index.php/misc/verify', headers=headers, verify=False,allow_redirects=False)
    a = img_data.headers
    yzm_ct = img_data.content
    if 'Location' in a.keys():
        print("重定向")
        img_url = a.pop('Location')  # pop传入键 返回值 并删除键值对
        rd_img = requests.get(url=img_url).content
        ocr = ddddocr.DdddOcr(old=True)
        after_deal_yzm = ocr.classification(rd_img)
        after_deal_yzm = after_deal_yzm.replace('o', '0')
        print('验证码识别结果为:',after_deal_yzm)
    else:
        ocr = ddddocr.DdddOcr(old=True)
        after_deal_yzm = ocr.classification(yzm_ct)
        after_deal_yzm = after_deal_yzm.replace('o', '0')
        print('验证码识别结果为:', after_deal_yzm)
    yzm_headers = {
        'Referer': 'https://wechat.laixuanzuo.com/index.php/reserve/layout/libid=' + floor + '.html',
        'Cookie': 'wechatSESS_ID=' +input_ID + ''
    }
    final_result = requests.get('https://wechat.laixuanzuo.com/index.php/reserve/get/libid='+floor+'&'+js_after+'=' +data_key+ '&yzm='+after_deal_yzm+'', headers=yzm_headers).text
    print(final_result)
    while '"code":1000' in final_result:
        print('进入循环请求验证码')
        reget_img = requests.get('https://wechat.laixuanzuo.com/index.php/misc/verify', headers=headers, verify=False,
                                 allow_redirects=False).content
        ocr = ddddocr.DdddOcr(old=True)
        after_deal_yzm = ocr.classification(reget_img)
        after_deal_yzm = after_deal_yzm.replace('o', '0')
        print('识别结果为:', after_deal_yzm)
        yzm_headers = {
            'Referer': 'https://wechat.laixuanzuo.com/index.php/reserve/layout/libid=' + floor + '.html',
            'Cookie': 'wechatSESS_ID=' + input_ID + ''
        }
        final_result = requests.get(
            'https://wechat.laixuanzuo.com/index.php/reserve/get/libid=' + floor + '&' + js_after + '=' + data_key + '&yzm=' + after_deal_yzm + '',
            headers=yzm_headers).text
        print(final_result)