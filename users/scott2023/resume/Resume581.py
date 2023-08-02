lst = []
lst = [1,2,3]
print(len(lst)) # 3
# key & value
dic = {}
dic = dict()
dic = {"Scott":10,"Alice":15,"Bob":7}
print(dic["Alice"]) #15
print(len(dic))  # 3
# "Bob":3 
dic["Bob"] = 3

for value,key in dic.items():
	print(value, key)