from pymongo import MongoClient
import numpy as np
from scipy import linalg
import datetime
import json
from pprint import *
from hashtag import * #the hashtags we want to retrive

hashtag_number=21
timeinterval_number=10
interval_day=1
start_time=datetime.datetime(2016, 5, 26, 0)
end_time=start_time+datetime.timedelta(days=10)
co_occurrence_matrix=np.zeros((hashtag_number,hashtag_number))

client=MongoClient('146.169.33.33',27020)#build a connection to MongoDB
database=client.get_database('Twitter_DATA')
database.authenticate('twitterApplication','gdotwitter')
collection=database.GNIP_50000_sample_users_above150twts

taglist=[]
cursor=collection.aggregate(
    [
        {'$match':{'ISO_created_at':{'$gte':start_time,'$lt':end_time}}},
        {'$unwind':'$hashtags'},
        {'$group':{'_id':'$hashtags','frequency':{'$sum':1}}},
        {'$sort':{'frequency':-1}}
    ]
)


for record in cursor:
    taglist.append(record)
with open('hashtag_frequency.json', mode='w') as f:
    json.dump(taglist,f)
