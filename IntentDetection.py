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
            NP:  {<IN><CD><CC><CD>}
            {<NN|NNS|NNP><WDT>?<VBZ|VBP>?<JJR><IN><CD|NNS>}
                {<NNS|NN><IN><CD>}
                {<DT>?<JJ><CD><NNS|NN>}
                {<DT><JJ|JJS><NN|NNS|NNP>}
                {<WDT><VBP|VBZ><IN><CD>}
                {<CD><NN|NNS|NNP><RB|VBP>}
                {<JJ|JJS><NN|NNS|NNP>(<IN><NN|NNS|NNP>)?}
                {<DT>?<NN>?<IN><DT>?<NN|NNS|NNP><IN>?<NN|NNS|NNP>?}"""
        parser = nltk.RegexpParser(chunkToExtract)
        result = parser.parse(sentence)

        chunks=[]
        for subtree in result.subtrees():
            if subtree.label() == 'NP':
                t = subtree
                t = ' '.join(word for word, pos in t.leaves())
                chunks.append(t)
        return chunks

    def getAttributes(self,chunk,attributes):
        list1=chunk.split()
        list2=attributes
        list3 = set(list1)&set(list2) # we don't need to list3 to actually be a list

        list4 = sorted(list3, key = lambda k : list1.index(k))
        return (list4[0])

    def getAggWord(self,chunk):
        chunk=chunk.split()
        try:
            return chunk[1]
        except:
            return chunk[0]
    def detectIntent(self, NLQuery,attributes):



        words=nltk.word_tokenize(NLQuery)
        tags =nltk.pos_tag(words)

        simple=NLQuery
        #REPLACING WITH CORRECT ATTRIBUTE NAMES, example replacing 'temp' in NLQuery with "Temperature. Note: Sensor will not be able to be replaced with device in this method"

        nouns=[]

        for tag in tags:
            if tag[1]=="NN" or tag[1]=="NNS":
                nouns.append(tag[0])
        for word in nouns:
            for attribute in attributes:
                distance=nltk.edit_distance(word,attribute.lower())
                if distance<4:#OR LESS THAN 3
                    NLQuery=NLQuery.replace(word,attribute,1)



        sentences=self.prepareForNLP(NLQuery)
        # print sentences
        for sentence in sentences:

            chunks=self.chunk(sentence)


        intents=[]
        windowModel=pickle.load(open('finalized_windowModel.sav', 'rb'))
        filterModel=pickle.load(open('finalized_filterModel.sav', 'rb'))
        aggregateModel=pickle.load(open('finalized_aggregateModel.sav', 'rb'))
        groupModel=pickle.load(open('finalized_groupModel.sav','rb'))
        f=a=w=g=-1
        fil=agg=win=grp=-1
        entities={}
        for chunk in chunks:
            NLQuery=chunk
            NLQuery=tfidfPreparer.prepareTextForTFIDF(NLQuery)
            NLQuery=[' '.join(NLQuery)]
            cv,idf,tfidf_filter, tfidf_window,tfidf_aggre, tfidf_group=tfidfTrainer.getIDF()
            tfidf=tfidfInstance.getTFIDF(NLQuery,cv,idf)

            fdata=tfidfPreparer.getSumOfCosineSimilarity(tfidf,tfidf_filter)
            wdata=tfidfPreparer.getSumOfCosineSimilarity(tfidf,tfidf_window)
            adata=tfidfPreparer.getSumOfCosineSimilarity(tfidf,tfidf_aggre)
            gdata=tfidfPreparer.getSumOfCosineSimilarity(tfidf,tfidf_group)
            # print ([fdata,adata,wdata,gdata])


            # fil,agg,win,grp=filterModel.predict(fdata),aggregateModel.predict(adata),windowModel.predict(wdata),groupModel.predict(gdata)
            # print chunk
            fil =filterModel.decision_function(fdata)
            agg=aggregateModel.decision_function(adata)
            win=windowModel.decision_function(wdata)
            grp=groupModel.decision_function(gdata)
            vals=[fil,agg,win,grp]
            # print (vals)
            maxx=max(vals)

            if maxx==fil:
                intents.append('filter')
            elif maxx==agg:
                intents.append('aggregate')
                # print "agg"
                entities['aggregate']=self.getAttributes(chunk,attributes)
                # print entities['aggregate']
                chunk=chunk.replace(entities['aggregate'],"")
                entities['aggWord']=self.getAggWord(chunk)
            elif maxx==win:
                intents.append('window')
            elif maxx==grp and maxx>0.8:
                intents.append('group')
                entities['group']=self.getAttributes(chunk,attributes)





        if "aggregate" in intents:
            intents.append("window")
        intents=list(set(intents))
        if "filter" in intents:
            f=1
        if "aggregate" in intents:
            a=1
        if "window" in intents:
            w=1
        if "group" in intents and 'group' in entities.keys():
            g=1
        fil,agg,win,grp=f,a,w,g
        values=[fil,agg,win,grp]


        return values,intents,entities