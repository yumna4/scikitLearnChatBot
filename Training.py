import json
from sklearn import svm
from tfidf import TFIDF
import pickle
from PrepareNLQuery import NLQueryPreparer
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.font_manager
from sklearn import svm
from sklearn.covariance import EllipticEnvelope



class Trainer:



    windowModel =svm.OneClassSVM(nu=0.1, kernel="rbf", gamma="auto",tol=15)
    filterModel = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma="auto",tol=15.00500)
    aggregateModel=svm.OneClassSVM(nu=0.1, kernel="rbf", gamma="auto",tol=15.00500)


    pn=NLQueryPreparer()
    tfidfInstance=TFIDF()

    documents=[]
    countList=[]
    a=[]

    def createTrainingSet(self):

        with open('intents.json') as json_data:
            intentsData=json.load(json_data)



        for intent in intentsData['intents']:
            count=0

            self.documents.append(intent['pattern'])

            for pattern in intent['pattern']:
                count+=1

            self.countList.append(count)

        h=[]

        for i in self.documents:
            for j in i:
                h.append("".join(j))
        self.documents=h




        streamWords=["temperature","room","id","device","sensor","area","room number","humidity","office","temp","temperatures","degree","temps","ids","rooms","numbers","degrees","server"]


        for query in self.documents:


            query=self.pn.prepareNLQuery(query,streamWords)
            self.a.append(query)


        self.documents=self.a
        # print "########################"
        # for i in self.documents:

        #     print i

        cv,idf=self.tfidfInstance.getIDF(self.documents)

        tfidf=self.tfidfInstance.getTFIDF(self.documents,cv,idf)

        self.trainModel("filterTrainingSet",tfidf)
        self.trainModel("windowTrainingSet",tfidf)
        self.trainModel("aggregateTrainingSet",tfidf)




    def trainModel(self,training,tfidf):

        if training=="filterTrainingSet":
            x_train=tfidf[0:self.countList[0]]
            for i in x_train:
                print i
                print ""
                print ""
            self.filterModel.fit(x_train)


        if training=="windowTrainingSet":
            x_train=tfidf[self.countList[0]:self.countList[0]+self.countList[1]]
            self.windowModel.fit(x_train)




        if training=="filterTrainingSet":
            x_train=tfidf[self.countList[1]:self.countList[1]+self.countList[2]]

            self.aggregateModel.fit(x_train)



        filename = 'finalized_windowModel.sav'
        pickle.dump(self.windowModel, open(filename, 'wb'))


        filename = 'finalized_filterModel.sav'
        pickle.dump(self.filterModel, open(filename, 'wb'))

        filename = 'finalized_aggregateModel.sav'
        pickle.dump(self.aggregateModel, open(filename, 'wb'))








tr=Trainer()
tr.createTrainingSet()
