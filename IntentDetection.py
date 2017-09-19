import pickle
from Trainer import Trainer
from FilterFeatures import FilterModel
from AggregateFunctionFeatures import AggregateFunctionModel
from WindowFeatures import WindowModel
f
from query import QueryGenerator
from FeatureExtractionWithTFIDF import Trainer

tr=Trainer()
tr.createTrainingSet()
results=[]
filter=[]
aggre=[]
window=[]

class IntentDetector:

    def detectIntent(self, NLQuery):
        intents=[]
        windowModel=pickle.load(open('finalized_windowModel.sav', 'rb'))
        filterModel=pickle.load(open('finalized_filterModel.sav', 'rb'))
        aggregateModel=pickle.load(open('finalized_aggregateModel.sav', 'rb'))

        tr=Trainer()
        fm=FilterModel()
        afm=AggregateFunctionModel()
        wm=WindowModel()
        # tr.createTrainingSet()



        streamWords=["temperature","room","id","device","sensor","area","room number","humidity","office","temp","temperatures","temps","ids","rooms","numbers","degrees","server"]
        fdata=fm.getFilterFeatures(NLQuery)
        adata=afm.getAggregateFunctionFeatures(NLQuery)
        wdata=wm.getWindowFeatures(NLQuery)


        a=filterModel.predict([fdata])
        filter.append(a)
        if a==1:
            intents.append("filter")

        b=aggregateModel.predict([adata])
        aggre.append(b)
        if b==1:
            intents.append("aggregate")

        c=windowModel.predict([wdata])
        window.append(c)
        if c==1:
            intents.append("window")


        print intents
        return intents



q=QueryGenerator()
id=IntentDetector()


NLQuery="tallest tree"
intents=id.detectIntent(NLQuery)
# intents=id.detectIntent("greater than 7")
# intents=id.detectIntent("Show the temperatures equal to 60 degrees")
# intents=id.detectIntent("give me the average temperatures above 30 of room in past 10 minutes")
# intents=id.detectIntent("highest temperature")
# intents=id.detectIntent("tree")
# intents=id.detectIntent("average of temperature")
# intents=id.detectIntent("last 10 minutes, more than 7")
# intents=id.detectIntent("biggest tree")
# SiddhiQuery= q.generateQuery(NLQuery,intents,"Heights",["height"])
# print SiddhiQuery



#Here tfidf is shown only for the words in CV. tfidf is even calculated only based on the presence of those words. example "show the temp values greater than 40" is same as "show the temp
#values greater than 40 oh mary had a little lamp" eventhough ggreater shud have lesser importance in the second example as it is 1 word of many more words



#
# results=filter+aggre
# print results
#
#
# print accuracy_score([-1, -1,-1,-1,1,1,-1,-1],results)




