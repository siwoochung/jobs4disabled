#frontend/backend


from flask import Flask,render_template, request,send_file, redirect,url_for,flash, jsonify,session
import pandas as pd
from register_login import register,login_check, get_interest
from recommendation import pick_jobs,pick_jobs2, pick_jobs_filter_by_class, pick_jobs_filter_by_hire_type
from datetime import timedelta
from graph_generator import income_compare, similarity_graph
import json
from calculate_income import convert, get_average, compare_income
from naver_distance import calculate_distance
import random
import os
import sqlite3 as sq
import shutil
import asyncio

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
lst_jobs = []
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=180)

@app.route('/',methods=['GET','POST'])
def index():
        global lst_jobs,isLogin, fill, business_checked, it_checked, design_checked, trade_checked,education_checked, medical_checked, service_checked, produce_checked, special_checked, contract_checked,fulltime_checked,parttime_checked
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
                        if 'username' in session:
                                lst_jobs = pick_jobs2(80,session["username"])
                                lst_jobs = sorted(lst_jobs, key=lambda x: x['add'])
                        else:
                                lst_jobs = pick_jobs(80,-1)
                                lst_jobs = sorted(lst_jobs, key=lambda x: x['add'])
                if 'username' in session: #when user is logged in
                        imge_path='../static/users/'+session["username"]+"/image/img.png"
                        bookmarked_jobs = read_bookmarked_jobs(session['username'])
                        isLogin = True
                        username = session["username"]
                        typ = session["type"]
                        conn = sq.connect('data/login_info.db')
                        cursor = conn.cursor()

                        cursor.execute("SELECT interest FROM user WHERE username = ?", (username,))
                        interest = cursor.fetchone()[0]
                        cursor.execute("SELECT edu FROM user WHERE username = ?", (username,))
                        edu = cursor.fetchone()[0]
                        cursor.execute("SELECT exp FROM user WHERE username = ?", (username,))
                        exp = cursor.fetchone()[0]
                        cursor.execute("SELECT type FROM user WHERE username = ?", (username,))
                        typ = cursor.fetchone()[0]
                        return render_template("index.html",typ=typ,edu=edu,exp=exp,interest=interest, img_path=imge_path,bookmarked_jobs=bookmarked_jobs, job_lst=lst_jobs, isLogin = isLogin, username=session['username'], data1=income_compare_data, data2=sim_compare_data )
                else: # when user is not logged in 
                        isLogin = False  
                        return render_template("index.html",edu=0, exp=1,interest=[],bookmarked_jobs=[],job_lst=lst_jobs, isLogin = isLogin, data1=income_compare_data, data2=sim_compare_data)
@app.route('/api/job-listings')
def get_job_listings():
    return jsonify(lst_jobs)

def read_bookmarked_jobs(username):
    file_path = 'users/' + username + '/bookmark_lst.txt'
    bookmarked_jobs = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                job_id = int(line.strip())
                bookmarked_jobs.append(job_id)
    except FileNotFoundError:
        pass
    return bookmarked_jobs
@app.route('/login',methods=['GET','POST'])
def login():
        if request.method=='POST':
                username = request.form['username']
                password = request.form['password']
                if(login_check(username,password)==True):
                        session['username'] = request.form['username']
                        conn = sq.connect('data/login_info.db')
                        cursor = conn.cursor()

                        cursor.execute("SELECT type FROM user WHERE username = ?", (username,))
                        typ = cursor.fetchone()[0]
                        session['type'] = typ
                        return redirect(url_for('index'))
                else:
                        flash('Wrong Password') 
                        return render_template("login.html")

        else:
                if 'username' in session:
                        return redirect (url_for('index'))
                return render_template("login.html")


@app.route('/signup',methods=['GET','POST'])
async def signup():
        if request.method=='POST':
                username = request.form['username']
                password = request.form['password']
                typ = request.form.get('userType')
                if typ == 1:
                        age=0
                        gender=0
                else:
                        age = request.form['age']
                        gender = request.form.get('gender')
                phone = request.form['phone_number']
                interest  = request.form.getlist('interests[]')
                interest = ",".join(interest)
                address = request.form['address']
                
                email = request.form['email']
                level = request.form.get('level')
                restrict = request.form.get('rest')
                edu = request.form.get('education')
                exp= request.form.get('experience')
                register(username,password, age, gender, phone, interest, address,level, typ, restrict,edu,exp,email)
                df = pd.read_csv("data/temp_data.csv")
                #df["time"] = df["사업장 주소"].apply(calculate_distance, args=(address,))
                #loop = asyncio.get_event_loop()
                #results = loop.run_until_complete(calculate_distances_async(df,address))
                path = os.path.join("users/", username )
                path2 = os.path.join("static/users/", username )
                source_path = 'static/users/img.png'
                source_path2 = 'users/time.csv'
                try:
                                        os.makedirs(path)
                                        os.makedirs(path+"/resume")
                                        os.makedirs(path+"/resume_own")
                                        with open(path+"/applied_lst.txt", "w") as file:
                                                pass
                                        with open(path+"/bookmark_lst.txt", "w") as file:
                                                pass
                                        shutil.copy(source_path2, os.path.join(path, "time.csv"))

                                        os.makedirs(path2)
                                        os.makedirs(path2+"/image")
                                        shutil.copy(source_path, os.path.join(path2+"/image", "img.png"))

                                        
                except:
                                        pass
                return redirect (url_for('login'))
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
                typ = session["type"]
                interest = get_interest(username)
                file_path = 'users/'+session["username"]+"/applied_lst.txt" 
                imge_path='../static/users/'+session["username"]+"/image/img.png"
                lines_list = []
                df = pd.read_csv("data/temp_data.csv")

                if typ == 0:
                        with open(file_path, "r") as file:
                            for line in file:
                                lines_list.append(int(line.strip()))
                        final_lst = []
                        for i in lines_list:
                                matching_rows = df[df['id'] == i]
                                dic = {}
                                dic["companyname"] = matching_rows["Company"].iloc[0]
                                dic["jobname"] = matching_rows["모집직종"].iloc[0]
                                dic["address"] = matching_rows["사업장 주소"].iloc[0]
                                final_lst.append(dic)
                        bookmarked_jobs = read_bookmarked_jobs(session['username'])
                        final_lst2 = []
                        for i in bookmarked_jobs:
                                matching_rows = df[df['id'] == i]
                                dic = {}
                                dic["companyname"] = matching_rows["Company"].iloc[0]
                                dic["jobname"] = matching_rows["모집직종"].iloc[0]
                                dic["address"] = matching_rows["사업장 주소"].iloc[0]
                                dic["applied"] = False
                                for j in final_lst:
                                        if j["companyname"] == dic["companyname"]:  
                                                dic["applied"] = True
                                final_lst2.append(dic)
                else:
                        with open(file_path, "r") as file:
                            for line in file:
                                lines_list.append(line.strip())
                        conn = sq.connect('data/login_info.db')
                        cursor = conn.cursor()
                        final_lst2 = []
                        # Define the username
                        username = session["username"]

                        cursor.execute("SELECT phone FROM user WHERE username = ?", (username,))
                        phone = cursor.fetchone()[0]
                        cursor.execute("SELECT email FROM user WHERE username = ?", (username,))
                        email = cursor.fetchone()[0]
                        cursor.execute("SELECT level FROM user WHERE username = ?", (username,))
                        level = cursor.fetchone()[0]
                        final_lst = []
                        for i in lines_list:
                                matching_rows = df[df['id'] == i]
                                dic = {}
                                dic["phone"] = phone
                                dic["email"] = email
                                dic["username"] = i
                                dic["level"] = level
                                final_lst.append(dic)            

                conn = sq.connect('data/login_info.db')
                cursor = conn.cursor()

                # Define the username
                username = session["username"]

                cursor.execute("SELECT gender FROM user WHERE username = ?", (username,))
                gender = cursor.fetchone()[0]
                if gender =='male':
                        gender = "남성"
                else:
                        gender = "여"
                cursor.execute("SELECT age FROM user WHERE username = ?", (username,))
                age = cursor.fetchone()[0]
                cursor.execute("SELECT interest FROM user WHERE username = ?", (username,))
                interest = cursor.fetchone()[0]
                cursor.execute("SELECT phone FROM user WHERE username = ?", (username,))
                phone = cursor.fetchone()[0]
                cursor.execute("SELECT level FROM user WHERE username = ?", (username,))
                level = cursor.fetchone()[0]
                cursor.execute("SELECT restrict FROM user WHERE username = ?", (username,))
                restrict = cursor.fetchone()[0]
                cursor.execute("SELECT type FROM user WHERE username = ?", (username,))
                typ = cursor.fetchone()[0]
                if restrict == 'y':
                        restrict =="있음"
                else:
                        restrict=="없음"
                return render_template("profile.html",typ=typ,level=level,restrict=restrict,username=username,gender=gender,age=age,interest=interest,phone=phone,img_path=imge_path,bookmarked_jobs=final_lst2, final_lst = final_lst, isLogin=isLogin)

                        
        else:
                return redirect (url_for('index'))

@app.route('/bookmark/<int:job_id>', methods=['POST'])
def bookmark_job(job_id):
    file_path = 'users/' + session["username"] + "/bookmark_lst.txt" 
    with open(file_path, "a") as file:
        file.write(str(job_id) + "\n")
    bookmarked_jobs = read_bookmarked_jobs(session['username'])
    return jsonify(message='Job bookmarked successfully', bookmarked_jobs=bookmarked_jobs), 200

@app.route('/unbookmark/<int:job_id>', methods=['POST'])
def unbookmark_job(job_id):
    file_path = 'users/' + session["username"] + "/bookmark_lst.txt"
    temp_file_path = 'users/' + session["username"] + "/bookmark_lst_temp.txt"

    with open(file_path, 'r') as f_in, open(temp_file_path, 'w') as f_out:
        for line in f_in:
            if int(line.strip()) != job_id:
                f_out.write(line)

    # Remove the original bookmark_lst.txt file and rename the temp file to the original name
    os.remove(file_path)
    os.rename(temp_file_path, file_path)
    bookmarked_jobs = read_bookmarked_jobs(session['username'])
    return jsonify(message='Job unbookmarked successfully', bookmarked_jobs=bookmarked_jobs), 200
@app.route('/FAQ')
def faq(): 
        if 'username' in session:
                imge_path='../static/users/'+session["username"]+"/image/img.png"

                username = session['username']
                interest = get_interest(username)
                return render_template("FAQ.html", img_path=imge_path,username=username,interest=interest, isLogin=isLogin)
        else:
                return redirect (url_for('index'))

@app.route('/search', methods=['POST'])
def search_results():
        username = session["username"]
        imge_path='../static/users/'+session["username"]+"/image/img.png"
        income_compare_data = income_compare()
        income_compare_data = json.dumps(income_compare_data)
        sim_compare_data = similarity_graph()
        sim_compare_data = json.dumps(sim_compare_data)
        df = pd.read_csv("users/"+session["username"]+"/time.csv")
        conn = sq.connect('data/login_info.db')
        cursor = conn.cursor()
        bookmarked_jobs = read_bookmarked_jobs(session['username'])
        isLogin = True
        cursor.execute("SELECT interest FROM user WHERE username = ?", (username,))
        interest = cursor.fetchone()[0]
        myinterest = interest
        cursor.execute("SELECT edu FROM user WHERE username = ?", (username,))
        edu = cursor.fetchone()[0]
        cursor.execute("SELECT exp FROM user WHERE username = ?", (username,))
        exp = cursor.fetchone()[0]
        search_query = request.form['query']  # Get the search query from the form data
        filtered_df= df[df["모집직종"].str.contains(search_query, case=False) | df["Company"].str.contains(search_query, case=False)]
        filtered_df["pay_month"] = filtered_df['임금'].apply(convert)
        filtered_df["pay_month_diff"] = filtered_df["pay_month"].apply(compare_income)
        if len(filtered_df) == 0:
                return render_template('search_result.html', results=[])
        name = filtered_df["모집직종"].tolist()
        hire_type = filtered_df["고용형태"].tolist()
        pay = filtered_df["임금"].tolist()
        paytype = filtered_df["임금형태"].tolist()
        location = filtered_df["사업장 주소"].tolist()
        company_type = filtered_df["기업형태"].tolist()
        job_class = filtered_df["Classification"].tolist()
        required_degree = filtered_df["요구학력"].tolist()
        required_work = filtered_df["요구경력"].tolist()
        company = filtered_df["Company"].tolist()
        address = filtered_df["사업장 주소"].tolist()
        job_id = filtered_df["id"].tolist()
        time = filtered_df["time"].tolist()
        pay_month = filtered_df["pay_month"].tolist()
        pay_month_diff = filtered_df["pay_month_diff"].tolist()
        final_lst=[]
        # i = 0
        # while i < NUMS:
        for i in range(len(filtered_df)):
                # if (calculate_distance(address[i])>60):
                #       continue
                dic = dict()  #{}
                dic["Company"] = company[i]
                dic["모집직종"]=name[i]
                dic["id"] = job_id[i]
                dic["add"] = time[i]
                pay_month_diff[i] = round(pay_month_diff[i],1)
                dic["pay_month_diff"] = pay_month_diff[i]
                pay_month_diff[i] = round(pay_month_diff[i],1)
                dic["pay_month_diff"] = pay_month_diff[i]
                percent = 90
                percent = 90 - float(time[i]*0.4)
                if str(job_class[i]) in myinterest:
                        if percent + 20 < 100:
                                percent += 20
                        else:
                                percent = 100
                else:
                        percent = percent-10
                dic["percent"] = int(percent)
                pay[i] = "{:,}".format(pay[i])
                if paytype[i] == 0:
                        # dic["pay"]= "시급: ₩"+ str(pay[i])
                        dic["pay"]= str(pay[i])
                elif paytype[i]== 1:
                        dic["pay"]= str(pay[i])
                elif paytype[i] == 2:
                        dic["pay"]= str(pay[i])
                else:
                        dic["pay"]= str(pay[i])
                # dic[""]=company[i]

                dic["고용형태"]=hire_type[i]
                if hire_type[i]==0:
                        dic["고용형태"] = "계약직"
                elif hire_type[i]==1:
                        dic["고용형태"] = "상용직"
                else:
                        dic["고용형태"] = "시간제"

                dic["사업장 주소"]=location[i]

                dic["기업형태"]=company_type[i]
                if company_type[i]==0:
                        dic["기업형태"]="개인"
                elif company_type[i]==1 or company_type[i]==5:
                        dic["기업형태"]="중소"
                elif company_type[i]==2:
                        dic["기업형태"]="협회,단체"
                elif company_type[i]==3:
                        dic["기업형태"]="공사,공공"
                elif company_type[i]==4:
                        dic["기업형태"]="대기업"
                dic["edu"] = required_degree[i]
                dic["exp"] = required_work[i]

                dic["Classification"]=job_class[i]

                dic["요구학력"]=required_degree[i]
                if required_degree[i]==0:
                        dic["요구학력"]="학력무관"
                elif required_degree[i]==1:
                        dic["요구학력"]="고졸"
                elif required_degree[i]==2:
                        dic["요구학력"]="초대졸"
                else:
                        dic["요구학력"]="대졸"

                
                dic["요구경력"]=required_work[i]
                if required_work[i]==0:
                        dic["요구경력"]="경력무관"
                elif required_work[i]==1:
                        dic["요구경력"]="1년"
                elif required_work[i]==2:
                        dic["요구경력"]="2년"
                else:
                        dic["요구경력"]="3년 이상"
                final_lst.append(dic)
        typ = session["type"]
        return render_template('search_result.html',img_path=imge_path, username=session['username'], data1=income_compare_data, data2=sim_compare_data, isLogin=isLogin,bookmarked_jobs=bookmarked_jobs,job_lst=final_lst,edu=edu,exp=exp,interest=interest,typ=typ)

@app.route('/save_changes', methods=['POST'])
def save_changes():
    id = request.args.get('id')
    username = session["username"]
    a = id
    if request.method == 'POST':
        uploaded_file = request.files['uploaded_file']  # 'uploaded_file' should match the input field name in your HTML form

        df = pd.read_csv("data/temp_data.csv")
        a = int(a)

        df = df[df["id"]==a]
        comp = df["Company"]
        comp = comp.iloc[0]
        comp = str(comp)

        directory_to_check = comp
        if os.path.isdir("users/"+comp):
            print(f"The directory '{directory_to_check}' exists in the specific path.")
            with open("users/"+comp+"/applied_lst.txt", "a") as file:
                    file.write(username+"\n")
        
        if uploaded_file:
            file_extension = os.path.splitext(uploaded_file.filename)[1]
            if id !='own':
                    file_path = os.path.join('users/'+session["username"]+"/resume", "Resume"+
                                             str(id)+file_extension)
            else:
                    
                    file_path = os.path.join('users/'+session["username"]+"/resume", "Resume-own"+file_extension)

            uploaded_file.save(file_path)
            file_path = 'users/'+session["username"]+"/applied_lst.txt"
            with open(file_path, "a") as file:
                    file.write(id+"\n")
            return '"성공적으로 지원이되었습니다.!"'
        else:
            return '오류가 발생했습니.!'
    return 'Invalid request'
@app.route('/download')
def download_file():
    file_path = 'users/'+session["username"]+"/resume_own"
    try:
        file_lst = os.listdir(file_path)
        print(file_path)
        if len(file_lst) == 1:
                filename = file_lst[0]
                file_path = os.path.join(file_path, filename)
        else:
                return "첨부된 파일이 없습니다.!"
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return str(e)
@app.route('/save_changes2', methods=['POST'])
def save_changes2():
    id = request.args.get('id')
    if request.method == 'POST':
        uploaded_file = request.files['uploaded_file']  # 'uploaded_file' should match the input field name in your HTML form
        if uploaded_file:
            file_extension = os.path.splitext(uploaded_file.filename)[1]
            if id !='own':
                    file_path = os.path.join('users/'+session["username"]+"/resume", "Resume"+
                                             str(id)+file_extension)
            else:
                    file_path = os.path.join('users/'+session["username"]+"/resume_own", "Resume-own"+file_extension)
                    for filename in os.listdir('users/'+session["username"]+"/resume_own"):
                            file_path = os.path.join('users/'+session["username"]+"/resume_own", filename)
                            if os.path.isfile(file_path):
                                    os.remove(file_path)
            uploaded_file.save(file_path)

            return '"성공적으로 저장되었습니다.!"'
        else:
            return '오류가 발생했습니.!'
    return 'Invalid request'
@app.route('/save_changes3', methods=['POST'])
def save_changes3():
    id = request.args.get('id')
    if request.method == 'POST':
        uploaded_file = request.files['uploaded_file2']  # 'uploaded_file' should match the input field name in your HTML form
        if uploaded_file:
            file_extension = os.path.splitext(uploaded_file.filename)[1]
            if id !='own':
                    file_path = os.path.join('static/users/'+session["username"]+"/image", "img"+file_extension)
                    for filename in os.listdir('static/users/'+session["username"]+"/image"):
                            file_path = os.path.join('static/users/'+session["username"]+"/image", filename)
                            if os.path.isfile(file_path):
                                    os.remove(file_path)
            else:
                    file_path = os.path.join('static/users/'+session["username"]+"/image", "img"+file_extension)
                    for filename in os.listdir('static/users/'+session["username"]+"/image"):
                            file_path = os.path.join('static/users/'+session["username"]+"/image", filename)
                            if os.path.isfile(file_path):
                                    os.remove(file_path)
            uploaded_file.save(file_path)

            return '"성공적으로 저장되었습니다.!"'
        else:
            return '오류가 발생했습니.!'
    return 'Invalid request'

def update_user_info2(username,interests, phone_number):
    try:
        con2 = sq.connect("data/login_info.db")  #connect to database
        cursor = con2.cursor()

        
        if phone_number.strip() != "" and  len(interests) != 0:
            cursor.execute('UPDATE user SET phone = ? WHERE username = ?', (phone_number, username))
            cursor.execute('UPDATE user SET interest = ? WHERE username = ?', (', '.join(interests), username))

        elif phone_number.strip() != "" and  len(interests) == 0:
            cursor.execute('UPDATE user SET phone = ? WHERE username = ?', (phone_number, username))
        elif phone_number.strip() == "" and  len(interests) != 0:
            cursor.execute('UPDATE user SET interest = ? WHERE username = ?', (', '.join(interests), username))
        else:
                pass
        con2.commit()
        
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        con2.close()


@app.route('/update_user_info', methods=['POST'])
def update_user_info():
    try:
        username = session["username"]  # Assuming you have a way to identify the user
        new_phone_number = request.form.get('phone_number')
        interests = request.form.getlist('interests[]')

        if update_user_info2(username,interests, new_phone_number):
            return jsonify({'status': 'success', 'message': 'User information updated successfully'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to update user information'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__=="__main__":
        app.run(host='127.0.0.1', port=9000,debug=True)

