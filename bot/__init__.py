from flask import Flask
from flaskext.mysql import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = '00f2b1ead3a0990b818517356cb40280'
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'chatbot'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
from bot import views
