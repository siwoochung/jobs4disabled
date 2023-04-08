import pandas as pd
from ast import literal_eval

def pick_jobs(n):
	NUMS = n
	data = pd.read_csv("data/temp_data.csv")
	random_data = data.sample(n=NUMS)
	name = random_data["모집직종"].tolist()
	hire_type = random_data["고용형태"].tolist()
	location = random_data["사업장 주소"].tolist()
	company_type = random_data["기업형태"].tolist()
	job_class = random_data["Classification"].tolist()
	pay_type = random_data["임금형태"].tolist()
	required_degree = random_data["요구학력"].tolist()
	required_work = random_data["요구경력"].tolist()


	final_lst=[]
	for i in range(NUMS):
		dic = dict()  #{}
		dic["이름"]=name[i]

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

		dic["분류"]=job_class[i]

		dic["임금형태"]=pay_type[i]
		if pay_type[i]==0:
			dic["임금형태"]="시급"
		elif pay_type[i]==1:
			dic["임금형태"]="일급"
		elif pay_type[i]==2:
			dic["임금형태"]="월급"
		else:
			dic["임금형태"]="연봉"

		dic["요구학력"]=required_degree[i]
		if required_degree[i]==0:
			dic["요구학력"]="학무관"
		elif required_degree[i]==1:
			dic["요구학력"]="고졸"
		elif required_degree[i]==2:
			dic["요구학력"]="초대졸"
		else:
			dic["요구학력"]="대졸"

		dic["요구경력"]=required_work[i]
		final_lst.append(dic)

	return final_lst

pick_jobs(10)

#data["Classification"] = data["Classification"].apply(literal_eval)

#print(data["Classification"])
# print(data.sample(n=10))





# 	print(i+1,name[i],hire_type[i],location[i],company_type[i],job_class[i])

# print(final_lst)
# classification = input("Enter a prefer job")
