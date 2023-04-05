import pandas
from sklearn.metrics.pairwise import cosine_similarity

data_mock = pandas.read_csv("mock_data.csv")
data = pandas.read_csv("data/job_data.csv")

print(data_mock)
print(data)

merge_data = pandas.merge(data_mock, data, on="연번")

print(merge_data) 

job_user_rating = merge_data.pivot_table('rating',index="모집직종",columns="userid")

job_user_rating.fillna(0,inplace=True)

print(job_user_rating)

similarity = cosine_similarity(job_user_rating)
print(similarity)

final_data = pandas.DataFrame(data=similarity,index=job_user_rating.index,columns=job_user_rating.index)
print(final_data)

#Choose the 5 jobs' title that has the highest similarity score with title
def get_best5(title):
	return final_data[title].sort_values(ascending=False)[:6]

a = get_best5("건물 청소원(공공건물,아파트,사무실,병원,상가,공장 등)")

print(a)