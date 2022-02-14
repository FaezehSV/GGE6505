######################################################################################################################
#download data from kaggle
import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi
api = KaggleApi()
api.authenticate()

     
import pandas as pd
     
api.dataset_download_files('imdevskp/corona-virus-report','C:/Users/15062/OneDrive/Desktop/Kaggle',unzip=True)

coviddata="country_wise_latest.csv"
data=pd.read_json(coviddata)

######################################################################################################################
#prepare coloumn name of data
modfied_columns={}
for column_I in data.columns:
    new_column=column_I
    for operations in " `~!@#$%^&*)(-+=,.?/\|":
        new_column=new_column.replace(operations, "_")
    modfied_columns[column_I]=new_column
data.rename(columns = modfied_columns,inplace = True)
data.head()

modfied_columns2={}
for column_I in data.columns:
    first_char=column_I[0]
    if first_char in "0123456789":
        first_char= "_" + first_char
        new_column=first_char + column_I[1:]     
        modfied_columns2[column_I]=new_column
data.rename(columns = modfied_columns2,inplace = True)
data.head()

######################################################################################################################
#Change CSV to Json and import data to MongoDB


import pandas as pd
import os
from pymongo import MongoClient

path="C:/Users/15062/OneDrive/Desktop/Kaggle/" #Filepath
os.chdir(path)


client = MongoClient("mongodb://localhost:27017/")
db=client["dbname1"]
db_c=db["collectionname1"] 
x=db_c.count_documents({}) #Since its new one the count will be empty

def csv_to_json(filename, header=None):
    data = pd.read_csv(filename, header=header)
    return data.to_dict('records')

#print(csv_to_json('country_wise_latest.csv'))

db_c.insert_many(csv_to_json('country_wise_latest.csv', header=0))

######################################################################################################################
#Query

q1 = { "WHO_Region": "Europe" }

list = db_c.find(q1)

#for x in list:
#    print(x)
    
#q2
q2 = { "Confirmed" : 907 , "WHO_Region": "Europe" }

list2 = db_c.find(q2)

for x in list2:
    print(x)    
    
#q3

q3 = { "Active" : { "$gte" : 25000}, "New_cases" : {"$lte": 10}, "WHO_Region": "Europe"}
list3 = db_c.find(q3)

for i in list3:
    print(i)    