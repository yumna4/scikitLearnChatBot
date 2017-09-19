import json
from tfidf import TFIDF
import pickle
from PrepareNLQuery import NLQueryPreparer
from sklearn import svm
from sklearn.metrics.pairwise import cosine_similarity



class Trainer:



    windowModel =svm.OneClassSVM(nu=0.1, kernel="linear", gamma="auto",tol=1)
    filterModel = svm.OneClassSVM(nu=0.1, kernel="linear", gamma="auto",tol=1.00500)
    aggregateModel=svm.OneClassSVM(nu=0.1, kernel="linear", gamma="auto",tol=1.00500)


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

        tfidf_matrix=self.tfidfInstance.getTFIDF(self.documents,cv,idf)
        print tfidf_matrix

        a= cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
        print a
        index=[]

        for i in a:
            val= list(enumerate(list(i)))
            print val
            for i in val:
                if i[1]>0.3:
                    index.append(i[0])

        for i in index:
            print i
            print self.documents[i]

        self.trainModel("filterTrainingSet",tfidf_matrix)
        self.trainModel("windowTrainingSet",tfidf_matrix)
        self.trainModel("aggregateTrainingSet",tfidf_matrix)




    def trainModel(self,training,tfidf):

        if training=="filterTrainingSet":
            x_train=tfidf[0:self.countList[0]]
            # for i in x_train:
            #     print i
            #     print ""
            #     print ""
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