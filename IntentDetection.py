import pickle
from sklearn.metrics import accuracy_score


# from TrainingWithTFIDF import TFIDFTrainer
# tfidfTrainer=TFIDFTrainer()
# from FeatureExtractionWithTFIDF import TFIDFPreparer
# from tfidf import TFIDF
# tfidfInstance=TFIDF()
# tfidfPreparer=TFIDFPreparer()
# from query import QueryGenerator
#
# Q=QueryGenerator()


from FeatureExtractionWithTagging import TaggingPreparer
from TrainingWithTagging import TaggingTrainer
tag=TaggingTrainer()
taggingPreparer=TaggingPreparer()



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




        # streamWords=["temperature","server","room","id","device","sensor","room number","humidity","temp","temperatures","degree","temps","ids","rooms","numbers","degrees","server","office","area"]
        # NLQuery=tfidfPreparer.prepareTFIDF(NLQuery,streamWords)
        # NLQuery=[' '.join(NLQuery)]
        # cv,idf,tfidf_filter, tfidf_window,tfidf_aggre, tfidf_group=tfidfTrainer.getIDF()
        # tfidf=tfidfInstance.getTFIDF(NLQuery,cv,idf)
        # fdata=tfidfPreparer.getSumOfCosineSimilarity(tfidf,tfidf_filter)
        # wdata=tfidfPreparer.getSumOfCosineSimilarity(tfidf,tfidf_window)
        # adata=tfidfPreparer.getSumOfCosineSimilarity(tfidf,tfidf_aggre)
        # gdata=tfidfPreparer.getSumOfCosineSimilarity(tfidf,tfidf_group)




        fdata=adata=wdata=gdata=[taggingPreparer.prepareTagging(NLQuery)]



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
        print intents
        return intents



id=IntentDetector()
# intents=id.detectIntent("show devices having temperature less than 10")
# Q.generateQuery("show devices having temperature less than 10",intents,"TempStream",['temperature'])
id.detectIntent("Per office area calculate the average temperature over last 10 minutes")
id.detectIntent("Give me the average temperatures above 30 of room in past 10 minutes")
id.detectIntent("Show the sum of temperature")
id.detectIntent("Delay all events in a stream by 1 minute",)
id.detectIntent("Show the average temperature per room and device ID for the last 10 minutes",)
id.detectIntent( "Within a 10 minutes window, calculate the average Temperature per sensor and display the  event details if the average temperature is less than 45")
id.detectIntent("Filtering all server rooms having temperature greater than 40 degrees")
id.detectIntent("get the average temperature for each room with the 10 minutes window",)
id.detectIntent( "for all the events in the past 10 minutes display the average temperature which are bigger than 30 of all the rooms along with there and device ID grouping all of this by the")
id.detectIntent("For every group of device IDs in the temperature stream display the device ID and maximum temperature for every 10 events",)
id.detectIntent("Show the temperatures below 100 degrees",)
id.detectIntent( "most recent 10 minutes",)

id.detectIntent("Show the temperatures higher than 6 degrees",)
id.detectIntent( "show the average sum of temperature values")
id.detectIntent("Per sensor, calculate the maximum temperature over last 10 temperature events each sensor has emitted")
id.detectIntent("for every sensor, calculate the lowest temperature each sensor has emitted in the past 10 minutes,")
id.detectIntent("let me know if the temperature values are lesser than 40 in server rooms")
id.detectIntent("Show the server rooms which have a temperature that is higher than 20 degrees from the temperature stream",)
id.detectIntent( "display all the expired events in the past 1 minute from the temperature stream",)
id.detectIntent("average temperature")
id.detectIntent( "let me know the temperature over temperature events each sensor has emitted in a group of sensors")
id.detectIntent("group the temperature stream by device ID and display all the temperatures of each device ID",)
id.detectIntent("for every 10 events in each temperature group for a device ID get the, device ID maximum temperature",)
id.detectIntent( "temperature in the last 4 events",)


results=id.fval+id.aval+id.wval+id.gval
print accuracy_score([-1,1, -1 ,-1 ,-1,1,1,-1,1,-1,1,-1,1,-1,-1,-1 ,1,1,-1,-1,-1,-1,-1,-1        ,1,1, 1 ,-1 ,1 ,1 ,-1 ,1,1,1,-1 ,-1,-1 ,1,1,1,-1,-1 ,-1,1,-1,-1,1,-1              ,1,1,-1,1,1,1,-1,1,1 ,-1 ,-1 ,1,-1,-1,1,1 ,-1,-1,1,-1,-1,-1,-1,1          ,1,-1,-1,-1,1,1,-1,1 ,1,1,-1,-1,-1,-1,1,1 ,1 ,-1,-1,-1,-1,1,1,-1                             ],results)
print "filter accuracy"
print accuracy_score([-1,1, -1 ,-1 ,-1,1,1,-1,1,-1,1,-1,1,-1,-1,-1 ,1,1,-1,-1,-1,-1,-1,-1],id.fval)
print "aggregate accuracy"
print accuracy_score([1,1, 1 ,-1 ,1 ,1 ,-1 ,1,1,1,-1 ,-1,-1 ,1,1,1,-1,-1 ,-1,1,-1,-1,1,-1 ],id.aval)
print "window accuracy"
print accuracy_score([1,1,-1,1,1,1,-1,1,1 ,-1 ,-1 ,1,-1,-1,1,1 ,-1,-1,1,-1,-1,-1,-1,1 ],id.wval)
print "group accuracy"
print accuracy_score([1,-1,-1,-1,1,1,-1,1 ,1,1,-1,-1,-1,-1,1,1 ,1 ,-1,-1,-1,-1,1,1,-1 ],id.gval)

