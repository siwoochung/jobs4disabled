import pandas as pd
from calculate_income import convert, get_average, compare_income
from naver_distance import calculate_distance
import random

data = pd.read_csv("data/temp_data.csv")
def income_compare():
        income_lst = data["임금"].tolist()
        for i in range(len(income_lst)):
                income_lst[i] = convert(income_lst[i])
        
        income_lst = sorted(income_lst, reverse=True)
        num_elements = int(len(income_lst) * 0.25)
        top25 = income_lst[:num_elements]
        top25_avg = sum(top25) / len(top25)
        average = sum(income_lst) / len(income_lst)

        income_lst = sorted(income_lst, reverse=False)
        low25 = income_lst[:num_elements]
        low25_avg = sum(low25) / len(low25)

        return [round(average,0) ,round(top25_avg,0),round(low25_avg,0)]

def similarity_graph():
        lst = []
        for i in range(100):
                lst.append(random.randint(0,100))
        percent_lst = lst
        count10 = 0
        count30 = 0
        count50 = 0
        count70 = 0
        count90 = 0
        count100 = 0
        for i in percent_lst:
                if 0<= i <= 10:
                        count10 +=1
                elif 10 < i <=30:
                        count30 +=1
                elif 30 < i <=50:
                        count50 +=1
                elif 50 < i <=70:
                        count50 +=1
                elif 70 < i <=90:
                        count50 +=1
                else:
                        count100 +=1

        return [count10,count30,count50,count70,count90,count100]