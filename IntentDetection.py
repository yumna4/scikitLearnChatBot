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


    def getFilterChunk(self,sentence):
        chunkToExtract = """
            pattern:
           
            {<NNP|NNS|NN><WDT>?<VBP|VBZ>?<JJR>?<IN><CD><CC>?<CD>?}
               """

        parser = nltk.RegexpParser(chunkToExtract)
        result = parser.parse(sentence)

        chunks=[]
        for subtree in result.subtrees():
            if subtree.label() == 'pattern':
                t = subtree
                t = ' '.join(word for word, pos in t.leaves())
                return t


    def chunk(self,sentence):

        chunkToExtract = """
            pattern:
            {<DT><JJ|JJS><NN|NNS|NNP>}
            {<DT>?<JJ><CD><NNS|NN>}
            {<NNP|NNS|NN>?<WDT>?<VBP|VBZ>?<JJR>?<IN><CD><CC>?<CD>?}
                {<CD><NN|NNS|NNP><RB|VBP>}
                {<JJ|JJS><NN|NNS|NNP>(<IN><NN|NNS|NNP>)?}
                {<DT>?<NN>?<IN><DT>?<NN|NNS|NNP><IN>?<NN|NNS|NNP>?}"""

        parser = nltk.RegexpParser(chunkToExtract)
        result = parser.parse(sentence)

        chunks=[]
        for subtree in result.subtrees():
            if subtree.label() == 'pattern':
                t = subtree
                t = ' '.join(word for word, pos in t.leaves())
                chunks.append(t)
        return chunks


    def getFilterWord(self,chunk):
        filters=['greater','larger','bigger','more','higher','above','smaller','less','lesser','below','lower','equal','same','between']
        for word in chunk.split():
            if word in filters:
                return word
    def getFilterAttribute(self,NLQuery,attributes):
        chunk=NLQuery

        sentences = nltk.sent_tokenize(chunk)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]
        sentences = [nltk.pos_tag(sent) for sent in sentences]

        for sentence in sentences:

            chunk=self.getFilterChunk(sentence)
        for word in chunk.split():
            if word in attributes:
                return word



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



    def getTimeUnit(self,chunk):
        words=chunk.split()
        units={"minutes":"min","seconds":"sec","hours":"hour","milliseconds":"millisec","days":"day","weeks":"week","months":"month","years":"year"}

        for word in words:
            for unit in units.keys():
                distance=nltk.edit_distance(word,unit)
                if distance<3:#OR LESS THAN 3
                    return units[unit]
        return "length"



    def detectIntent(self, NLQuery,attributes):
        words=nltk.word_tokenize(NLQuery)
        tags =nltk.pos_tag(words)


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


        query=NLQuery
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

            fil =filterModel.decision_function(fdata)
            agg=aggregateModel.decision_function(adata)
            win=windowModel.decision_function(wdata)
            grp=groupModel.decision_function(gdata)
            vals=[fil,agg,win,grp]
            maxx=max(vals)

            if maxx==fil:
                intents.append('filter')
                entities['filterWord']=self.getFilterWord(chunk)
                if entities['filterWord']!='between':
                    entities['filterValue']=[int(s) for s in chunk.split() if s.isdigit()][0]
                else:

                    entities['filterValue']=[int(s) for s in chunk.split() if s.isdigit()]

                entities['filterAttribute']=self.getFilterAttribute(query,attributes)

            elif maxx==agg:
                intents.append('aggregate')
                # print "agg"
                entities['aggregate']=self.getAttributes(chunk,attributes)
                # print entities['aggregate']
                chunk=chunk.replace(entities['aggregate'],"")
                entities['aggWord']=self.getAggWord(chunk)

            elif maxx==win:
                intents.append('window')
                entities['timeUnit']=self.getTimeUnit(chunk)
                entities['windowType']="time"
                if entities['timeUnit']=="length":
                    entities['windowType']="length"
                    entities['timeUnit']=""
                entities['windowValue']=[int(s) for s in chunk.split() if s.isdigit()][0]

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