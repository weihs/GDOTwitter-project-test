import numpy as np
from scipy import linalg
import datetime
import json
import copy
from pprint import *

want_top=20#the number of top hashtags you want to show in pie chart
top_hashtag_list=[]
chartlist={}
to_draw={}
with open('GNIP_hashtag_frequency.json',mode='r') as f:#load the raw data
    hashtag_list=json.load(f)

chartlist['caption']='hashtag proportion'#prepare the chart part
chartlist['showvalues']='1'
chartlist['showpercentvalues']='1'
chartlist['theme']='fint'
to_draw['chart']=chartlist

count=0
tempdic={}
other_sum=0
tophashtags=[]
for entry in hashtag_list:#parse the rawdata to FusionCharts required form(data part)
    if count==0:
        count+=1
        continue
    if count>want_top:
        other_sum+=entry['frequency']
        continue
    count+=1
    tophashtags.append(entry['_id'])
    tempdic['label']=entry['_id']
    tempdic['value']=entry['frequency']
    top_hashtag_list.append(copy.deepcopy(tempdic))
tempdic['label']='others'
tempdic['value']=other_sum
top_hashtag_list.append(copy.deepcopy(tempdic))
to_draw['data']=top_hashtag_list



np.save('tophashtags.npy',np.array(tophashtags))
with open('top20_hashtag_frequency.json',mode='w') as f:#save the data to draw pie charts
    json.dump(to_draw,f)
