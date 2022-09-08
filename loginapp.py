from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from passlib.hash import pbkdf2_sha256
import os
from flask import Flask, render_template, request, jsonify
from flask_migrate import Migrate

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1qaz2wsx@localhost/MovieDatabase'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
# PEOPLE_FOLDER = os.path.join('templates', 'static/abhi.jpg')
# app.config['templates'] = PEOPLE_FOLDER

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.VARCHAR(120), nullable=False)
    email = db.Column(db.VARCHAR(120), nullable=True)

    @staticmethod
    def adduser(name, password):
        data = Users.query.filter_by(name=name).first()
        if data == None:
            hashed = pbkdf2_sha256.hash(password)
            new_user = Users(name=name, password=hashed)
            db.session.add(new_user)
            db.session.commit()
            return True

        else:
            return False

    @staticmethod
    def checkpassword(name, password):
        data = Users.query.all()
        for p in data:
            if name == p.name:
                if pbkdf2_sha256.verify(password, p.password):
                    return True
                else:
                    return False
        else:
            return False


@app.route("/", methods=["GET", "POST"])
def homepage():
    data = {}
    if request.method == 'POST':
        if request.form['submit_button'] == "Login":
            return render_template('loginpage.html', data=data)
        elif request.form['submit_button'] == "SignUp":
            return render_template('newaccount.html', data=data)
        else:
            pass
    else:
        return render_template('home.html')


@app.route("/login", methods=["GET", "POST"])
def loginpage():
    data = {}
    if request.method == "POST":
        n = request.form["name"]
        p = request.form["password"]
        check = Users.checkpassword(n, p)
        if check:
            data = {'code': 200}
            return render_template('index.html', data=data)
        else:
            data = {'code': 400}
            return render_template('loginpage.html', data=data)


@app.route("/create", methods=["GET", "POST"])
def createpage():
    data = {}
    if request.method == "POST":
        n = request.form["name"]
        p = request.form["password"]
        createuser = Users.adduser(n, p)
        if createuser:
            data = {'code': 200}
            return render_template('newaccount.html', data=data)
        else:
            data = data = {'code': 400}
            return render_template('newaccount.html', data=data)

    return render_template('newaccount.html', data=data)


@app.route("/axe",methods=["GET", "POST"])
def axe_page():
    return render_template('axe.html')


@app.route("/blog",methods=["GET", "POST"])
def blog_page():
    return render_template('blog.html')


@app.route("/index",methods=["GET", "POST"])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
