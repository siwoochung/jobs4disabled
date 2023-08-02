#frontend/backend


from flask import Flask,render_template, request, redirect,url_for,flash, jsonify,session
import pandas as pd
from register_login import register,login_check, get_interest
from recommendation import pick_jobs, pick_jobs_filter_by_class, pick_jobs_filter_by_hire_type
from datetime import timedelta
from graph_generator import income_compare, similarity_graph
import json

app = Flask(__name__)

app.config['SECRET_KEY']='abc'
fill = False
business_checked = False
it_checked = False
design_checked = False
trade_checked = False
education_checked = False
medical_checked = False
service_checked = False
produce_checked  = False
special_checked  = False
contract_checked = False
fulltime_checked = False
parttime_checked = False
isLogin = False 

app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=60)

@app.route('/',methods=['GET','POST'])
def index():
	global isLogin, fill, business_checked, it_checked, design_checked, trade_checked,education_checked, medical_checked, service_checked, produce_checked, special_checked, contract_checked,fulltime_checked,parttime_checked
	income_compare_data = income_compare()
	income_compare_data = json.dumps(income_compare_data)
	sim_compare_data = similarity_graph()
	sim_compare_data = json.dumps(sim_compare_data)

	if request.method=='POST':
		business_checked = request.form.get("business") != None
		it_checked = request.form.get("IT") != None
		design_checked = request.form.get("design") != None
		trade_checked = request.form.get("trade") != None
		education_checked = request.form.get("education") != None
		medical_checked = request.form.get("medical") != None
		service_checked = request.form.get("service") != None
		produce_checked = request.form.get("produce") != None
		special_checked = request.form.get("special") != None
		contract_checked = request.form.get("contract") != None
		fulltime_checked = request.form.get("fulltime") != None
		parttime_checked = request.form.get("parttime") != None
		fill=True
		return redirect (url_for('index')) 
	else:
		if business_checked == True or design_checked == True or trade_checked==True or education_checked==True or medical_checked==True or service_checked==True or produce_checked==True or special_checked==True : 
				print("This is error output", flush=True)
				lst_jobs = pick_jobs_filter_by_class(10,business_checked,it_checked, design_checked, trade_checked,education_checked, medical_checked, service_checked, produce_checked, special_checked)
				if contract_checked==True or fulltime_checked==True or parttime_checked==True:
					lst_jobs = pick_jobs_filter_by_hire_type(10, lst_jobs,contract_checked, fulltime_checked, parttime_checked)
		else: 
			lst_jobs = pick_jobs(3)
		if 'username' in session: #when user is logged in 
			isLogin = True 
			return render_template("index.html", job_lst=lst_jobs, isLogin = isLogin, username=session['username'], data1=income_compare_data, data2=sim_compare_data )
		else: # when user is not logged in 
			isLogin = False  
			return render_template("index.html", job_lst=lst_jobs, isLogin = isLogin, data1=income_compare_data, data2=sim_compare_data)

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method=='POST':
		username = request.form['username']
		password = request.form['password']
		if(login_check(username,password)==True):
			session['username'] = request.form['username']
			return redirect(url_for('index'))
		else:
			flash('Wrong Password') 
			return render_template("login.html")

	else:
		if 'username' in session:
			return redirect (url_for('index'))
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

@app.route('/logout')
def logout():
	session.pop('username', None) #remove out 'username' from session // removing session
	return redirect (url_for('index'))

@app.route('/profile')
def profile():
	if 'username' in session:
		username = session['username']
		interest = get_interest(username)
		return render_template("profile.html", username=username,interest=interest, isLogin=isLogin)
	else:
		return redirect (url_for('index'))

@app.route('/FAQ')
def faq(): 
	if 'username' in session:
		username = session['username']
		interest = get_interest(username)
		return render_template("FAQ.html", username=username,interest=interest, isLogin=isLogin)
	else:
		return redirect (url_for('index'))



if __name__=="__main__":
	app.run(host='127.0.0.1', port=8000,debug=True)

