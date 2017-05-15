import json

with open('data/json/GNIP_hashtag_frequency.json',mode='r') as f:
    hashtag_frequency=json.load(f)
hashtag_toplist=[d['_id'] for d in hashtag_frequency]
