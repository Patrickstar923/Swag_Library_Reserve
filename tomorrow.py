'''
作者：zuoshiwen
b站:UID:383391954
邮箱：2580518100@qq.com
使用说明：请手动更改 cookie = np.array(['c1dfda58fbf27a4a824a7b14c6e6db8c','10000','8,11'])里的数值，参数一为sessid，参数二为楼层编号，参数三为具体座位
'''
import requests
import re
import urllib3
import time
import ddddocr
import numpy as np
from jscode import js_yzm,js_code
urllib3.disable_warnings()
start = time.time()
cookie = np.array(['61deecf5b00e193e254645545bea3bbd','10000','8,11'])
floor_url = 'https://wechat.laixuanzuo.com/index.php/reserve/layoutApi/action=prereserve_event&libid=' + cookie[1] + ''
headers = {
    'Cookie': 'wechatSESS_ID=' + cookie[0] + ''
}
floor_page = requests.get(url=floor_url, headers=headers).text
ex = '<script src="https://static.wechat.laixuanzuo.com/template/theme2/cache/layout/(.*?).js"></script>'
try:
    js_before = str(re.findall(ex, floor_page, re.S))[2:-2]
    js_after = js_code[js_before]
    # 获取验证码
    img_data = requests.get('https://wechat.laixuanzuo.com/index.php/misc/verify', headers=headers, verify=False,allow_redirects=False).headers
    img_data = str(img_data)
    ex_yzm = 'theme2/cache/yzm/(.*?).jpg'  # 重定向验证码
    yzm_code = str(re.findall(ex_yzm, img_data, re.S))[2:-2]
    get_yzm = js_yzm[yzm_code]
    print("对应验证码为:",get_yzm)
    yzm_headers = {
        'Referer': 'https://wechat.laixuanzuo.com/index.php/reserve/layoutApi/action=prereserve_event&libid=' + cookie[1] + '',
        'Cookie': 'wechatSESS_ID=' + cookie[0] + ''
    }
    final_result = requests.get('https://wechat.laixuanzuo.com/index.php/prereserve/save/libid=' + cookie[1] + '&' +js_after+ '=' + cookie[2] + '&yzm=' + get_yzm + '', headers=yzm_headers).text
    print(final_result)
    end = time.time()
    print('选座用时:%ss' % (round(end - start, 2)))
except:
    js_before = str(re.findall(ex, floor_page, re.S))[2:-2]
    js_after = js_code[js_before]
    headers = {
        'Cookie':'wechatSESS_ID='+cookie[0]+''
    }
    img_data = requests.get('https://wechat.laixuanzuo.com/index.php/misc/verify', headers=headers,verify=False,allow_redirects=False)
    a = img_data.headers
    yzm_ct = img_data.content
    if 'Location' in a.keys():
        print("重定向")
        img_url = a.pop('Location')#pop传入键 返回值 并删除键值对
        rd_img = requests.get(url=img_url).content
        ocr = ddddocr.DdddOcr(old=True)
        after_deal_yzm = ocr.classification(rd_img)
        after_deal_yzm = after_deal_yzm.replace('o', '0')
        print('识别结果为:', after_deal_yzm)
    else:
        ocr = ddddocr.DdddOcr(old=True)
        after_deal_yzm = ocr.classification(yzm_ct)
        after_deal_yzm = after_deal_yzm.replace('o', '0')
        print('识别结果为:', after_deal_yzm)
    yzm_headers = {
            'Referer':'https://wechat.laixuanzuo.com/index.php/reserve/layoutApi/action=prereserve_event&libid='+cookie[1]+'',
            'Cookie': 'wechatSESS_ID=' + cookie[0] + ''
    }
    final_result = requests.get('https://wechat.laixuanzuo.com/index.php/prereserve/save/libid='+cookie[1]+'&'+js_after+'='+cookie[2]+'&yzm='+after_deal_yzm+'', headers=yzm_headers).text
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
            'Referer': 'https://wechat.laixuanzuo.com/index.php/reserve/layoutApi/action=prereserve_event&libid=' +
                       cookie[1] + '',
            'Cookie': 'wechatSESS_ID=' + cookie[0] + ''
        }
        final_result = requests.get(
            'https://wechat.laixuanzuo.com/index.php/prereserve/save/libid=' + cookie[1] + '&' + js_after + '=' +
            cookie[2] + '&yzm=' + after_deal_yzm + '', headers=yzm_headers).text
        print(final_result)
    end =time.time()
    print('选座用时:%ss'%(round(end-start,2)))
    input()


