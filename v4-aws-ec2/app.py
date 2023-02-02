from flask import Flask,g
from flask import request
from flask import render_template
from flask import redirect, url_for, flash
import json
import os
import sqlite3
import time

#Capture
import paho.mqtt.client as mqtt
# define Mqtt address, and password
SERVER = "35.174.5.8"
user_name = "moment"
password = "iot2022"
  
app = Flask(__name__)
app.secret_key='3435234'
def closedb(cur,conn):
    cur.close()
    conn.close()

# share code
scode=0
# picture code
pcode=0
# initial indicator
icode=0

@app.route('/')
def login():
    return redirect(url_for('index'))

# 登录
@app.route('/index', methods=['get','post'])
def index():
    if request.method=='POST':
        username = request.form.get('username')
        password = str(request.form.get('password'))
        #sqlite
        conn=sqlite3.connect('credentials.db')
        cur=conn.cursor()
        cur.execute('SELECT password FROM USER WHERE (UID='+str(username)+')')

        result=cur.fetchall()

        if not result:
            # User not exit
            closedb(cur,conn)
            flash("用户名不存在")
            return render_template("index.html")
        elif result[0][0]==password:
            # Pass
            closedb(cur,conn)
            global scode
            scode = (int(username)*1778)%1000
            global icode
            icode = 0
            context = {
                "scode" : scode,
                "image" : "/static/photo/test.jpg"
            }
            return  render_template("photo.html",**context)
        else:
            # Fail
            closedb(cur,conn)
            flash("密码不匹配")
            return render_template("index.html")
    else:
        return render_template("index.html")

# 注册
@app.route('/register', methods=['get','post'])
def register():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        #sqlite
        conn=sqlite3.connect('credentials.db')
        cur=conn.cursor()
        try:
            cur.execute("INSERT INTO USER VALUES("+str(username)+',"'+str(password)+'",0);')
            conn.commit()
        except:
            conn.rollback()
            flash("注册失败")
            return render_template('register.html')

        closedb(cur,conn)
        flash("注册成功")
        return redirect(url_for('index'))
    else:
        return render_template('register.html')

# 分享
@app.route('/share', methods=['get','post'])
def share():
    if request.method=='POST':
        sharecode = request.form.get('scode')
        global scode
        if sharecode == str(scode):
            context = {
                "image" : "/static/photo/test.jpg"
            }
            return render_template('photo1.html',**context)
        else:
            flash('号码不存在')
            return render_template('share.html')       
    else:
        return render_template('share.html')     


# 捕获
def on_connect(client,userdata,flags,rc):
    if rc==0:
        client.publish("TakeAPicture","on")
        return 1
    else:
        return 0

def on_publish(client,userdata,mid):
    client.disconnect()

@app.route('/capture', methods=['get'])
def capture():
    client = mqtt.Client(client_id="2", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
    client.username_pw_set(username=user_name, password=password)
    rc = client.connect(SERVER, 1883, 30)
    if rc==1:
        # 截取图片名称
        global pcode
        pcode+=1
        # 用户界面获取了图片
        global icode
        icode = 1

        while not os.path.exists(f'static/photo/{pcode}.jpg'):
            time.sleep(0.5)
        response = {'success': 1 ,
                    "path": f'/static/photo/{pcode}.jpg'}
        return json.dumps(response)
    else:
        return json.dumps({'success': 0 })

# 更新
@app.route('/renew', methods=['get'])
def renew():
    global icode 
    if icode==1:
        response = {'success': 1 ,
                    "path": f'/static/photo/{pcode}.jpg'}
        return json.dumps(response)
    else:
        return json.dumps({'success': 0 })
        
if __name__  == "__main__":
    app.run(debug=True)
