import numpy as np
from scipy import linalg
import datetime
import json
import copy
from pprint import *
from hashtag_toplist import * #the hashtags we want to retrive


def transform_combine_matrix_for_linechart(timeinterval_number=50,
                                           start_time=datetime.datetime(2016, 5, 1),
                                           combine_matrix_file='data/npy/aggregated_combine_matrix.npy',
                                           aggregated_list_file='data/json/GNIP_aggregated_hashtag_frequency.json'):
    with open(combine_matrix_file,mode='r') as f:#load the matrix
        matrix=np.load(f)
    with open(aggregated_list_file, mode='r') as f:
        hashtag_frequency_list=json.load(f)
    hashtag=[d['_id'] for d in hashtag_frequency_list]
    hashtag_number=matrix.shape[0]/timeinterval_number
    interval_day=1

    frequency={}
    d={}
    d['caption']='hashtag line graph'#build the data for chart (chart part)
    d['subcaption']='first try'
    d['xAxisName']='date'
    d['yAxisName']='frequency'
    d['theme']='fint'
    d['showValues']='0'
    frequency['chart']=copy.deepcopy(d)

    dist=[]
    d={}
    for i in range(timeinterval_number):#build the data for chart (category part)
        d['label']=str(start_time+datetime.timedelta(days=i))
        dist.append(copy.deepcopy(d))
    temp=[{}]
    temp[0]['category']=copy.deepcopy(dist)
    frequency['categories']=copy.deepcopy(temp)

    dist=[]
    d={}
    for i in range(hashtag_number):#build the data for chart (value part)
        d['seriesname']=hashtag[i]
        dist2=[]
        d2={}
        for j in range(timeinterval_number):
            d2['value']=np.log2(matrix[j*hashtag_number+i][j*hashtag_number+i]+0.00001)
            dist2.append(copy.deepcopy(d2))
        d['data']=copy.deepcopy(dist2)
        dist.append(copy.deepcopy(d))
    frequency['dataset']=copy.deepcopy(dist)


    with open('data/json/GNIP_aggregated_top20_hashtag_50days.json','w') as f:
        json.dump(frequency,f)

def transform_combine_matrix_for_lineheatmap(timeinterval_number=50,
                                           start_time=datetime.datetime(2016, 5, 1),
                                           combine_matrix_file='data/npy/aggregated_combine_matrix.npy',
                                           aggregated_list_file='data/json/GNIP_aggregated_hashtag_frequency.json'):
    with open(combine_matrix_file,mode='r') as f:#load the matrix
        matrix=np.load(f)
    with open(aggregated_list_file, mode='r') as f:
        hashtag_frequency_list=json.load(f)
    hashtag=[d['_id'] for d in hashtag_frequency_list]
    hashtag_number=matrix.shape[0]/timeinterval_number
    interval_day=1

    frequency={}
    d={}
    d['caption']='hashtag line heatmap'#build the data for chart (chart part)
    d['subcaption']='first try'
    d['xAxisName']='date'
    d['yAxisName']='frequency'
    d['theme']='fint'
    d['showValues']='0'
    frequency['chart']=copy.deepcopy(d)

    d={}
    d['gradient']=1#build the data for chart (colorrange part)
    d['minvalue']=8
    d['code']='cc0000'
    d['startlabel']='infrequent'
    d['endlabel']='frequent'
    d['maxvalue']=20
    frequency['colorrange']=copy.deepcopy(d)

    dist=[]
    d={}
    temp={}
    for i in range(hashtag_number):#build the data for chart (row part)
        d['label']=hashtag[i]
        d['id']=hashtag[i]
        dist.append(copy.deepcopy(d))
    temp['row']=copy.deepcopy(dist)
    frequency['rows']=copy.deepcopy(temp)

    dist=[]
    d={}
    temp={}
    for i in range(timeinterval_number):#build the data for chart (column part)
        d['label']=str(start_time+datetime.timedelta(days=i))
        d['id']=str(start_time+datetime.timedelta(days=i))
        dist.append(copy.deepcopy(d))
    temp['column']=copy.deepcopy(dist)
    frequency['columns']=copy.deepcopy(temp)

    dist=[]
    d={}
    temp=[{}]
    for i in range(hashtag_number):#build the data for chart (data part)
        for j in range(timeinterval_number):
            d['rowid']=hashtag[i]
            d['columnid']=str(start_time+datetime.timedelta(days=j))
            d['value']=np.log2(matrix[j*hashtag_number+i][j*hashtag_number+i]+0.1)
            dist.append(copy.deepcopy(d))
    temp[0]['data']=copy.deepcopy(dist)
    frequency['dataset']=copy.deepcopy(temp)

    with open('data/json/GNIP_aggregated_top20_hashtag_heatmap_50days.json','w') as f:
        json.dump(frequency,f)
