import os
from pprint import pprint
import simplejson
import mysql.connector
#from Tools.scripts.mailerdaemon import x
import sql as sql
from flask import Flask, session, flash
from flask import render_template
from flask import request
from flask import json
from werkzeug.security import generate_password_hash, check_password_hash
from flaskext.mysql import MySQL

project_root = os.path.dirname(__name__)
template_path = os.path.join(project_root)

mysql = MySQL()
app = Flask(__name__,template_folder=template_path)
# mysql configuratoin
app.config['MYSQL_DATABASE_HOST']       = 'localhost'
app.config['MYSQL_DATABASE_USER']       = 'root'
app.config['MYSQL_DATABASE_PASSWORD']   = 'Rajesh@0608'
app.config['MYSQL_DATABASE_DB']         = 'Testing'
mysql.init_app(app)

@app.route('/')
def main_world():
    return render_template('Index.html')


def home():
    if not session.get ('logged_in'):
        return render_template ('SignUp.html')
    else:
        return "Hello Boss!"


@app.route ('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['name'] == '':
        session['logged_in'] = True
    else:
        flash ('wrong password!')
    return home ()


@app.route('/signup')
def signUp():
    # open connection
    return render_template ('SignUp.html')
    # read request from UI
    _name_   = request.form['name']
    _email_  = request.form['email']
    _pass_   = request.form['pass']
    _hash_pass_ = generate_password_hash(_pass_)

    if _name_ and _email_ and _pass_:
        insert(_name_,_email_,_hash_pass_)
        return json.dumps({'html':'<span>Data Inserted </span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})

@app.route('/insert')
def insert():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO user1 (name,email,pass) VALUES (%s,%s,%s)", [('varun1','varun1@qpair.io','csdjcscdhsd'),('Raghu','ragu@qpair.io','dsvcsj')])
    conn.commit()
    conn.close()
    return 'success'

@app.route('/show')
def show():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user1")
    data = cursor.fetchall()
    dataList = []
    if data is not None:
        for item in data:
            dataTempObj = {
#               'id'        : item[0],
                'name'      : item[0],
                'email'     : item[1],
                'password'  : item[2]
            }
            dataList.append(dataTempObj)
        return json.dumps(dataList)
    else:
        return 'data kosong'

@app.route('/update')
def update():
    conn = mysql.connect()
    cursor = conn.cursor()
    result = cursor.execute("UPDATE user1 set name='Varun1' where email='varun@qpair.io'")
    conn.commit()
    conn.close()
    return 'success'

@app.route('/delete')
def delete():
    conn = mysql.connect()
    cursor = conn.cursor()
    result = cursor.execute("DELETE FROM user1 where name='Varun1' ")
    conn.commit()
    conn.close()
    if(result):
        return json.dumps({'delete':'true'})
    else:
        return json.dumps({'delete':'false'})
if __name__ == '__main__':
    app.secret_key = os.urandom (12)
    app.run(debug=True,port = 3200)