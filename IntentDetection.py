import pickle
from PrepareNLQuery import NLQueryPreparer
from tfidf import TFIDF
from Training import Trainer
pn=NLQueryPreparer()
t=TFIDF()
tr=Trainer()

windowModel=pickle.load(open('finalized_windowModel.sav', 'rb'))
filterModel=pickle.load(open('finalized_filterModel.sav', 'rb'))




class IntentDetector:

    def detectIntent(self, NLQuery):

        streamWords=["temperature","room","ID","device","sensor","area","room number","humidity","office","temp","temperatures","temps","IDs","rooms","numbers","degrees","server"]


        NLQuery=pn.prepareNLQuery(NLQuery,streamWords)
        # print NLQuery
        document=tr.a

        cv,idf=t.getIDF(document)

        NLQuery=t.getTFIDF((NLQuery,),cv,idf)


        print windowModel.predict(NLQuery)

        print filterModel.predict(NLQuery)



id=IntentDetector()
id.detectIntent("Show the temperatures above than 60 degrees in the past 10 minutes")

#Here tfidf is shown only for the words in CV. tfidf is even calculated only based on the presence of those words. example "show the temp values greater than 40" is same as "show the temp
#values greater than 40 oh mary had a little lamp" eventhough ggreater shud have lesser importance in the second example as it is 1 word of many more words



