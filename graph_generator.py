import pandas as pd
from calculate_income import convert, get_average, compare_income


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

print(income_compare())
