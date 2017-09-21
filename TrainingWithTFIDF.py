import json
from tfidf import TFIDF
import pickle
from sklearn import svm
from FeatureExtractionWithTFIDF import Preparer

prep=Preparer()

class Trainer:
    cv=[]
    IDF=[]
    tfidf_filter=[]
    tfidf_window=[]
    tfidf_aggre=[]
    tfidf_group=[]

    def createTrainingSet(self):


        windowModel =svm.OneClassSVM(nu=0.1, kernel="linear", gamma="auto",tol=0.002)
        filterModel = svm.OneClassSVM(nu=0.1, kernel="linear", gamma="auto",tol=0.00200500)
        aggregateModel=svm.OneClassSVM(nu=0.1, kernel="linear", gamma="auto",tol=0.00200500)
        groupModel=svm.OneClassSVM(nu=0.1, kernel="linear", gamma="auto",tol=0.00200500)


        tfidfInstance=TFIDF()
        documents=[]
        countList=[]



        with open('intents1.json') as json_data:
            intentsData=json.load(json_data)

        for intent in intentsData['intents']:
            count=0

            for pattern in intent['pattern']:
                documents.append(pattern)
                count+=1
            countList.append(count)


        texts=[]
        for doc in documents:
            text = prep.prepare(doc)
            texts.append(text)


        from collections import defaultdict
        frequency = defaultdict(int)

        for text in texts:

            for token in text:

                frequency[token] += 1
        texts = [[token for token in text if frequency[token] > 1] for text in texts]


        documents=texts
        documents=[' '.join(doc)for doc in documents]

        fdoc=documents[0:countList[0]]
        wdoc=documents[countList[0]:countList[0]+countList[1]]
        adoc=documents[countList[0]+countList[1]:countList[0]+countList[1]+countList[2]]
        gdoc=documents[countList[0]+countList[1]+countList[2]:countList[0]+countList[1]+countList[2]+countList[3]]



        self.cv,self.IDF=tfidfInstance.getIDF(documents)
        cv=self.cv
        idf=self.IDF


        tfidf_filter=tfidfInstance.getTFIDF(fdoc,cv,idf)
        tfidf_aggre=tfidfInstance.getTFIDF(adoc,cv,idf)
        tfidf_window=tfidfInstance.getTFIDF(wdoc,cv,idf)
        tfidf_group=tfidfInstance.getTFIDF(gdoc,cv,idf)

        self.tfidf_filter=tfidf_filter
        self.tfidf_window=tfidf_window
        self.tfidf_aggre=tfidf_aggre
        self.tfidf_group=tfidf_group


        x_filter=[]

        for i in range (countList[0]):
            total=prep.getSumOfCosineSimilarity(tfidf_filter[i],tfidf_filter)
            x_filter.append([total])


        x_aggre=[]
        for i in range (countList[2]):
            total=prep.getSumOfCosineSimilarity(tfidf_aggre[i],tfidf_aggre)
            x_aggre.append([total])


        x_window=[]
        for i in range (countList[1]):
            total=prep.getSumOfCosineSimilarity(tfidf_window[i],tfidf_window)
            x_window.append([total])

        x_group=[]
        for i in range (countList[3]):
            total=prep.getSumOfCosineSimilarity(tfidf_group[i],tfidf_group)
            x_group.append([total])




        filterModel.fit(x_filter)
        windowModel.fit(x_window)
        aggregateModel.fit(x_aggre)
        groupModel.fit(x_group)



        filename = 'finalized_windowModel.sav'
        pickle.dump(windowModel, open(filename, 'wb'))
        filename = 'finalized_filterModel.sav'
        pickle.dump(filterModel, open(filename, 'wb'))
        filename = 'finalized_aggregateModel.sav'
        pickle.dump(aggregateModel, open(filename, 'wb'))
        filename = 'finalized_groupModel.sav'
        pickle.dump(groupModel, open(filename, 'wb'))



    def getIDF(self):
        self.createTrainingSet()
        return self.cv,self.IDF,self.tfidf_filter, self.tfidf_window, self.tfidf_aggre,self.tfidf_group



tr=Trainer()
tr.createTrainingSet()