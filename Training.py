import json
from sklearn import svm
from tfidf import TFIDF
import pickle
from PrepareNLQuery import NLQueryPreparer


class Trainer:

    windowModel =svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
    filterModel = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)



    pn=NLQueryPreparer()
    tfidfInstance=TFIDF()


    windowTrainingSet=[] # the data set that will be used for training the bot
    filterTrainingSet=[]


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




        streamWords=["temperature","room","ID","device","sensor","area","room number","humidity","office","temp","temperatures","temps","IDs","rooms","numbers","degrees","server"]


        for query in self.documents:

            query=self.pn.prepareNLQuery(query,streamWords)
            self.a.append(query)


        self.documents=self.a



        cv,idf=self.tfidfInstance.getIDF(self.documents)

        tfidf=self.tfidfInstance.getTFIDF(self.documents,cv,idf)

        self.trainModel("filterTrainingSet",tfidf)
        self.trainModel("windowTrainingSet",tfidf)




    def trainModel(self,training,tfidf):




        if training=="windowTrainingSet":
            x_train=tfidf[self.countList[0]:self.countList[1]+self.countList[0]]
            self.windowModel.fit(x_train)


        if training=="filterTrainingSet":
            x_train=tfidf[0:self.countList[0]]
            self.filterModel.fit(x_train)



        filename = 'finalized_windowModel.sav'
        pickle.dump(self.windowModel, open(filename, 'wb'))


        filename = 'finalized_filterModel.sav'
        pickle.dump(self.filterModel, open(filename, 'wb'))


tr=Trainer()
tr.createTrainingSet()
