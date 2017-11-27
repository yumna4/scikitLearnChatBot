class TFIDFTrainer:



    countVectorizer=[]
    IDF=[]
    tfidf_filter=[]
    tfidf_window=[]
    tfidf_aggre=[]
    tfidf_group=[]



    def createTrainingSet(self):


        # initialize one class SVM models for each intent
        from sklearn import svm
        windowModel =svm.OneClassSVM(nu=0.01, kernel="linear", gamma="auto",tol=1)
        filterModel = svm.OneClassSVM(nu=0.01, kernel="linear", gamma="auto",tol=1)
        aggregateModel=svm.OneClassSVM(nu=0.01, kernel="linear", gamma="auto",tol=1)
        groupModel=svm.OneClassSVM(nu=0.01, kernel="linear", gamma="auto",tol=1)



        from tfidf import TFIDF
        tfidfInstance=TFIDF()



        documents=[]
        fdoc=[]
        adoc=[]
        wdoc=[]
        gdoc=[]



        import json
        with open('intents.json') as json_data:
            intentsData=json.load(json_data)
        for intent in intentsData['intents']:
            for pattern in intent['pattern']:
                documents.append(pattern)
                if intent['tag']=="filter":
                    fdoc.append(pattern)
                if intent['tag']=="window":
                    wdoc.append(pattern)
                if intent['tag']=="aggre":
                    adoc.append(pattern)
                if intent['tag']=="group":
                    gdoc.append(pattern)



        texts=[]
        # words relevant to the stream. These words do not help in intent detection and must be removed
        streamWords=["temperature","server","room","id","deviceid","device","sensor","roomNo","roomnos","room number","devices","humidity","temp","temperatures","degree","temps","ids","rooms","numbers","degrees","server","office","area"]
        from FeatureExtractionWithTFIDF import TFIDFPreparer
        tfidfPreparer=TFIDFPreparer()
        for doc in documents:
            text = tfidfPreparer.prepareTextForTFIDF(doc,streamWords)
            texts.append(text)



        # remove words than occur only once in the corpus. This increased accuracy drastically
        from collections import defaultdict
        frequency = defaultdict(int)
        for text in texts:
            for token in text:
                frequency[token] += 1
        texts = [[token for token in text if frequency[token] > 1] for text in texts]
        documents=texts
        documents=[' '.join(doc)for doc in documents]



        self.countVectorizer,self.IDF=tfidfInstance.getIDF(documents)
        countVectorizer=self.countVectorizer
        idf=self.IDF



        tfidf_filter=tfidfInstance.getTFIDF(fdoc,countVectorizer,idf)
        tfidf_aggre=tfidfInstance.getTFIDF(adoc,countVectorizer,idf)
        tfidf_window=tfidfInstance.getTFIDF(wdoc,countVectorizer,idf)
        tfidf_group=tfidfInstance.getTFIDF(gdoc,countVectorizer,idf)
        # print "tfidfaggre"
        # print tfidf_aggre
        # print "tfidfwindow"
        # print tfidf_window


        self.tfidf_filter=tfidf_filter
        self.tfidf_window=tfidf_window
        self.tfidf_aggre=tfidf_aggre
        self.tfidf_group=tfidf_group



        x_filter=[]
        for i in range (len(fdoc)):
            total=tfidfPreparer.getSumOfCosineSimilarity(tfidf_filter[i],tfidf_filter)
            x_filter.append([total])
        x_aggre=[]
        for i in range (len(adoc)):
            total=tfidfPreparer.getSumOfCosineSimilarity(tfidf_aggre[i],tfidf_aggre)
            x_aggre.append([total])
        x_window=[]
        for i in range (len(wdoc)):
            total=tfidfPreparer.getSumOfCosineSimilarity(tfidf_window[i],tfidf_window)
            x_window.append([total])
        x_group=[]
        for i in range (len(gdoc)):
            total=tfidfPreparer.getSumOfCosineSimilarity(tfidf_group[i],tfidf_group)
            x_group.append([total])



        filterModel.fit(x_filter)
        windowModel.fit(x_window)
        aggregateModel.fit(x_aggre)
        groupModel.fit(x_group)



        import pickle
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
        return self.countVectorizer,self.IDF,self.tfidf_filter, self.tfidf_window, self.tfidf_aggre,self.tfidf_group

#
tfidfTrainer=TFIDFTrainer()
tfidfTrainer.createTrainingSet()