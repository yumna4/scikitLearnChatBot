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

        # NLQuery=tfidfPreparer.prepareTFIDF(NLQuery,streamWords)
        # NLQuery=[' '.join(NLQuery)]
        # cv,idf,tfidf_filter, tfidf_window,tfidf_aggre, tfidf_group=tfidfTrainer.getIDF()
        # tfidf=tfidfInstance.getTFIDF(NLQuery,cv,idf)
        # fdata=tfidfPreparer.getSumOfCosineSimilarity(tfidf,tfidf_filter)
        # wdata=tfidfPreparer.getSumOfCosineSimilarity(tfidf,tfidf_window)
        # adata=tfidfPreparer.getSumOfCosineSimilarity(tfidf,tfidf_aggre)
        # gdata=tfidfPreparer.getSumOfCosineSimilarity(tfidf,tfidf_group)

        fdata=gdata=wdata=adata=[taggingPreparer.prepareTagging(NLQuery)]
        fil,agg,win,grp=filterModel.predict(fdata),aggregateModel.predict(adata),windowModel.predict(wdata),groupModel.predict(gdata)
        values=[fil,grp,win,grp]

        if fil==1: intents.append("filter")
        if agg==1: intents.append("aggregate")
        if win==1: intents.append("window")
        if grp==1:intents.append("group")
        # print intents
        return values,intents