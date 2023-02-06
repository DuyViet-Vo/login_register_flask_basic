from flask import Flask, request,render_template, session,url_for,redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)

app.secret_key="secret key"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'test'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['GET','POST'])
def login():
    messen = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cur= mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM users WHERE username = % s AND password = % s', (username, password, ))
        account = cur.fetchone()
        if account:
            session['login'] = True
            session['id']= account['id']
            session['username'] = account['username']
            messen = 'Dang nhap thanh cong!'
            data = account
            return render_template('index.html',msg = messen, data = data)
        else:
            messen ='Đăng nhập không thành công!'
    return render_template('login.html', msg = messen)

@app.route('/logout')
def logout():
    session.pop('login', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register',methods = ['POST','GET'])
def register():
    messen =''
    if request.method == "POST":
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM users WHERE username = %s',(userName,))
        account = cur.fetchone()
        if account:
            messen = "Tên đã tồn tại!"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            messen ="Địa chỉ email không hợp lệ!"
        elif not re.match(r'[A-Za-z0-9]+', userName):
            messen = 'Tên người dùng không được chứa ký tự số!'
        elif not userName or not password or not email:
            messen = 'Vui lòng điền vào mẫu đơn!'
        else:
            cur.execute('INSERT INTO users(id,username,password,email) VALUES (NULL,%s,%s,%s)', (userName,password,email))
            mysql.connection.commit()
            messen = 'Đăng ký thành công tài khoản'
    elif request.method == 'POST':
        messen = 'Vui lòng điền vào mẫu đơn!'
    return render_template('register.html',msg = messen)

if __name__ == '__main__':
    app.run(debug=True)
    