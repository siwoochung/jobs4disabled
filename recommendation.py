import pandas as pd
from ast import literal_eval
from calculate_income import convert, get_average, compare_income
from naver_distance import calculate_distance
import random

data = pd.read_csv("data/temp_data.csv")
def get_average():
	return data["pay_month"].mean()

def compare_income(x):
	average_income = get_average()
	p = (abs(x-average_income))/((x+average_income) / 2) * 100
	if x < average_income:
		p = p * -1
	return p


def pick_jobs(n):
	NUMS = n
	data["pay_month"] = data['임금'].apply(convert)
	data["pay_month_diff"] = data["pay_month"].apply(compare_income)
	random_data = data.sample(n=NUMS)


	name = random_data["모집직종"].tolist()
	hire_type = random_data["고용형태"].tolist()
	pay = random_data["임금"].tolist()
	paytype = random_data["임금형태"].tolist()
	location = random_data["사업장 주소"].tolist()
	company_type = random_data["기업형태"].tolist()
	job_class = random_data["Classification"].tolist()
	required_degree = random_data["요구학력"].tolist()
	required_work = random_data["요구경력"].tolist()
	company = random_data["Company"].tolist()
	address = random_data["사업장 주소"].tolist()
	job_id = random_data["id"].tolist()

	pay_month = random_data["pay_month"].tolist()
	pay_month_diff = random_data["pay_month_diff"].tolist()

	final_lst=[]
	# i = 0
	# while i < NUMS:
	for i in range(NUMS):
		# if (calculate_distance(address[i])>60):
		# 	continue

		dic = dict()  #{}
		dic["Company"] = company[i]
		dic["모집직종"]= name[i]
		dic["add"]= calculate_distance(address[i])
		dic["id"]= job_id[i]

		
		pay_month_diff[i] = round(pay_month_diff[i],1)
		dic["pay_month_diff"] = pay_month_diff[i]
		dic["percent"] = random.randint(20,100)

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
		# i +=1
		

	return final_lst

def pick_jobs_class(data):
	name = data["모집직종"].tolist()
	hire_type = data["고용형태"].tolist()
	location = data["사업장 주소"].tolist()
	company_type = data["기업형태"].tolist()
	job_class = data["Classification"].tolist()
	pay_type = data["임금형태"].tolist()
	required_degree = data["요구학력"].tolist()
	required_work = data["요구경력"].tolist()


	# final_lst=[]
	# for i in range(len(name)):
	# 	dic = dict()  #{}
	# 	dic["모집직종"]=name[i]
	# 	# dic[""]=company[i]

	# 	dic["고용형태"]=hire_type[i]
	# 	if hire_type[i]==0:
	# 		dic["고용형태"] = "계약직"
	# 	elif hire_type[i]==1:
	# 		dic["고용형태"] = "상용직"
	# 	else:
	# 		dic["고용형태"] = "시간제"

	# 	dic["사업장 주소"]=location[i]

	# 	dic["기업형태"]=company_type[i]
	# 	if company_type[i]==0:
	# 		dic["기업형태"]="개인"
	# 	elif company_type[i]==1 or company_type[i]==5:
	# 		dic["기업형태"]="중소"
	# 	elif company_type[i]==2:
	# 		dic["기업형태"]="협회,단체"
	# 	elif company_type[i]==3:
	# 		dic["기업형태"]="공사,공공"
	# 	elif company_type[i]==4:
	# 		dic["기업형태"]="대기업"

	# 	dic["Classification"]=job_class[i]

	# 	dic["임금형태"]=pay_type[i]
	# 	if pay_type[i]==0:
	# 		dic["임금형태"]="시급"
	# 	elif pay_type[i]==1:
	# 		dic["임금형태"]="일급"
	# 	elif pay_type[i]==2:
	# 		dic["임금형태"]="월급"
	# 	else:
	# 		dic["임금형태"]="연봉"

	# 	dic["요구학력"]=required_degree[i]
	# 	if required_degree[i]==0:
	# 		dic["요구학력"]="학무관"
	# 	elif required_degree[i]==1:
	# 		dic["요구학력"]="고졸"
	# 	elif required_degree[i]==2:
	# 		dic["요구학력"]="초대졸"
	# 	else:
	# 		dic["요구학력"]="대졸"

	# 	dic["요구경력"]=required_work[i]
	# 	final_lst.append(dic)

	# return final_lst

def pick_jobs_filter_by_class(n,business_checked,it_checked, design_checked, trade_checked,education_checked, medical_checked, service_checked, produce_checked, special_checked):
	NUMS = n
	data = pd.read_csv("data/temp_data.csv")
	count = 0
	data_business = pd.DataFrame()
	data_it = pd.DataFrame()
	data_design = pd.DataFrame()
	data_trade = pd.DataFrame()
	data_education = pd.DataFrame()
	data_medical = pd.DataFrame()
	data_service = pd.DataFrame()
	data_produce = pd.DataFrame()
	data_special = pd.DataFrame()

	if business_checked:
		data_business = data[data["Classification"]=="경영/사무"]
		count += 1
	if it_checked:
		data_it = data[data["Classification"]=="IT/인터넷"]
		count += 1
	if design_checked:
		data_design = data[data["Classification"]=="디자인"]
		count += 1
	if trade_checked:
		data_trade = data[data["Classification"]=="무역/유통"]
		count += 1
	if education_checked:
		data_education = data[data["Classification"]=="교육"]
		count += 1
	if medical_checked:
		data_medical = data[data["Classification"]=="의료"]
		count += 1
	if service_checked:
		data_service = data[data["Classification"]=="서비스"]
		count += 1
	if produce_checked:
		data_produce = data[data["Classification"]=="생산/제조"]
		count += 1
	if special_checked:
		data_special = data[data["Classification"]=="전문/특수직"]
		count += 1

	show = 10 // count
	rem = 10 % count
	final_data = pd.DataFrame()

	final_lst = []
	if not data_business.empty:
		random_business = data_business.sample(n=show)
		final_lst.append(random_business)
	if not data_it.empty:
		random_it = data_it.sample(n=show)
		final_lst.append(random_it)
	if not data_design.empty:
		random_design = data_design.sample(n=show)
		final_lst.append(random_design)
	if not data_trade.empty:
		random_trade = data_trade.sample(n=show)
		final_lst.append(random_trade)
	if not data_education.empty:
		random_education = data_education.sample(n=show)
		final_lst.append(random_education)
	if not data_medical.empty:
		random_medical = data_medical.sample(n=show)
		final_lst.append(random_medical)
	if not data_service.empty:
		random_service = data_service.sample(n=show)
		final_lst.append(random_service)
	if not data_produce.empty:
		random_produce = data_produce.sample(n=show)
		final_lst.append(random_produce)
	if not data_special.empty:
		random_special = data_special.sample(n=show)
		final_lst.append(random_special)

	final_data = pd.concat(final_lst)
	final_data=pick_jobs_class(final_data)

	return final_data

print(pick_jobs_filter_by_class(10,True,True,False,True,False,False,False,False,False))


def pick_jobs_filter_by_hire_type(n,d,contract_checked, fulltime_checked, parttime_checked):
	data = pd.DataFrame(d)
	NUMS = n
	count = 0
	data_contract = pd.DataFrame()
	data_fulltime = pd.DataFrame()
	data_parttime = pd.DataFrame()

	if contract_checked:
		data_contract = data[data["고용형태"]=="계약직"]
		count += 1
	if fulltime_checked:
		data_fulltime = data[data["고용형태"]=="상용직"]
		count += 1
	if parttime_checked:
		data_parttime = data[data["고용형태"]=="시간제"]
		count += 1

	show = 3 // count
	rem = 3 % count
	final_data = pd.DataFrame()

	final_lst = []
	try: 
		if not data_contract.empty:
			random_contract = data_contract.sample(n=show)
			final_lst.append(random_contract)
		if not data_fulltime.empty:
			random_fulltime = data_fulltime.sample(n=show)
			final_lst.append(random_fulltime)
		if not data_parttime.empty:
			random_parttime = data_parttime.sample(n=show)
			final_lst.append(random_parttime)
	except ValueError:
		pass

	final_data = pd.concat(final_lst)
	final_data=pick_jobs_filter_by_hire_type(final_data)

	return final_data

def pick_jobs_filter_by_company_type(n,private_checked,medium_checked, group_checked, public_checked,big_checked):
	NUMS = n
	data = pd.read_csv("data/temp_data.csv")
	count = 0
	data_private = pd.DataFrame()
	data_medium = pd.DataFrame()
	data_group = pd.DataFrame()
	data_public = pd.DataFrame()
	data_big = pd.DataFrame()

	if private_checked:
		data_private = data[data["기업형태"]=="개인"]
		count += 1
	if medium_checked:
		data_medium = data[data["기업형태"]=="중소"]
		count += 1
	if group_checked:
		data_group = data[data["기업형태"]=="협회,단체"]
		count += 1
	if public_checked:
		data_public = data[data["기업형태"]=="공사,공공"]
		count += 1
	if big_checked:
		data_big= data[data["기업형태"]=="대기업"]
		count += 1

	show = 5 // count
	rem = 5 % count
	final_data = pd.DataFrame()

	final_lst = []
	if not data_private.empty:
		random_private = data_private.sample(n=show)
		final_lst.append(random_private)
	if not data_medium.empty:
		random_medium = data_medium.sample(n=show)
		final_lst.append(random_it)
	if not data_group.empty:
		random_group = data_group.sample(n=show)
		final_lst.append(random_design)
	if not data_public.empty:
		random_public = data_public.sample(n=show)
		final_lst.append(random_trade)
	if not data_big.empty:
		random_big = data_big.sample(n=show)
		final_lst.append(random_education)

	final_data = pd.concat(final_lst)
	final_data=pick_jobs_filter_by_company_type(final_data)

	return final_data

def pick_jobs_filter_by_required_degree(n,none_checked,highschool_checked, precollege_checked,college_checked):
	NUMS = n
	data = pd.read_csv("data/temp_data.csv")
	count = 0
	data_none = pd.DataFrame()
	data_highschool = pd.DataFrame()
	data_precollege = pd.DataFrame()
	data_college = pd.DataFrame()

	if none_checked:
		data_none = data[data["요구학력"]=="학력무관"]
		count += 1
	if highschool_checked:
		data_highschool = data[data["요구학력"]=="고졸"]
		count += 1
	if precollege_checked:
		data_precollege = data[data["요구학력"]=="초대졸"]
		count += 1
	if college_checked:
		data_precollege = data[data["요구학력"]=="대졸"]
		count += 1

	show = 4 // count
	rem = 4 % count
	final_data = pd.DataFrame()

	final_lst = []
	if not data_none.empty:
		random_none = data_none.sample(n=show)
		final_lst.append(random_none)
	if not data_highschool.empty:
		random_highschool = data_highschool.sample(n=show)
		final_lst.append(random_highschool)
	if not data_precollege.empty:
		random_precollege = data_precollege.sample(n=show)
		final_lst.append(random_precollege)
	if not data_college.empty:
		random_college = data_college.sample(n=show)
		final_lst.append(random_college)

	final_data = pd.concat(final_lst)
	final_data=pick_jobs_filter_by_required_degree(final_data)

	return final_data

print(pick_jobs(10))
#data["Classification"] = data["Classification"].apply(literal_eval)

