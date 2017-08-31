import json
from AggregateFunction import AggregateFunctionChecker
from Group import GroupChecker
from Filter import FilterChecker
from Window import WindowChecker
import pickle
import joblib



afc=AggregateFunctionChecker()
gc=GroupChecker()
fc=FilterChecker()
wc=WindowChecker()

windowModel=pickle.load(open('finalized_windowModel.sav', 'rb'))
filterModel=pickle.load(open('finalized_filterModel.sav', 'rb'))
tfidf=joblib.load('Classifier.sav')



class IntentDetector:

    def detectIntent(self, NLQuery):

        aggregate=afc.check(NLQuery)
        group=gc.check(NLQuery)
        filter=fc.check(NLQuery)
        window=wc.check(NLQuery)
        having=False
        if group and filter:
            having=True
            filter=False

        result=[aggregate,group,filter,window,having]
        intents=["aggregate","group","filter","window","having"]
        for i in range (len(intents)):
            if result[i]==True:
                print intents[i],

        print ""
        print ""

        # windowModel.predict(NLQuery)
        # filterModel.predict(NLQuery)






with open('intents.json') as json_data:
    intentsData=json.load(json_data)


id=IntentDetector()
for intent in intentsData['intents']:

    for pattern in intent['pattern']:
        print pattern
        id.detectIntent(pattern)



