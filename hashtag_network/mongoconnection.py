from pymongo import MongoClient
import numpy as np
from scipy import linalg
import datetime
from pprint import *
from hashtag import * #the hashtags we want to retrive

hashtag_number=20
timeinterval_number=60
interval_day=1
start_time=datetime.datetime(2016, 5,1)
co_occurrence_matrix=np.zeros((hashtag_number,hashtag_number))

client=MongoClient('146.169.33.33',27020)#build a connection to MongoDB
database=client.get_database('Twitter_DATA')
database.authenticate('twitterApplication','gdotwitter')
collection=database.Twitter_Brexit_GNIP

for timeinterval in range(timeinterval_number):#get co_occurrence matrix for every timeinterval
    start_time=start_time+datetime.timedelta(days=interval_day)
    end=start_time+datetime.timedelta(days=interval_day)
    for i in range(hashtag_number-1):#count the co_occurrence frequency of every pair of hashtags by MongoDB
        for j in range(i,hashtag_number):
            co_occurrence_matrix[i][j]=collection.find({'ISO_created_at':{'$gte':start_time,'$lt':end},'hashtags':{'$all':[hashtag[i],hashtag[j]]}},{'ISO_created_at':1,'hashtags':1}).count()
            #print(co_occurrence_matrix[i][j])
    temp=co_occurrence_matrix.sum(axis=1)#count the frequency of every single hashtag
    for i in range(hashtag_number):
        co_occurrence_matrix[i][i]=temp[i]
    np.save('co_occurrence_'+str(timeinterval),co_occurrence_matrix)


for i in range(timeinterval_number):#build combine co_occurrence matrix
    filename='co_occurrence_'+str(i)+'.npy'
    if i==0:
        combine_matrix=np.load(filename)
    else:
        combine_matrix=linalg.block_diag(combine_matrix,np.load(filename))
np.save('combine_matrix',combine_matrix)
