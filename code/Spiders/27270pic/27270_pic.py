
# _*_ coding:utf-8 _*_
#__author__ :choupiMao
import requests
import re
import time

tag_url = 'http://www.27270.com/ent/meinvtupian/list_11_2.html'

def get_img_url(result):
    for item in result:
        response = requests.get(item)
        response.encoding = 'gb2312'
        page_num = re.findall(r'<li class="hide" pageinfo="(.*?)" id="pageinfo">',response.text)
        page = int(page_num[0])

        for i in range(1,page+1):
            url = '_'+str(i)+'.html'
            new_url = item.replace('.html',url)
            headers = {"User-Agent":'BaiduSpider'}
            response_pic = requests.get(new_url,headers = headers)
            response_pic.encoding = 'gb2312'

            pic_url = re.findall(r'<img alt=".*?"  src="(.*?)" />',response_pic.text)
            pic_url = pic_url[0]
            bytes = requests.get(pic_url)
            name = pic_url[-13::]
            print("./imags/"+name)
            f = open("./imags/"+name,'wb')
            f.write(bytes.content)
            f.flush()
            f.close()
            time.sleep(0.1)

for i in range(1,175):
    full_url = 'http://www.27270.com/ent/meinvtupian/list_11_'+str(i)+'.html'
    # print(full_url)
    response = requests.get(full_url)
    response.encoding = 'gb2312'

    pattern = re.compile(r'<a href="(.*?)" title=".*?" class="MMPic"')
    result = pattern.findall(response.text)
    get_img_url(result)
