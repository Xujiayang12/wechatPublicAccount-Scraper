# ------------------------------------------------------------------------------------------------------------------------
# 事先得在mysql里面建好表test1(id,title,date,content,url)，并且把字段设置为utf8，这里数据库名为TESTDB，表名为test1
# ------------------------------------------------------------------------------------------------------------------------
from datetime import datetime
import requests
import random
import time
import re
from bs4 import BeautifulSoup
import pymysql

######请在这里填入数据库密码########

password = "XXXXXX";

###########################

########输入爬取总页面地址#########这个地址是搜狗微信搜索，搜那个公众号的那个链接

allurl = "http://weixin.sogou.com/weixin?type=1&s_from=input&query=it%E4%B9%8B%E5%AE%B6&ie=utf8&_sug_=n&_sug_type_="

################################


db = pymysql.connect("localhost", "root", password, "TESTDB", charset="utf8")  # 注意设置为utf8
cursor = db.cursor()
cursor.execute("SELECT * FROM test1")
results = cursor.fetchall()
idlist = []  # 取出所有的ID号
print("数据库里面存放的所有文章id：")
for i in results:
    idlist.append(i[0])
    print(str(i[0]) + " ")

# 请求头用诺基亚N9
header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'mp.weixin.qq.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (MeeGo; NokiaN9) AppleWebKit/534.13 (KHTML, like Gecko) NokiaBrowser/8.5.0 Mobile Safari/534.13'
}


def getsurl(link):  # 获取最新的历史消息页面链接
    html = requests.get(url=link)
    source = html.content
    page = BeautifulSoup(source, 'html.parser')
    url = page.find('a', uigs="account_image_0")['href'].replace('amp;', '')
    return url


def getdetail(url):
    html = requests.get(url=url, headers=header)
    source = html.content
    page = BeautifulSoup(source, 'html.parser')
    title = page.find('title').text
    date = page.find('em', id='post-date').text
    content = page.find('div', id='js_content').text.replace('\xa0', ' ').replace('\u3000', ' ')
    # 本来想保留标签的，但是mysql不能存奇怪的符号，不然会报错
    detail = {'title': title, 'date': date, 'content': content}
    print(detail['title'])
    return detail


def geturl(surl):
    html = requests.get(url=surl, headers=header)
    source = html.content
    page = BeautifulSoup(source, 'html.parser')
    scripts = page.find_all('script', type="text/javascript")  # 提取出javacript部分，方便解析
    js = re.findall(r'var msgList = (.*?);\n        seajs.use\("sougou/profile\.js"\);', scripts[6].text)  # 找到json部分
    try:
        links = re.findall(r'"content_url":"(.*?)"', js[0])  # 找到所有链接部分
        ids = re.findall(r'"id":(.*?),"status"', js[0])  # json里面附有唯一id号
    except:
        print("出现验证码，需要手动上网打开以下网址填写一次验证码,然后重新运行脚本：")
        print(surl)
        return

    print("最新文章id" + str(ids))
    for link, id in zip(links, ids):
        if int(id) in idlist:  # 不抓重复的
            continue
        else:
            print("正在抓取" + id + "文章")
            link2 = "https://mp.weixin.qq.com" + link.replace("amp;", "")  # 去掉恶心的干扰
            detail = getdetail(link2)
            title = detail['title']
            date = detail['date']
            content = detail['content']
            try:
                cursor.execute(
                    "INSERT INTO test1(id,title,date,content,url) VALUES ('{}','{}','{}','{}','{}')".format(id, title,
                                                                                                            date,
                                                                                                            content,
                                                                                                            link2))  # 这里的字符集在mysql里面也要设置为utf8，目前只能用phpmydamin
                db.commit()
                time.sleep(random.randint(1, 5))
            except:
                db.rollback()
                print("数据库操作出现错误\n")



geturl(getsurl(allurl))
