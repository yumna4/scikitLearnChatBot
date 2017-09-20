import pickle
from tfidf import TFIDF
from sklearn.metrics.pairwise import cosine_similarity

from sklearn.metrics import accuracy_score

from FilterFeatures import FilterModel
from AggregateFunctionFeatures import AggregateFunctionModel
from WindowFeatures import WindowModel
from GroupFeatures import GroupModel
from FeatureExtractionWithTFIDF import Trainer
# from Trainer import Trainer

tr=Trainer()
tfidfInstance=TFIDF()


class IntentDetector:
    fval=[]
    aval=[]
    wval=[]
    gval=[]

    def detectIntent(self, NLQuery):
        intents=[]
        windowModel=pickle.load(open('finalized_windowModel.sav', 'rb'))
        filterModel=pickle.load(open('finalized_filterModel.sav', 'rb'))
        aggregateModel=pickle.load(open('finalized_aggregateModel.sav', 'rb'))
        groupModel=pickle.load(open('finalized_groupModel.sav','rb'))
        tfidfInstance=TFIDF()






        stoplist = set('a of the and to in'.split())

        NLQuery = [word for word in NLQuery.lower().split() if word not in stoplist]

        streamWords=["temperature","room","id","device","sensor","room number","humidity","temp","temperatures","degree","temps","ids","rooms","numbers","degrees","server", "office","area"]

        for word in streamWords:

            NLQuery=filter(lambda a: a != word, NLQuery)

        NLQuery=[filter(lambda a: a.isdigit()==False , NLQuery)]

        cv,idf,tfidf_filter, tfidf_window,tfidf_aggre, tfidf_group=tr.getIDF()
        NLQuery=[' '.join(word) for word in NLQuery]
        print NLQuery
        tfidf=tfidfInstance.getTFIDF(NLQuery,cv,idf)

        c=0
        for i in [tfidf_filter, tfidf_window, tfidf_aggre, tfidf_group]:

            a=cosine_similarity(tfidf,i)
            for i in list(a):
                a=i
            b= list(a)
            total=0
            for i in b:
                total=total+i
            c+=1
            if c==1:
                fil=filterModel.predict(total)
            if c==2:
                win=windowModel.predict(total)
            if c==3:
                agg=aggregateModel.predict(total)
            if c==4:
                grp=groupModel.predict(total)




        # fm=FilterModel()
        # afm=AggregateFunctionModel()
        # wm=WindowModel()
        # gm=GroupModel()
        # fdata=fm.getFilterFeatures(NLQuery)
        # adata=afm.getAggregateFunctionFeatures(NLQuery)
        # wdata=wm.getWindowFeatures(NLQuery)
        # gdata=gm.getGroupFeatures(NLQuery)
        #
        #
        # fil=filterModel.predict([fdata])
        # agg=aggregateModel.predict([adata])
        # win=windowModel.predict([wdata])
        # grp=groupModel.predict([gdata])




        self.fval.append(fil)
        if fil==1:
            intents.append("filter")


        self.aval.append(agg)
        if agg==1:
            intents.append("aggregate")


        self.wval.append(win)
        if win==1:
            intents.append("window")

        self.gval.append(grp)
        if grp ==1:
            intents.append("group")

        return intents



id=IntentDetector()
print id.detectIntent("Per office area calculate the average temperature over last 10 minutes")
print id.detectIntent("Give me the average temperatures above 30 of room in past 10 minutes")
print id.detectIntent("Show the sum of temperature")
print id.detectIntent("Delay all events in a stream by 1 minute",)
print id.detectIntent("Show the average temperature per room and device ID for the last 10 minutes",)
print id.detectIntent( "Within a 10 minutes window, calculate the average Temperature per sensor and display the  event details if the average temperature is less than 45")
print id.detectIntent("Filtering all server rooms having temperature greater than 40 degrees")
print id.detectIntent("get the average temperature for each room with the 10 minutes window",)
print id.detectIntent( "for all the events in the past 10 minutes display the average temperature which are bigger than 30 of all the rooms along with there and device ID grouping all of this by the")
print id.detectIntent("For every group of device IDs in the temperature stream display the device ID and maximum temperature for every 10 events",)
print id.detectIntent("Show the temperatures below 100 degrees",)
print id.detectIntent( "most recent 10 minutes",)

results=id.fval+id.aval+id.wval+id.gval
print accuracy_score([-1,1, -1 ,-1 ,-1,1,1,-1,1,-1,1,-1     ,1,1, 1 ,-1 ,1 ,1 ,-1 ,1,1,1,-1 ,-1      ,1,1,-1,1,1,1,-1,1,1 ,-1 ,-1 ,1,     1,-1,-1,-1,1,1,-1,1 ,1,1,-1,-1                     ],results)




