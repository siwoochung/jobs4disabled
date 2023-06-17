import pandas
import requests

url = "https://www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId=FILE_000000002738628&fileDetailSn=1&insertDataPrcus=N"  # Replace with the actual file download URL

response = requests.get(url)

if response.status_code == 200:
    with open("data.csv", "wb") as file:
        file.write(response.content)
    print("File downloaded successfully.")
else:
    print("Failed to download the file.")

data = pandas.read_csv("data.csv")

print(data)
print(data.head(10))    # print first 10 rows of data 
print(data["요구자격증"].isna().count())

data["요구자격증"] = data["요구자격증"].fillna(value=0)

data["전공계열"] = data["전공계열"].fillna(value=0)

print(data["요구자격증"])
print(data["전공계열"])

data = data.fillna(value=0)  #fill out every empty data with 0 

data_by_typeP = data.groupby("임금형태").count()
print(data_by_typeP)

data_by_typeH = data.groupby("고용형태").count()
print(data_by_typeH)

data_recommend= data.drop(columns=["연번","구인신청일자","모집기간","입사형태","담당기관","등록일","연락처"])
print(data_recommend)

data_month = data_recommend[data_recommend["임금형태"]=="월급"]
data_hour = data_recommend[data_recommend["임금형태"]=="시급"]
data_day = data_recommend[data_recommend["임금형태"]=="일급"]
data_year = data_recommend[data_recommend["임금형태"]=="연봉"]
print(data_month)

import matplotlib.pyplot as plt

list = [data_month["임금"].count(),data_year["임금"].count(), data_hour["임금"].count(), data_day["임금"].count()]
list_label=["Monthly","Yearly","Hourly","Daily"]
colors= ["006880","968EAF","red","yellow"]
# plt.bar(list_label,list)  # plt.plot is line graph
# plt.ylabel("Number of Jobs")
# plt.xlabel("Payment Type")
# plt.title("Number of Jobs by Payment Type")
# plt.show()
# plt.plt(list,labels=list_label,colors=colors)
# plt.show()

print(data_hour.describe())
print(data_hour[data_hour["임금"]==100])
print(data_hour[data_hour["임금"]==17033])

print(data_month.describe())
print(data_month[data_month["임금"]==3500000])
print(data_month[data_month["임금"]==538720])

print(data_year.describe())

data_year["임금(월급)"] = data_year["임금"] / 12
print(data_year)

print(data_recommend["고용형태"].value_counts())   #계약직-0,상용직-1,시간제-2
print(data_recommend["임금형태"].value_counts())   #시급-0,일급-1,월급-2,연봉-3
print(data_recommend["요구학력"].value_counts())   #무관-0,고졸-1,초대졸-2,대졸-3
print(data_recommend["요구경력"].value_counts())  
#less than 12 months-->무관
# 무관, 0년개월, 0년12개월, 0년0개월, 0년 3개월-0
# 1년0개월, 1년개월--1
# 3년개월--2
print(data_recommend["기업형태"].value_counts())
# 개인-0
# 중소-1
# 협회,단체-2
# 공사,공공-3
# 대기업-4
# 중소-5

data_recommend.loc[data_recommend["고용형태"]=="계약직","고용형태"] = 0 		#change 계약직 to 0
data_recommend.loc[data_recommend["고용형태"]=="상용직","고용형태"] = 1
data_recommend.loc[data_recommend["고용형태"]=="시간제","고용형태"] = 2

data_recommend.loc[data_recommend["임금형태"]=="시급","임금형태"] = 0
data_recommend.loc[data_recommend["임금형태"]=="일급","임금형태"] = 1
data_recommend.loc[data_recommend["임금형태"]=="월급","임금형태"] = 2
data_recommend.loc[data_recommend["임금형태"]=="연봉","임금형태"] = 3

data_recommend.loc[data_recommend["요구경력"].str[0]=="0","요구경력"]=0
data_recommend.loc[data_recommend["요구경력"].str[0]=="1","요구경력"]=1
data_recommend.loc[data_recommend["요구경력"].str[0]=="2","요구경력"]=2
data_recommend.loc[data_recommend["요구경력"].str[0]=="3","요구경력"]=3
data_recommend.loc[data_recommend["요구경력"].str[0:]=="무관","요구경력"]=0
try:
	data_recommend.loc[data_recommend["요구경력"].str[0].astype(int) > 3 ,"요구경력"]=4
except:
	print("No 요구경력 more than 3 years")

data_recommend.loc[data_recommend["요구학력"]=="무관","요구학력"] = 0
data_recommend.loc[data_recommend["요구학력"]=="고졸","요구학력"] = 1
data_recommend.loc[data_recommend["요구학력"]=="초대졸","요구학력"] = 2
data_recommend.loc[data_recommend["요구학력"]=="대졸","요구학력"] = 3

data_recommend.loc[data_recommend["기업형태"]=="개인","기업형태"] = 0
data_recommend.loc[data_recommend["기업형태"]=="중소","기업형태"] = 1
data_recommend.loc[data_recommend["기업형태"]=="협회,단체","기업형태"] = 2
data_recommend.loc[data_recommend["기업형태"]=="공사,공공","기업형태"] = 3
data_recommend.loc[data_recommend["기업형태"]=="대기업","기업형태"] = 4
data_recommend.loc[data_recommend["기업형태"]=="중소","기업형태"] = 5

print(data_recommend)


data_temp = data_recommend.drop(columns=["모집직종","전공계열","사업장 주소","기업형태","요구자격증"])

# from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances

# similarity_table = cosine_similarity(data_temp,data_temp)
# print(similarity_table)

similarity_table = euclidean_distances(data_temp,data_temp)
print(similarity_table)

similarity_df = pandas.DataFrame(similarity_table,index=data_temp.index,columns=data_temp.index)
print(similarity_df)


data_recommend.loc[data_recommend["모집직종"].str.contains("사무"),"Classification"] = "경영/사무"
data_recommend.loc[data_recommend["모집직종"].str.contains("전산"),"Classification"] = "경영/사무"
data_recommend.loc[data_recommend["모집직종"].str.contains("입력"),"Classification"] = "경영/사무"
data_recommend.loc[data_recommend["모집직종"].str.contains("마케터"),"Classification"] = "경영/사무"

data_recommend.loc[data_recommend["모집직종"].str.contains("개발자"),"Classification"] = "IT/인터넷"
data_recommend.loc[data_recommend["모집직종"].str.contains("프로그래머"),"Classification"] = "IT/인터넷"
data_recommend.loc[data_recommend["모집직종"].str.contains("프로그래밍"),"Classification"] = "IT/인터넷"
data_recommend.loc[data_recommend["모집직종"].str.contains("IT"),"Classification"] = "IT/인터넷"
data_recommend.loc[data_recommend["모집직종"].str.contains("제도"),"Classification"] = "IT/인터넷"

data_recommend.loc[data_recommend["모집직종"].str.contains("디자인"),"Classification"] = "디자인"
data_recommend.loc[data_recommend["모집직종"].str.contains("디자이너"),"Classification"] = "디자인"

data_recommend.loc[data_recommend["모집직종"].str.contains("택배"),"Classification"] = "무역/유통"
data_recommend.loc[data_recommend["모집직종"].str.contains("운반"),"Classification"] = "무역/유통"

data_recommend.loc[data_recommend["모집직종"].str.contains("교사"),"Classification"] = "교육"
data_recommend.loc[data_recommend["모집직종"].str.contains("상담"),"Classification"] = "교육"

data_recommend.loc[data_recommend["모집직종"].str.contains("병원"),"Classification"] = "의료"
data_recommend.loc[data_recommend["모집직종"].str.contains("의료"),"Classification"] = "의료"
data_recommend.loc[data_recommend["모집직종"].str.contains("복지"),"Classification"] = "의료"

data_recommend.loc[data_recommend["모집직종"].str.contains("안마"),"Classification"] = "서비스"
data_recommend.loc[data_recommend["모집직종"].str.contains("경비"),"Classification"] = "서비스"
data_recommend.loc[data_recommend["모집직종"].str.contains("정리"),"Classification"] = "서비스"
data_recommend.loc[data_recommend["모집직종"].str.contains("사서"),"Classification"] = "서비스"
data_recommend.loc[data_recommend["모집직종"].str.contains("검침"),"Classification"] = "서비스"
data_recommend.loc[data_recommend["모집직종"].str.contains("점검"),"Classification"] = "서비스"
data_recommend.loc[data_recommend["모집직종"].str.contains("조리"),"Classification"] = "서비스"
data_recommend.loc[data_recommend["모집직종"].str.contains("급식"),"Classification"] = "서비스"
data_recommend.loc[data_recommend["모집직종"].str.contains("서비스"),"Classification"] = "서비스"
data_recommend.loc[data_recommend["모집직종"].str.contains("세탁"),"Classification"] = "서비스"
data_recommend.loc[data_recommend["모집직종"].str.contains("미화원"),"Classification"] = "서비스"
data_recommend.loc[data_recommend["모집직종"].str.contains("청소"),"Classification"] = "서비스"
data_recommend.loc[data_recommend["모집직종"].str.contains("모니터"),"Classification"] = "서비스"
data_recommend.loc[data_recommend["모집직종"].str.contains("고객상담"),"Classification"] = "서비스"
data_recommend.loc[data_recommend["모집직종"].str.contains("안내"),"Classification"] = "서비스"
data_recommend.loc[data_recommend["모집직종"].str.contains("요리"),"Classification"] = "서비스"
data_recommend.loc[data_recommend["모집직종"].str.contains("수리"),"Classification"] = "서비스"
data_recommend.loc[data_recommend["모집직종"].str.contains("네일"),"Classification"] = "서비스"
data_recommend.loc[data_recommend["모집직종"].str.contains("방역"),"Classification"] = "서비스"
data_recommend.loc[data_recommend["모집직종"].str.contains("운전"),"Classification"] = "서비스"
data_recommend.loc[data_recommend["모집직종"].str.contains("요양"),"Classification"] = "서비스"
data_recommend.loc[data_recommend["모집직종"].str.contains("관리"),"Classification"] = "서비스"
data_recommend.loc[data_recommend["모집직종"].str.contains("영양"),"Classification"] = "서비스"
data_recommend.loc[data_recommend["모집직종"].str.contains("진열"),"Classification"] = "서비스"
data_recommend.loc[data_recommend["모집직종"].str.contains("주방"),"Classification"] = "서비스"
data_recommend.loc[data_recommend["모집직종"].str.contains("조경"),"Classification"] = "서비스"
data_recommend.loc[data_recommend["모집직종"].str.contains("머천다이저"),"Classification"] = "서비스"
data_recommend.loc[data_recommend["모집직종"].str.contains("MD"),"Classification"] = "서비스"
data_recommend.loc[data_recommend["모집직종"].str.contains("판매"),"Classification"] = "서비스"
data_recommend.loc[data_recommend["모집직종"].str.contains("서빙"),"Classification"] = "서비스"

data_recommend.loc[data_recommend["모집직종"].str.contains("제조"),"Classification"] = "생산/제조"
data_recommend.loc[data_recommend["모집직종"].str.contains("조작"),"Classification"] = "생산/제조"
data_recommend.loc[data_recommend["모집직종"].str.contains("식품"),"Classification"] = "생산/제조"
data_recommend.loc[data_recommend["모집직종"].str.contains("전기"),"Classification"] = "생산/제조"
data_recommend.loc[data_recommend["모집직종"].str.contains("전자"),"Classification"] = "생산/제조"
data_recommend.loc[data_recommend["모집직종"].str.contains("섬유"),"Classification"] = "생산/제조"
data_recommend.loc[data_recommend["모집직종"].str.contains("의복"),"Classification"] = "생산/제조"
data_recommend.loc[data_recommend["모집직종"].str.contains("조립"),"Classification"] = "생산/제조"
data_recommend.loc[data_recommend["모집직종"].str.contains("생산"),"Classification"] = "생산/제조"
data_recommend.loc[data_recommend["모집직종"].str.contains("기계"),"Classification"] = "생산/제조"
data_recommend.loc[data_recommend["모집직종"].str.contains("금속"),"Classification"] = "생산/제조"
data_recommend.loc[data_recommend["모집직종"].str.contains("재봉"),"Classification"] = "생산/제조"
data_recommend.loc[data_recommend["모집직종"].str.contains("수선"),"Classification"] = "생산/제조"
data_recommend.loc[data_recommend["모집직종"].str.contains("제과"),"Classification"] = "생산/제조"
data_recommend.loc[data_recommend["모집직종"].str.contains("제빵"),"Classification"] = "생산/제조"

data_recommend.loc[data_recommend["모집직종"].str.contains("운동선수"),"Classification"] = "전문/특수직"
data_recommend.loc[data_recommend["모집직종"].str.contains("연구"),"Classification"] = "전문/특수직"
data_recommend.loc[data_recommend["모집직종"].str.contains("지휘"),"Classification"] = "전문/특수직"



data_recommend.to_csv("temp_data.csv")

temp_data = pandas.read_csv("temp_data.csv")
pandas.set_option('display.max_rows',None)
print(temp_data)

# 80% - Train (640), 20% - Test (160)
from sklearn.model_selection import train_test_split

X_train, X_test, Y_train, Y_test = train_test_split(data_recommend["모집직종"],data_recommend["Classification"],test_size=0.2,random_state=19)
X_train.info()
X_test.info()

import fasttext 
data_train = pandas.DataFrame(columns=["모집직종","Classification"])
data_train["Classifcation"] = "__label__"+Y_train
data_train["모집직종"] = X_train

data_train.to_csv('labellingtrain.txt', sep='\t',index= False)
labeling = pandas.read_csv("labellingtrain.txt",sep='\t')


output_lst = ["경영/사무","IT/인터넷","서비스","교육","의료","디자인","무역/유통","생산/제조","전문/특수직"]
classification_model = fasttext.train_supervised('labellingtrain.txt',wordNgrams=3, epoch=25,lr=0.35)

predictions = []
for d in X_test:
	predictions.append(classification_model.predict(d))

print(predictions)

from sklearn.metrics import accuracy_score 
final_predictions=[]
for data in predictions:
	final_predictions.append(data[0][0],replace("__label__",""))

