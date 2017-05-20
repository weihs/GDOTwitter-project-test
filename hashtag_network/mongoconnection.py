from pymongo import MongoClient
import numpy as np
from scipy import linalg
import datetime
from pprint import *
from hashtag_toplist import * #the hashtags we want to retrive

hashtag=hashtag_toplist
hashtag_number=20
timeinterval_number=50
interval_day=1
start_time=datetime.datetime(2016, 5,1)
co_occurrence_matrix=np.zeros((hashtag_number,hashtag_number))

def merge_cooccurrence_matrix(number=50,
                              origin_directory='data/npy/',
                              result_directory='data/npy/',
                              origin_prefix='co_occurrence_',
                              result_filename='combine_matrix.npy'):
    postfix='.npy'
    for i in range(number):#build combine co_occurrence matrix
        filename=origin_directory+origin_prefix+str(i)+postfix
        if i==0:
            combine_matrix=np.load(filename)
        else:
            combine_matrix=linalg.block_diag(combine_matrix,np.load(filename))
    result_file=result_directory+result_filename
    np.save(result_file,combine_matrix)

client=MongoClient('146.169.33.33',27020)#build a connection to MongoDB
database=client.get_database('Twitter_DATA')
database.authenticate('twitterApplication','gdotwitter')
collection=database.Twitter_Brexit_GNIP

for timeinterval in range(1,timeinterval_number):#get co_occurrence matrix for every timeinterval
    start_time=start_time+datetime.timedelta(days=interval_day)
    end=start_time+datetime.timedelta(days=interval_day)
    for i in range(hashtag_number-1):#count the co_occurrence frequency of every pair of hashtags by MongoDB
        for j in range(i,hashtag_number):
            co_occurrence_matrix[i][j]=collection.find({'ISO_created_at':{'$gte':start_time,'$lt':end},'hashtags':{'$all':[hashtag[i],hashtag[j]]}},{'ISO_created_at':1,'hashtags':1}).count()
            #print(co_occurrence_matrix[i][j])
    temp=co_occurrence_matrix.sum(axis=1)#count the frequency of every single hashtag
    for i in range(hashtag_number):
        co_occurrence_matrix[i][i]=temp[i]
    np.save('data/npy/co_occurrence_'+str(timeinterval),co_occurrence_matrix)

merge_cooccurrence_matrix(number=50, origin_directory='data/npy/', result_directory='data/npy/', origin_prefix='co_occurrence_', result_filename='combine_matrix.npy')
