import json
from tfidf import TFIDF
import pickle
from sklearn import svm
from sklearn.metrics.pairwise import cosine_similarity



class Trainer:



    windowModel =svm.OneClassSVM(nu=0.1, kernel="linear", gamma="auto",tol=1)
    filterModel = svm.OneClassSVM(nu=0.1, kernel="linear", gamma="auto",tol=1.00500)
    aggregateModel=svm.OneClassSVM(nu=0.1, kernel="linear", gamma="auto",tol=1.00500)


    tfidfInstance=TFIDF()

    documents=[]
    countList=[]
    a=[]

    def createTrainingSet(self):
        fdoc=[]
        wdoc=[]
        adoc=[]

        with open('intents1.json') as json_data:
            intentsData=json.load(json_data)

        for intent in intentsData['intents']:
            count=0

            for pattern in intent['pattern']:
                # if intent['tag']=="filter":
                #     fdoc.append(pattern)
                # if intent['tag']=="window":
                #     wdoc.append(pattern)
                # if intent['tag']=="aggre":
                #     adoc.append(pattern)
                self.documents.append(pattern)
                count+=1
            self.countList.append(count)




        stoplist = set('a of the and to in'.split())

        texts = [[word for word in doc.lower().split() if word not in stoplist] for doc in self.documents]
        a=[]
        streamWords=["temperature","room","id","device","sensor","room number","humidity","temp","temperatures","degree","temps","ids","rooms","numbers","degrees","server"]


        for text in texts:
            text=filter(lambda a: a.isdigit()==False , text)


            for word in streamWords:
                text=filter(lambda a: a != word, text)
            a.append(text)


        texts=a

        from collections import defaultdict
        frequency = defaultdict(int)
        for text in texts:
            for token in text:
                frequency[token] += 1
        texts = [[token for token in text if frequency[token] > 1] for text in texts]

        texts=[' '.join(word) for word in texts]

        # print self.documents

        self.documents=texts

        fdoc=self.documents[0:self.countList[0]]
        wdoc=self.documents[self.countList[0]:self.countList[0]+self.countList[1]]
        adoc=self.documents[self.countList[0]+self.countList[1]:self.countList[1]+self.countList[2]]
        adoc=self.documents[57:83]


        cv,idf=self.tfidfInstance.getIDF(self.documents)



        tfidf_filter=self.tfidfInstance.getTFIDF(fdoc,cv,idf)
        tfidf_aggre=self.tfidfInstance.getTFIDF(adoc,cv,idf)
        tfidf_window=self.tfidfInstance.getTFIDF(wdoc,cv,idf)


        x_filter=[]

        for i in range (self.countList[0]):
            a= cosine_similarity(tfidf_window[i],tfidf_filter)
            for i in list(a):
                a=i
            b= list(a)


            total=0
            for i in b:

                total=total+i

            x_filter.append(total)


        x_aggre=[]

        for i in range (self.countList[2]):
            a= cosine_similarity(tfidf_aggre[i],tfidf_aggre)
            for i in list(a):
                a=i
            b= list(a)


            total=0
            for i in b:

                total=total+i

            x_aggre.append(total)


        x_window=[]

        a= cosine_similarity(tfidf_window[5],tfidf_window)
        for i in list(a):
            a=i
        b= list(a)


        total=0
        for i in b:
            # change the window to aggre and print total and see
            total=total+i


        a= cosine_similarity(tfidf_aggre[5],tfidf_window)

        for i in list(a):
            a=i
        b= list(a)


        total=0
        for i in b:
            # change the window to aggre and print total and see
            total=total+i



        for i in range (self.countList[1]):
            a= cosine_similarity(tfidf_window[i],tfidf_window)

            for i in list(a):
                a=i
            b= list(a)


            total=0
            for i in b:
                # change the window to aggre and print total and see
                total=total+i

            x_window.append(total)



        self.trainModel("filterTrainingSet",x_filter)
        self.trainModel("windowTrainingSet",x_window)
        self.trainModel("aggregateTrainingSet",x_aggre)




    def trainModel(self,training,tfidf):

        if training=="filterTrainingSet":
            x_train=tfidf
            self.filterModel.fit(x_train)


        if training=="windowTrainingSet":
            x_train=tfidf
            self.windowModel.fit(x_train)




        if training=="filterTrainingSet":
            x_train=tfidf

            self.aggregateModel.fit(x_train)



        filename = 'finalized_windowModel.sav'
        pickle.dump(self.windowModel, open(filename, 'wb'))


        filename = 'finalized_filterModel.sav'
        pickle.dump(self.filterModel, open(filename, 'wb'))

        filename = 'finalized_aggregateModel.sav'
        pickle.dump(self.aggregateModel, open(filename, 'wb'))








tr=Trainer()
tr.createTrainingSet()