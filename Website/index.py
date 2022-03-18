from flask import Flask,render_template, request
from flask_mysqldb import MySQL
app = Flask(__name__)

app.run(host='localhost', port=5000)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Regina123'
app.config['MYSQL_DB'] = 'flask'
 
mysql = MySQL(app)

@app.route('/index')
def form():
    return render_template('index.html')
