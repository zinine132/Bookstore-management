from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'KAJSDFKLKMLAKMDK123LJKLAJSOIDFIO123'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:1234@localhost/bookstoredb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['PAGE_SIZE'] = 8

db = SQLAlchemy(app=app)
login = LoginManager(app=app)