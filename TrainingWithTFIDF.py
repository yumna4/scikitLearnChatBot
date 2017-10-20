import json
from tfidf import TFIDF
import pickle
from sklearn import svm
from FeatureExtractionWithTFIDF import TFIDFPreparer
tfidfPreparer=TFIDFPreparer()

class TFIDFTrainer:
    cv=[]
    IDF=[]
    tfidf_filter=[]
    tfidf_window=[]
    tfidf_aggre=[]
    tfidf_group=[]

    def createTrainingSet(self):


        windowModel =svm.OneClassSVM(nu=0.01, kernel="linear", gamma="auto",tol=1)
        filterModel = svm.OneClassSVM(nu=0.01, kernel="linear", gamma="auto",tol=1)
        aggregateModel=svm.OneClassSVM(nu=0.01, kernel="linear", gamma="auto",tol=1)
        groupModel=svm.OneClassSVM(nu=0.01, kernel="linear", gamma="auto",tol=1)



        tfidfInstance=TFIDF()
        documents=[]


        fdoc=[]
        adoc=[]
        wdoc=[]
        gdoc=[]


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





        attributes=['Temperature','RoomNo','DeviceID']

        texts=[]
        streamWords=["temperature","server","room","id","device","sensor","room number","humidity","temp","temperatures","degree","temps","ids","rooms","numbers","degrees","server","office","area"]

        for doc in documents:
            # NLQuery=doc


            # # REPLACING WITH CORRECT ATTRIBUTE NAMES, example replacing 'temp' in NLQuery with "Temperature. Note: Sensor will not be able to be replaced with device in this method"
            #
            # words=nltk.word_tokenize(NLQuery)
            # tags =nltk.pos_tag(words)
            #
            # nouns=[]
            # # print tags
            # for tag in tags:
            #     # print tag[0]
            #     if tag[1]=="NN" or tag[1]=="NNS":
            #
            #         nouns.append(tag[0])
            #     elif tag[1]=="JJ":
            #         NLQuery=NLQuery.replace(tag[0],"adjective")
            #     # #     # print NLQuery
            #     elif tag[1]=="JJR":
            #         NLQuery=NLQuery.replace(tag[0],"comparative")
            #         # print NLQuery
            #     # elif tag[1]=="JJS":
            #     #     NLQuery=NLQuery.replace(tag[0],"superlative")
            #     # #     print NLQuery
            #
            # # for word in nouns:
            # #     for attribute in attributes:
            # #         distance=nltk.edit_distance(word,attribute.lower())
            # #         if distance<4:#OR LESS THAN 3
            # #
            # #             NLQuery=NLQuery.replace(word,"attribute",1)



            text = tfidfPreparer.prepareTFIDF(doc,streamWords)
            texts.append(text)


        from collections import defaultdict
        frequency = defaultdict(int)

        for text in texts:

            for token in text:

                frequency[token] += 1
        texts = [[token for token in text if frequency[token] > 1] for text in texts]


        documents=texts
        documents=[' '.join(doc)for doc in documents]



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

        from FeatureExtractionWithTagging import TaggingPreparer

        taggingPreparer=TaggingPreparer()
        x_filter=[]

        for i in range (len(fdoc)):
            total=tfidfPreparer.getSumOfCosineSimilarity(tfidf_filter[i],tfidf_filter)
            bag=taggingPreparer.prepareTagging(fdoc[i])
            # x_filter.append([total]+bag)
            x_filter.append([total])



        x_aggre=[]
        for i in range (len(adoc)):
            total=tfidfPreparer.getSumOfCosineSimilarity(tfidf_aggre[i],tfidf_aggre)
            bag=taggingPreparer.prepareTagging(adoc[i])
            # x_aggre.append([total]+bag)
            x_aggre.append([total])



        x_window=[]
        for i in range (len(wdoc)):
            total=tfidfPreparer.getSumOfCosineSimilarity(tfidf_window[i],tfidf_window)
            bag=taggingPreparer.prepareTagging(wdoc[i])
            # x_window.append([total]+bag)
            x_window.append([total])

        x_group=[]
        for i in range (len(gdoc)):
            total=tfidfPreparer.getSumOfCosineSimilarity(tfidf_group[i],tfidf_group)
            bag=taggingPreparer.prepareTagging(gdoc[i])
            # x_group.append([total]+bag)
            x_group.append([total])





        # fx_train=[]
        # for NLQuery in fdoc:
        #     bag=taggingPreparer.prepareTagging(NLQuery)
        #     fx_train.append(bag)
        #
        # ax_train=[]
        # for NLQuery in adoc:
        #     bag=taggingPreparer.prepareTagging(NLQuery)
        #     ax_train.append(bag)
        #
        # wx_train=[]
        # for NLQuery in wdoc:
        #     bag=taggingPreparer.prepareTagging(NLQuery)
        #     wx_train.append(bag)
        #
        # gx_train=[]
        # for NLQuery in gdoc:
        #     bag=taggingPreparer.prepareTagging(NLQuery)
        #     gx_train.append(bag)





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


tfidfTrainer=TFIDFTrainer()
tfidfTrainer.createTrainingSet()