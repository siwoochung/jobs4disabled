# File I/O -

# File input/Output is the ability of a program to take a file
# as input or create a file as output


# open -> is a functionality built into Python that allows you to open a file
#          and utilize it in your program,
#         open allow you to read/write the file

# 'w' --> overwriting, 'r' --> reading
# f = open("sample.txt","w")
# f.write("Bye World!")
# f.close()


# name = input("What is your name?")
# f = open("names.txt","w") # this will create a file name 'names.txt'
# f.write(name) # write the name in file 'f'
# f.close()

# 'a' --> append
# name = input("What is your name?")
# f = open("names.txt","a")
# # \n -> new line --> Enter
# f.write(name+"\n") # write itself does not go to next line
# f.close()

# name = input("What is your name?")
# f = open("names.txt","a")
# # \n -> new line --> Enter
# f.write(f"Hello, {name}!\n") # write itself does not go to next line
# f.close()

# with --> the keyword with allows you to automate the closing of
#          a file
# name = input("What is your name?")
# with open("names.txt","a") as f:
#     f.write(f"Hello, {name}!\n")
with open("names.txt","r") as f:
    # read whole lines of the file, and store each line as an item of the list
    lines = f.readlines()

print(lines) # ['Alice\n', 'Scott\n', 'Bob\n', 'Jason\n', 'John\n']

for line in lines:
    print(line.strip()) # strip removes \n


with open("names.txt","r") as f:
    # read whole lines of the file, and store each line as an item of the list
    lines = f.readlines()

names = []
for line in lines:
    names.append(line.strip()) # strip removes \n
print(names)

names = sorted(names)
print(names)

# use 'w' to overate the file
with open("names.txt","w") as f:
    for name in names:
        f.write(name+"\n")

# .csv --> comma seperated values
# Harry,Gryffindor
# Ron,Gryffindor
# Draco,Slytherin
# with open("students.csv","r") as f:
#     for line in f:
#         row = line.strip().split(",")
#         print(f"Student Name: {row[0]}, House Name: {row[1]}")
#
# # Diciontary --> each item has a key and value
# student = {}
# student["name"] = "Scott"
# print(student)
# student["age"] = 20
# print(student)


# Read students.csv,
# then create a list of dictionaries that contain student information
# expected output:
# [{"name": "Harry","house":"Gryffindor"},{"name": "Ron","house":"Gryffindor"},
#   {"name": "Draco","house":"Slytherin"}]
# lst_students = []
# with open("students.csv", "r") as file:
#     for line in file:
#         line = line.strip() # To remove every \n or whitespace
#         values = line.split(",") # splich each row by comma
#         student = {"name":values[0],'house':values[1]}
#         lst_students.append(student)
# print(lst_students)
# import csv # csv is a library for doing something with csv
# with open("students.csv", "r") as file:
#     csv_reader = csv.DictReader(file)
#     for row in csv_reader:
#         print(row)
# import csv
# # csv.DictWriter --> write a csv file
# name = input("What's your name? ")
# house = input("Where's your home? ")
# with open("students.csv","a") as file:
#     csv_writer = csv.DictWriter(file, fieldnames=["name","house"])
#     csv_writer.writerow({"name":name, "house":house})

# Read sample.py and prints the number of lines of that file
# But, Do not count the comment(the row starts with '#') and Empty line

with open("sample.py","r") as file:
    lines = file.readlines() #["# Say hello", " ","name = input("What's your name? ")
    num_lines = 0
    for line in lines:
        line = line.strip()
        if len(line) <= 0:
            continue
        if line[0] == "#":
            continue
        if line == "":
            continue
        num_lines += 1
print(num_lines)