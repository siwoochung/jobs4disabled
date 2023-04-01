#frontend/backend

from flask import Flask,render_template, request, redirect,url_for,flash, jsonify
import pandas as pd
from register_login import register,login_check
from recommendation import pick_jobs


app = Flask(__name__)

app.config['SECRET_KEY']='abc'

@app.route('/')
def index():
	lst_jobs = pick_jobs(10)
	return render_template("index.html", job_lst=lst_jobs)

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method=='POST':
		username = request.form['username']
		password = request.form['password']
		if(login_check(username,password)==True):
			return redirect(url_for('index'))
		else:
			flash('Wrong Password') 
			return render_template("login.html")


	else:
		return render_template("login.html")
@app.route('/signup',methods=['GET','POST'])
def signup():
	if request.method=='POST':
		username = request.form['username']
		password = request.form['password']
		age = request.form['age']
		gender = request.form.get('gender')
		phone = request.form['phone_number']
		interest = request.form.get('interest')
		register(username,password, age, gender, phone, interest)
		return "Successfully Registered!"
	else: #'GET'
		return render_template("signup.html")


if __name__=="__main__":
	app.run(debug=True)

