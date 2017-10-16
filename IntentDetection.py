import pickle

# from TrainingWithTFIDF import TFIDFTrainer
# tfidfTrainer=TFIDFTrainer()
# from FeatureExtractionWithTFIDF import TFIDFPreparer
# from tfidf import TFIDF
# tfidfInstance=TFIDF()
# tfidfPreparer=TFIDFPreparer()

from FeatureExtractionWithTagging import TaggingPreparer
from TrainingWithTagging import TaggingTrainer
tag=TaggingTrainer()
taggingPreparer=TaggingPreparer()

class IntentDetector:

    def detectIntent(self, NLQuery,streamWords):
        intents=[]
        windowModel=pickle.load(open('finalized_windowModel.sav', 'rb'))
        filterModel=pickle.load(open('finalized_filterModel.sav', 'rb'))
        aggregateModel=pickle.load(open('finalized_aggregateModel.sav', 'rb'))
        groupModel=pickle.load(open('finalized_groupModel.sav','rb'))
        model=pickle.load(open('finalized_TagModel.sav','rb'))

        # NLQuery=tfidfPreparer.prepareTFIDF(NLQuery,streamWords)
        # NLQuery=[' '.join(NLQuery)]
        # cv,idf,tfidf_filter, tfidf_window,tfidf_aggre, tfidf_group=tfidfTrainer.getIDF()
        # tfidf=tfidfInstance.getTFIDF(NLQuery,cv,idf)
        # fdata=tfidfPreparer.getSumOfCosineSimilarity(tfidf,tfidf_filter)
        # wdata=tfidfPreparer.getSumOfCosineSimilarity(tfidf,tfidf_window)
        # adata=tfidfPreparer.getSumOfCosineSimilarity(tfidf,tfidf_aggre)
        # gdata=tfidfPreparer.getSumOfCosineSimilarity(tfidf,tfidf_group)

        data,queryChunks=taggingPreparer.prepareTagging(NLQuery)
        intent=["filter","window","aggre","group"]
        print NLQuery
        for chunk in queryChunks:

            x=taggingPreparer.getBag(chunk)
            # print x
            # print len(x)
            pred=model.predict([x])
            print intent[pred-1]

        # values=[fil,grp,win,grp]
        #
        # if fil==1: intents.append("filter")
        # if agg==1: intents.append("aggregate")
        # if win==1: intents.append("window")
        # if grp==1:intents.append("group")
        # # print intents
        values,intents=0,0
        return values,intents