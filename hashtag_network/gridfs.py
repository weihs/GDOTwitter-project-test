from pymongo import MongoClient
import gridfs
import pprint as pp
db=MongoClient().test
collection=db.Twitter_Brexit_GNIP
resultset=collection.aggregate(
[
    {'$unwind':'$hashtags'},
    {
        '$group':{
            '_id':'$hashtags',
            'count':{'$sum':1}
        }
    },
    {'$sort':{'count':-1}}

])
for record in resultset:
    print(record['_id'])
    break






data_json=json.dumps(frequency)
pprint(data_json)
