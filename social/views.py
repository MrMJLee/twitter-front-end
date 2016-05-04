from django.shortcuts import render_to_response
import json
from pymongo import MongoClient
from collections import OrderedDict
from datetime import date, timedelta
from django.template import loader
import math

today = str(date.today())

client = MongoClient('52.36.220.142',27017)
db = client['MyApp']

def home(request):
    results = db.myapp_micollection.find()
    for postdic in results:
        totaltweets = postdic['totaltweets']
        positivesentiment = postdic['positivesentiment']
        negativesentiment = postdic['negativesentiment']
        neutralsentiment = postdic['neutralsentiment']

        pospercent = math.ceil(positivesentiment *100/totaltweets)
        negpercent = math.ceil(negativesentiment *100/totaltweets)
        neupercent = math.ceil(neutralsentiment *100/totaltweets)

        hashtags = postdic['hashtags']
        hashtags = OrderedDict(sorted(hashtags.items(), key=lambda x:x[1],reverse=True))

        toptweetsdic = postdic['toptweets']
        sortednames = sorted(toptweetsdic, key=lambda x:toptweetsdic[x]['retweetcount'],reverse=True)
        sortedtoptweetsdic = OrderedDict()

        i=0
        for k in sortednames:
            if i>4:
                break
            i = i+1
            sortedtoptweetsdic[k] = toptweetsdic[k]

        toptweets = OrderedDict()
        for key in sortedtoptweetsdic:
            t = []
            t.append(sortedtoptweetsdic[key]['retweetscreenname'])
            t.append(sortedtoptweetsdic[key]['retweetname'])
            t.append(sortedtoptweetsdic[key]['retweettext'])
            t.append(sortedtoptweetsdic[key]['retweetcount'])
            t.append(sortedtoptweetsdic[key]['retweetsentiment'])
            #t.append(sortedtoptweetsdic[key]['retweetimage'])
            toptweets[key] = t
        hourlyaggregate = postdic['hourlyaggregate']
        total = {}
        positive = {}
        negative ={}
        neutral ={}
        hi = {}
        for key in hourlyaggregate:
            hi[int(key)] = hourlyaggregate[key]
        hourlyaggregate = OrderedDict(sorted(hi.items()))

        for entry in hourlyaggregate:
            total[entry] = hourlyaggregate[entry]['totaltweets']
            positive[entry] = hourlyaggregate[entry]['positivesentiment']
            negative[entry] = hourlyaggregate[entry]['negativesentiment']
            neutral[entry] =hourlyaggregate[entry]['neutralsentiment']
	template = loader.get_template('social/index.html')
	return render_to_response('social/index.html',{'totaltweets':totaltweets,'positivesentiment':positivesentiment,'negativesentiment':negativesentiment,'neutralsentiment':neutralsentiment,
											'pospercent':pospercent,'negpercent':negpercent, 'neupercent':neupercent,'hashtags':hashtags,'hourlyaggregate':hourlyaggregate,'total':total
												,'positive':positive,'negative':negative,'neutral':neutral,'toptweets':toptweets})

