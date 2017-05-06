import numpy as np
from scipy import linalg
import datetime
import json
import copy
from pprint import *
from hashtag import * #the hashtags we want to retrive

hashtag_number=21
timeinterval_number=10
interval_day=1
start_time=datetime.datetime(2016, 5, 26)

array_filename='combine_matrix.npy'#load the matrix
matrix=np.load(array_filename)

frequency={}
d={}
d['caption']='hashtag line graph'#build the data for chart (chart part)
d['subcaption']='first try'
d['xAxisName']='date'
d['yAxisName']='frequency'
d['theme']='fint'
frequency['chart']=copy.deepcopy(d)

dist=[]
d={}
for i in range(timeinterval_number):#build the data for chart (category part)
    d['label']=str(start_time+datetime.timedelta(days=i))
    dist.append(copy.deepcopy(d))
temp={}
temp['category']=copy.deepcopy(dist)
frequency['categories']=copy.deepcopy(temp)

dist=[]
d={}
for i in range(hashtag_number):#build the data for chart (value part)
    d['seriesname']=hashtag[i]
    dist2=[]
    d2={}
    for j in range(timeinterval_number):
        d2['value']=matrix[j*hashtag_number+i][j*hashtag_number+i]
        dist2.append(copy.deepcopy(d2))
    d['data']=copy.deepcopy(dist2)
    dist.append(copy.deepcopy(d))
frequency['dataset']=copy.deepcopy(dist)


with open('data.json','w') as f:
    json.dump(frequency,f)
