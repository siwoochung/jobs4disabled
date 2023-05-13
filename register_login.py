import sqlite3 as sq

# conn = sq.connect("data/login_info.db")  #connect to database

# cur = conn.cursor() #create cursor for execute SQL in python

# conn.execute('INSERT INTO user(username, password, age, gender, phone, interest) Values ("alice2023", "abcde", 20, "M", "01012345678", "IT")')

# conn.commit() #save data

# conn.close() #end connection

#Function for sign-up page
def register(username, password, age, gender, phone, interest):
	conn = sq.connect("data/login_info.db")  #connect to database
	cur = conn.cursor() #create cursor for execute SQL in python
	try:
		conn.execute('INSERT INTO user(username, password, age, gender, phone, interest) Values (?, ?, ?, ?, ?, ?)',(username, password, age, gender, phone, interest))
	except sq.IntegrityError:
		print("Already have " + username)
	conn.commit() #save data
	conn.close() #end connection

#Function for login-page
def login_check(username,password):  #compare password of user input with password of DB
	conn = sq.connect("data/login_info.db")
	cur = conn.cursor()
	cur.execute('SELECT password FROM user WHERE username = (?)',(username,))
	user = cur.fetchone() 
	conn.close() #Close DataBase
	if user == None:
		return False
	pass_DB = user[0] #password from DB
	if pass_DB == password:
		return True
	else:
		return False



