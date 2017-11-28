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
        windowModel =svm.OneClassSVM(nu=0.01,kernel="linear")
        filterModel = svm.OneClassSVM(nu=0.01, kernel="linear")
        aggregateModel=svm.OneClassSVM(nu=0.01, kernel="linear")
        groupModel=svm.OneClassSVM(nu=0.01, kernel="linear")



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
        from FeatureExtractionWithTFIDF import TFIDFPreparer
        tfidfPreparer=TFIDFPreparer()
        for doc in documents:
            text = tfidfPreparer.prepareTextForTFIDF(doc)
            texts.append(text)

        self.countVectorizer,self.idf=tfidfInstance.getIDF(documents)



        self.tfidf_filter=tfidfInstance.getTFIDF(fdoc,self.countVectorizer,self.idf)
        self.tfidf_aggre=tfidfInstance.getTFIDF(adoc,self.countVectorizer,self.idf)
        self.tfidf_window=tfidfInstance.getTFIDF(wdoc,self.countVectorizer,self.idf)
        self.tfidf_group=tfidfInstance.getTFIDF(gdoc,self.countVectorizer,self.idf)


        x_filter=[]
        for i in range (len(fdoc)):
            total=tfidfPreparer.getSumOfCosineSimilarity(self.tfidf_filter[i],self.tfidf_filter)
            x_filter.append([total])
        x_aggre=[]
        for i in range (len(adoc)):
            total=tfidfPreparer.getSumOfCosineSimilarity(self.tfidf_aggre[i],self.tfidf_aggre)
            x_aggre.append([total])
        x_window=[]
        for i in range (len(wdoc)):
            total=tfidfPreparer.getSumOfCosineSimilarity(self.tfidf_window[i],self.tfidf_window)
            x_window.append([total])
        x_group=[]
        for i in range (len(gdoc)):
            total=tfidfPreparer.getSumOfCosineSimilarity(self.tfidf_group[i],self.tfidf_group)
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
        return self.countVectorizer,self.idf,self.tfidf_filter, self.tfidf_window, self.tfidf_aggre,self.tfidf_group


tfidfTrainer=TFIDFTrainer()
tfidfTrainer.createTrainingSet()