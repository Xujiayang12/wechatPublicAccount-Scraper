from flask import Flask
from flask import request,Response,jsonify
import json
import pymysql

app = Flask(__name__)
######请在这里填入密码########

password="XXX"

###########################
db = pymysql.connect("localhost", "root", password, "TESTDB", charset="utf8")  # 注意设置为utf8
cursor = db.cursor()

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/article_list/<listnum>', methods=['GET','POST'])
def artlist(listnum):
    if request.method=="GET":
        return getpage(int(listnum))

@app.route('/article_list/', methods=['POST'])
def artlist2():
    if request.method == "POST":
        page = json.loads(request.get_data())['page']##一开始用的page = request.form['page']是要x-ww啥啥啥的请求方式
        return getpage(int(page))

def getpage(num):
    db = pymysql.connect("localhost", "root", password, "TESTDB", charset="utf8")  # 注意设置为utf8
    cursor = db.cursor()
    print("SELECT * FROM test1 ORDER BY id DESC LIMIT %d,10"%((num-1)*10))
    cursor.execute("SELECT * FROM test1 ORDER BY id DESC LIMIT %d,10"%((num-1)*10))
    results = cursor.fetchall()
    datain=[]
    for i in results:
        dictt={}
        dictt['title']=i[1]
        dictt['date']=i[2]
        dictt['id']=i[0]
        datain.append(dictt)
    data={"data":datain}
    js=json.dumps(data)
    resp=Response(js,status=200,mimetype="application/json")
    return resp
@app.route('/article_detail/<connum>',methods=['GET','POST'])
def artdtl(connum):
    if request.method=="GET":
        return getdtl(int(connum))

@app.route('/article_detail/', methods=['POST'])
def artdtl2():
    if request.method=="POST":
        sid=json.loads(request.get_data())['id']
        return getdtl(int(sid))

def getdtl(num):
    db = pymysql.connect("localhost", "root", password, "TESTDB", charset="utf8")  # 注意设置为utf8
    cursor = db.cursor()
    print("SELECT * FROM test1 WHERE id = %d "% num)
    cursor.execute("SELECT * FROM test1 WHERE id = %d "% num)
    out= cursor.fetchone()
    dictt={}
    dictt['title']=out[1]
    dictt['data']=out[2]
    dictt['content']=out[3]
    dictt['url']=out[4]
    js=json.dumps(dictt)
    resp=Response(js,status=200,mimetype="application/json")
    return resp


if __name__ == '__main__':
    app.run()
