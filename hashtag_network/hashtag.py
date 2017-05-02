# db.getCollection('GNIP_50000_sample_users_above150twts').find({'ISO_created_at':{'$gte':new Date('2016-05-26T12:00:00.000Z')},'hashtags':{'$all':['brexit','voteleave']}},{'hashtags':1,'postedTime':1,'ISO_created_at':1}).limit(50)
hashtag='brexit, yes2eu, yestoeu, betteron, votein, ukineu, bremain, strongerin, leadnotleave, voteremain, no2eu, notoeu, betteroout, voteout, eureform, britainout, leaveeu, voteleave, beleave, loveeuropeleaveeu, leaveeu'
hashtag=hashtag.split(', ')
