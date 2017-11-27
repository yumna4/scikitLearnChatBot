import pickle

from TrainingWithTFIDF import TFIDFTrainer
tfidfTrainer=TFIDFTrainer()
from FeatureExtractionWithTFIDF import TFIDFPreparer
from tfidf import TFIDF
tfidfInstance=TFIDF()
import nltk
tfidfPreparer=TFIDFPreparer()


class IntentDetector:

    def prepareForNLP(self,text):
        sentences = nltk.sent_tokenize(text)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]
        sentences = [nltk.pos_tag(sent) for sent in sentences]
        return sentences

    def chunk(self,sentence):
        #GREATER THAN 4, THE LAST 4 EVENTS, THE AVERAGE TEMPERATURE, PER SENSOR
        #5:THAT ARE /is above/below 59
        #6:netween 5 and 4
        #7:WITIN A 10 MINUTES WINDOW
        chunkToExtract = """
            NP: {<NN|NNS|NNP><WDT>?<VBZ|VBP>?<JJR><IN><CD|NNS>}
                {<NNS|NN><IN><CD>}
                {<DT>?<JJ><CD><NNS|NN>}
                {<DT><JJ|JJS><NN|NNS>}
                {<WDT><VBP|VBZ><IN><CD>}
                {<IN><CD><CC><CD>}
                {<CD><NN|NNS><RB|VBP>}
                {<JJ|JJS><NN|NNS>(<IN><NN|NNS>)?}
                {<DT>?<NN>?<IN><DT>?<NN|NNS>}"""
        parser = nltk.RegexpParser(chunkToExtract)
        result = parser.parse(sentence)

        chunks=[]
        for subtree in result.subtrees():
            if subtree.label() == 'NP':
                t = subtree
                t = ' '.join(word for word, pos in t.leaves())
                chunks.append(t)
        return chunks


    def detectIntent(self, NLQuery,streamWords,Attributes):

        sentences=self.prepareForNLP(NLQuery)
        print sentences
        for sentence in sentences:

            chunks=self.chunk(sentence)


        intents=[]
        windowModel=pickle.load(open('finalized_windowModel.sav', 'rb'))
        filterModel=pickle.load(open('finalized_filterModel.sav', 'rb'))
        aggregateModel=pickle.load(open('finalized_aggregateModel.sav', 'rb'))
        groupModel=pickle.load(open('finalized_groupModel.sav','rb'))
        f=a=w=g=-1
        fil=agg=win=grp=-1
        for chunk in chunks:
            NLQuery=chunk
            NLQuery=tfidfPreparer.prepareTextForTFIDF(NLQuery,streamWords)
            NLQuery=[' '.join(NLQuery)]
            cv,idf,tfidf_filter, tfidf_window,tfidf_aggre, tfidf_group=tfidfTrainer.getIDF()
            tfidf=tfidfInstance.getTFIDF(NLQuery,cv,idf)

            fdata=tfidfPreparer.getSumOfCosineSimilarity(tfidf,tfidf_filter)
            wdata=tfidfPreparer.getSumOfCosineSimilarity(tfidf,tfidf_window)
            adata=tfidfPreparer.getSumOfCosineSimilarity(tfidf,tfidf_aggre)
            gdata=tfidfPreparer.getSumOfCosineSimilarity(tfidf,tfidf_group)
            print ([fdata,adata,wdata,gdata])


            # fil,agg,win,grp=filterModel.predict(fdata),aggregateModel.predict(adata),windowModel.predict(wdata),groupModel.predict(gdata)
            print chunk
            fil =filterModel.decision_function(fdata)
            agg=aggregateModel.decision_function(adata)
            win=windowModel.decision_function(wdata)
            grp=groupModel.decision_function(gdata)
            vals=[fil,agg,win,grp]
            print (vals)
            maxx=max(vals)

            if maxx==fil and maxx>0.2:
                intents.append('filter')
            elif maxx==agg:
                intents.append('aggregate')
            elif maxx==win:
                intents.append('window')
            elif maxx==grp and maxx>0.8:
                intents.append('group')


            # if fil>0.2:
            #     f=1
            # if agg>0:
            #     a=1
            # if win>0:
            #     w=1
            # if grp>0.8:
            #     g=1
            # fil,agg,win,grp=f,a,w,g
            #
            # if fil==1: intents.append("filter")
            # if agg==1:
            #     intents.append("aggregate")
            #     win=agg
            # if win==1:
            #     intents.append("window")
            # if grp==1:intents.append("group")
        if "aggregate" in intents:
            intents.append("window")
        intents=list(set(intents))
        if "filter" in intents:
            f=1
        if "aggregate" in intents:
            a=1
        if "window" in intents:
            w=1
        if "group" in intents:
            g=1
        fil,agg,win,grp=f,a,w,g
        values=[fil,agg,win,grp]


        return values,intents