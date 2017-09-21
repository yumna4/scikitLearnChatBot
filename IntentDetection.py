import pickle
from tfidf import TFIDF
from sklearn.metrics.pairwise import cosine_similarity
from FeatureExtractionWithTagging import NLQueryPreparer
from FeatureExtractionWithTFIDF import Preparer
from sklearn.metrics import accuracy_score
from TrainingWithTFIDF import Trainer
# from TrainingWithTagging import Trainer

tr=Trainer()
tfidfInstance=TFIDF()
prep=NLQueryPreparer()
prep1=Preparer()

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



        NLQuery=prep1.prepare(NLQuery)


        NLQuery=[' '.join(NLQuery)]

        cv,idf,tfidf_filter, tfidf_window,tfidf_aggre, tfidf_group=tr.getIDF()
        tfidf=tfidfInstance.getTFIDF(NLQuery,cv,idf)






        fdata=prep1.getSumOfCosineSimilarity(tfidf,tfidf_filter)
        wdata=prep1.getSumOfCosineSimilarity(tfidf,tfidf_window)
        adata=prep1.getSumOfCosineSimilarity(tfidf,tfidf_aggre)
        gdata=prep1.getSumOfCosineSimilarity(tfidf,tfidf_group)

        #
        # fdata=adata=wdata=gdata=prep.prepareNLQuery(NLQuery)


        fil=filterModel.predict(fdata)
        agg=aggregateModel.predict(adata)
        win=windowModel.predict(wdata)
        grp=groupModel.predict(gdata)





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




