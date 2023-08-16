import re # library for regular expression

# ^ --> does not allow to have any characters before the pattern
# $ --> no characters after pattern
pattern = r"\d{3}-\d{4}-\d{4}"
s = "my phone number is 010-1234-1234"

# re.search(), find a 'pattern' from string 's'
match = re.search(pattern,s)

if match:
	print("Valid")
else:
	print("Invalid")

# re.sub(pattern,replacement,string)
# re.sub() --> fint a substring with 'pattern', and subsitute to "" from s
no_phone = re.sub(pattern,"",s)

print(no_phone)

name = "Scott Kim"

pattern = r"^([a-zA-Z]+) ([a-zA-Z]+)$"

match = re.search(pattern,name)

if match:
	first_name = match.group(1)
	last_name = match.group(2)
	print("Valid")
	print(f"first name is {first_name}")
	print(f"last_name is {last_name}")
else:
	print("Invalid")

# IP address
# pattern of IP: #.#.#.#
#   # --> numbers between 0 to 255
# ex) 255.255.255.255 --> good
# ex) 255.255.255.300 --> invalid
# ex) 10.10.1.1 --> good
# ex) 10.10.1.1.10 --> invalid

ip = "10.256.1.1"
s = ip.split(".") # ['10', '10', '1', '1']
isValid = True
if len(s) != 4:
	isValid = False
for num in s:
	num = int(num)
	if num < 0 or num > 255:
		isValid = False

print(isValid)

def in_range(num):
	if num < 0 or num >255:
		return False
	return True 

ip = "10.256.1.1"
pattern = r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$"

match = re.search(pattern,ip)
if match:
	first = match.group(1)
	second = match.group(2)
	third = match.group(3)
	last = match.group(4)
	# checks whetehr the numbers are between 0-255
	if in_range(first) and in_range(second) and in_range(third) and in_range(last):
		print("Valid")
	else:
		print("Invalid")
	print("valid")
else:
	print("invalid")


import pandas as pd
# types of variables in python
# int,boolean,float,string, list...

# There are new types that are provided from pandas
# Series --> Column in a table
# DataFrame --> Data table
sample_lst = [10,20,"Scott"]
print(sample_lst)
# Series --> each series can contain only one type
lst = [10,20,30,40,50]
index_labels = ["A","B","C","D","E"]
series = pd.Series(lst, index = index_labels)
print(lst)
print(series)

data = {"Name": ["Alice","Scott","Bob"],
        "Age": [10,20,30]}
df = pd.DataFrame(data)
print(data)
print(df)
print(df["Name"]) # Print "Name" Series

data = pd.read_csv("student_marks.csv")
# print first 5 rows
print(data.head(5))
print(data.info())
# Access to any columns
# data_name[column name]
print(data["Student_ID"])
# Access to row
print(data.iloc[0]) # print first row

# Filtering Data
# stduents who got over 90 stores in to data_test1
data_test1 = data[(data["Test_1"]>90) & (data["Test_2"]>90) ]
print(data_test1)

# get average of series
print("Average of Test1:", data["Test_1"].mean())
print("Median of Test1:", data["Test_1"].median())
print("Highest of Test1:", data["Test_1"].max())
print("Lowest of Test1:", data["Test_1"].min())
print(data["Test_1"].describe())


data["Total"] = data["Test_1"]
for i in range(2,13):
        data["Total"] = data["Total"] + data["Test_"+str(i)]
print(data.head(3))
data["Average"] = data["Total"]/12
print(data.head(10))

sorted_data = data.sort_values(by ="Average",ascending=False)
print(sorted_data.head(10))

data.dropna() # Drop rows with missing values
data.fillna(90) # fill missing values with a specific value

def numeric_to_letter(score):
        if score >= 90:
                return "A"
        elif score >= 80:
                return "B"
        elif score >= 70:
                return "C"
        elif score >= 60:
                return "D"
        else:
                return "F"
data = data.fillna(90)
data["Letter Grade"] = data["Average"].apply(numeric_to_letter)
print(data.head(10))
# data["Test_1"] = data["Test_1"].apply(numeric_to_letter)
# print(data.head(10))

import matplotlib.pyplot as plt

a = [1,2,3,4,5,6,7]
b = [30,40,50,45,55,60,70]
b2 = [25,30,40,45,55,65,75]
# line graph
# plt.plot(a,b, color="#C5957A",marker='x',label = "Sample1")
# plt.plot(a,b2, color="blue",marker='o',label = "Sample2")
# plt.legend()
# plt.xlabel("Days")
# plt.ylabel("Values")
# plt.grid(True)
# plt.savefig("graph1.png")
# plt.show()

# countries = ["Korea","USA","Japan"]
# values = [10,20,15]
# color = ["red","blue","green"]
# plt.xlabel("Countries")
# plt.ylabel("Values")
# # plt.grid(True)
# plt.bar(countries,values, color = color,edgecolor="black",width=0.2,hatch="/")
# plt.show()


# plt.scatter(a,b, color="#C5957A",marker='x',label = "Sample1")
# plt.scatter(a,b2, color="blue",marker='o',label = "Sample2")
# plt.legend()
# plt.xlabel("Days")
# plt.ylabel("Values")
# plt.grid(True)
# plt.savefig("graph1.png")
# plt.show()

# index = []
# for i in range(56):
#         index.append(i)
# plt.scatter(index,data["Average"])
# plt.show()

data_student1 = data.iloc[1]
# gets all the column names and save them as a list
lst = data.columns.tolist()
lst.remove("Total")
lst.remove("Average")
lst.remove("Letter Grade")
lst.remove("Student_ID")

print(lst)
scores = []
for i in range(1,13):
        scores.append(data_student1["Test_"+str(i)])
print(scores)
plt.figure(figsize=(7,5))
plt.plot(lst,scores)
plt.tight_layout()
plt.show()

# homework
# Draw Bar Chart
# x axis --> Test1, test2...test12
# y axis --> average score for each test
# Try to change colors, labels, ...







