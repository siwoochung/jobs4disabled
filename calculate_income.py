import pandas as pd


def convert(x):
	if x<100000:
		x = x * 200
	elif x > 10000000:
		x = x / 12
	return x

# data = pd.read_csv("data/temp_data.csv")
# data["pay_month"] = data['임금'].apply(convert)

# print(data["pay_month"].head(10))

def get_average():
	return data["pay_month"].mean()

def compare_income(x):
	average_income = get_average()
	p = (abs(x-average_income))/((x+average_income) / 2) * 100
	if x < average_income:
		p = p * -1
	return p

# data["pay_month_diff"] = data["pay_month"].apply(compare_income)

# print(data["pay_month_diff"].head(10))