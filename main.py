import sqlite3
from flask import Flask,render_template,request,session,redirect,url_for,g,flash
from wtforms import FileField,SubmitField,FormField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
from flask_wtf import FlaskForm
import pandas as pd
import matplotlib.pyplot as plt
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin






class UploadFileForm(FlaskForm):
  file = FileField("File",validators=[InputRequired()])
  submit = SubmitField("Upload file")

db=SQLAlchemy()
DB_NAME= 'database.db'
app = Flask(__name__)
app.config['SECRET_KEY']='zamiel'
app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'
app.config['UPLOAD_FOLDER'] = 'static/files'

adminkey='z'

username=''

def create_database(app):
    db.init_app(app)
    if not path.exists(DB_NAME):
        with app.app_context():
            db.create_all()
        print("Database creaated")

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String,unique=True)
    fullName=db.Column(db.String(100))
    password=db.Column(db.String(100))  
class First_year(db.Model):
    #============first year table data ==================
    roll_no = db.Column(db.Integer, primary_key=True)
    st_name = db.Column(db.String(25), nullable=False)
    enrollment_no = db.Column(db.String(20), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    sub1 = db.Column(db.Integer, nullable=False)
    sub2 = db.Column(db.Integer, nullable=False)
    sub3 = db.Column(db.Integer, nullable=False)
    sub4 = db.Column(db.Integer, nullable=False)
    sub5 = db.Column(db.Integer, nullable=False)
    sub6 = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(30), nullable=False)

class Subject(db.Model):
    #============Subject table data ==================
    semester = db.Column(db.Integer, primary_key=True)
    sub1 = db.Column(db.String(50), nullable=False)
    sub2 = db.Column(db.String(50), nullable=False)
    sub3 = db.Column(db.String(50), nullable=False)
    sub4 = db.Column(db.String(50), nullable=False)
    sub5 = db.Column(db.String(50), nullable=False)
    sub6 = db.Column(db.String(50), nullable=False) 
    
class Second_year(db.Model):
    #============second year table data ==================
    roll_no = db.Column(db.Integer, primary_key=True)
    st_name = db.Column(db.String(25), nullable=False)
    enrollment_no = db.Column(db.String(20), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    sub1 = db.Column(db.Integer, nullable=False)
    sub2 = db.Column(db.Integer, nullable=False)
    sub3 = db.Column(db.Integer, nullable=False)
    sub4 = db.Column(db.Integer, nullable=False)
    sub5 = db.Column(db.Integer, nullable=False)
    sub6 = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(30), nullable=False)

class Third_year(db.Model):
    #============third year table data ==================
    roll_no = db.Column(db.Integer, primary_key=True)
    st_name = db.Column(db.String(25), nullable=False)
    enrollment_no = db.Column(db.String(20), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    sub1 = db.Column(db.Integer, nullable=False)
    sub2 = db.Column(db.Integer, nullable=False)
    sub3 = db.Column(db.Integer, nullable=False)
    sub4 = db.Column(db.Integer, nullable=False)
    sub5 = db.Column(db.Integer, nullable=False)
    sub6 = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(30), nullable=False)



    
 
    
    
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))




@app.route("/")
def home():
  return render_template('index.html')

@app.route("/view")
def view():  
    return render_template("view.html") 
    
@app.route("/result")
def result():  
    return render_template("result.html")   

        
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        email= request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                login_user(user, remember=True)
                return redirect('/profile')
            else:
                print('Wrong pass')

    return render_template('login.html')
        

@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email   = request.form['email']
        adminkey = request.form['adminkey']
        if adminkey != 'aisat123':
            return redirect(url_for('login'))   
        new_user=User(fullName=username,password=password,email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    else:
        return render_template('register.html')

@app.route('/profile', methods=['GET','POST'])
def file_upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # process the uploaded CSV file
            return render_template('/profile.html')
        else:
            return "No file selected"
        batch = request.form['batch']
        semester = request.form['semester']
    else:
        return render_template('/profile.html')

  



    
    
@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('home'))


if __name__ == "__main__":
    create_database(app)
    app.run(host="0.0.0.0", debug=True)