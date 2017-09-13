import pickle
from PrepareNLQuery import NLQueryPreparer
from tfidf import TFIDF
from Training import Trainer
pn=NLQueryPreparer()
t=TFIDF()
tr=Trainer()
from sklearn.metrics import accuracy_score

windowModel=pickle.load(open('finalized_windowModel.sav', 'rb'))
filterModel=pickle.load(open('finalized_filterModel.sav', 'rb'))
aggregateModel=pickle.load(open('finalized_aggregateModel.sav', 'rb'))

tr.createTrainingSet()

results=[]
class IntentDetector:

    def detectIntent(self, NLQuery):

        streamWords=["temperature","room","id","device","sensor","area","room number","humidity","office","temp","temperatures","temps","ids","rooms","numbers","degrees","server"]


        NLQuery=pn.prepareNLQuery(NLQuery,streamWords)

        # print NLQuery

        document=tr.a

        cv,idf=t.getIDF(document)
        NLQuery=t.getTFIDF((NLQuery,),cv,idf)
        # print NLQuery
        a=filterModel.predict(NLQuery)
        print a
        results.extend(a)
        b=windowModel.predict(NLQuery)
        print b
        results.extend(b)
        c= aggregateModel.predict(NLQuery)
        print c
        results.extend(c)



id=IntentDetector()
print "one"
print "1 1 -1"
id.detectIntent("greater than past minute")
print "two"
print "1 -1 -1"
id.detectIntent("greater than ")
print"three"
print "1 -1 1"
id.detectIntent("average above")
print "four"
print "1 -1 1"
id.detectIntent("greater than average")
print results
print accuracy_score([1, 1, -1,1 ,-1, -1,1, -1, 1,1, -1, 1],results)

#Here tfidf is shown only for the words in CV. tfidf is even calculated only based on the presence of those words. example "show the temp values greater than 40" is same as "show the temp
#values greater than 40 oh mary had a little lamp" eventhough ggreater shud have lesser importance in the second example as it is 1 word of many more words



