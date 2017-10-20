import pickle

from TrainingWithTFIDF import TFIDFTrainer
tfidfTrainer=TFIDFTrainer()
from FeatureExtractionWithTFIDF import TFIDFPreparer
from tfidf import TFIDF
tfidfInstance=TFIDF()
tfidfPreparer=TFIDFPreparer()

import nltk

class IntentDetector:

    def detectIntent(self, NLQuery,streamWords,attributes):





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
        #     # elif tag[1]=="JJ":
        #     #     NLQuery=NLQuery.replace(tag[0],"adjective")
        #     # #     # print NLQuery
        #     elif tag[1]=="JJR":
        #         NLQuery=NLQuery.replace(tag[0],"comparative")
        #     # print NLQuery
        #     elif tag[1]=="JJS":
        #         NLQuery=NLQuery.replace(tag[0],"superlative")
        #     # #     print NLQuery
        #
        # # for word in nouns:
        # #     for attribute in attributes:
        # #         distance=nltk.edit_distance(word,attribute.lower())
        # #         if distance<4:#OR LESS THAN 3
        # #
        # #             NLQuery=NLQuery.replace(word,"attribute",1)
















        intents=[]
        windowModel=pickle.load(open('finalized_windowModel.sav', 'rb'))
        filterModel=pickle.load(open('finalized_filterModel.sav', 'rb'))
        aggregateModel=pickle.load(open('finalized_aggregateModel.sav', 'rb'))
        groupModel=pickle.load(open('finalized_groupModel.sav','rb'))

        NLQuery=tfidfPreparer.prepareTFIDF(NLQuery,streamWords)
        NLQuery=[' '.join(NLQuery)]
        cv,idf,tfidf_filter, tfidf_window,tfidf_aggre, tfidf_group=tfidfTrainer.getIDF()
        tfidf=tfidfInstance.getTFIDF(NLQuery,cv,idf)

        fdata=tfidfPreparer.getSumOfCosineSimilarity(tfidf,tfidf_filter)
        wdata=tfidfPreparer.getSumOfCosineSimilarity(tfidf,tfidf_window)
        adata=tfidfPreparer.getSumOfCosineSimilarity(tfidf,tfidf_aggre)
        gdata=tfidfPreparer.getSumOfCosineSimilarity(tfidf,tfidf_group)


        fil,agg,win,grp=filterModel.predict(fdata),aggregateModel.predict(adata),windowModel.predict(wdata),groupModel.predict(gdata)


        if fil==1: intents.append("filter")

        if agg==1:
            intents.append("aggregate")

            win=agg
            intents.append("window")
        if grp==1:intents.append("group")


        # if fil==1: intents.append("filter")
        #
        # if win==1:
        #     intents.append("window")
        #     if agg==1:
        #         intents.append("aggregate")
        # else:
        #     agg=win
        #
        #
        # if grp==1:intents.append("group")



        values=[fil,agg,win,grp]

        return values,intents