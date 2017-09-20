import pickle
from tfidf import TFIDF
from sklearn.metrics.pairwise import cosine_similarity
from FeatureExtractionWithTFIDF import Trainer
from sklearn.metrics import accuracy_score


tr=Trainer()
tfidfInstance=TFIDF()


class IntentDetector:
    fval=[]
    aval=[]
    wval=[]

    def detectIntent(self, NLQuery):
        intents=[]
        windowModel=pickle.load(open('finalized_windowModel.sav', 'rb'))
        filterModel=pickle.load(open('finalized_filterModel.sav', 'rb'))
        aggregateModel=pickle.load(open('finalized_aggregateModel.sav', 'rb'))
        tfidfInstance=TFIDF()






        stoplist = set('a of the and to in'.split())

        NLQuery = [word for word in NLQuery.lower().split() if word not in stoplist]

        streamWords=["temperature","room","id","device","sensor","room number","humidity","temp","temperatures","degree","temps","ids","rooms","numbers","degrees","server"]

        for word in streamWords:

            NLQuery=filter(lambda a: a != word, NLQuery)

        NLQuery=[filter(lambda a: a.isdigit()==False , NLQuery)]

        cv,idf,tfidf_filter, tfidf_window,tfidf_aggre=tr.getIDF()
        NLQuery=[' '.join(word) for word in NLQuery]
        tfidf=tfidfInstance.getTFIDF(NLQuery,cv,idf)

        a= cosine_similarity(tfidf,tfidf_filter)
        for i in list(a):
            a=i
        b= list(a)
        total=0
        for i in b:
            total=total+i

        fil=filterModel.predict([total])



        a= cosine_similarity(tfidf,tfidf_window)
        for i in list(a):
            a=i
        b= list(a)
        total=0
        for i in b:
            total=total+i


        win=windowModel.predict([total])


        a= cosine_similarity(tfidf,tfidf_aggre)
        for i in list(a):
            a=i
        b= list(a)
        total=0
        for i in b:
            total=total+i

        agg=aggregateModel.predict([total])


        if fil==1:
            intents.append("filter")
            self.fval.append(fil)
        else:
            self.fval.append(-1)


        if agg==1:
            intents.append("aggregate")
            self.aval.append(agg)
        else:
            self.aval.append(-1)



        if win==1:
            intents.append("window")
            self.wval.append(win)
        else:
            self.wval .append(-1)



        return intents



id=IntentDetector()
#
#
# NLQuery="larger than"
# print id.detectIntent(NLQuery)

print id.detectIntent("Per office area calculate the average temperature over last 10 minutes")
print id.detectIntent("Give me the average temperatures above 30 of room in past 10 minutes")
print id.detectIntent("Show the sum of temperature")
print id.detectIntent("Delay all events in a stream by 1 minute",)
print id.detectIntent("Show the average temperature per room and device ID for the last 10 minutes",)
print id.detectIntent( "Within a 10 minute window, calculate the average Temp per sensor and display the  event details if the average temperature is less than 45")
print id.detectIntent("Filtering all server rooms having temperature greater than 40 degrees")
print id.detectIntent("get the average temperature for each with the 10 minutes window",)
print id.detectIntent( "for all the events in the past 10 minutes display the average temperature which are bigger than 30 of all the rooms along with there and device ID grouping all of this by the")
print id.detectIntent("For every group of device IDs in the temperature stream display the device ID and maximum temperature for every 10 events",)
print id.detectIntent("Show the temperatures below 100 degrees",)
print id.detectIntent( "most recent 10 minutes",)

results=id.fval+id.aval+id.wval
print accuracy_score([-1,1, -1 ,-1 ,-1,1,1,-1,1 ,-1 ,1,-1                   ,1,1, 1 ,-1 ,1 ,1 ,-1 ,1,1,1,-1 ,-1                            ,1,1, -1  ,1,1,1,-1,1,1 ,1 ,-1 ,1                            ],results)




