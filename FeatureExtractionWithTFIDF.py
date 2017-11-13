from nltk.stem.snowball import SnowballStemmer
stemmer=SnowballStemmer("english")
from sklearn.metrics.pairwise import cosine_similarity
import nltk

class TFIDFPreparer:
    def prepareTextForTFIDF(self,NLQuery,streamWords,Attributes):

        words=nltk.word_tokenize(NLQuery)
        tags =nltk.pos_tag(words)

        #REPLACING WITH CORRECT ATTRIBUTE NAMES, example replacing 'temp' in NLQuery with "Temperature. Note: Sensor will not be able to be replaced with device in this method"

        nouns=[]

        for tag in tags:
            if tag[1]=="NN" or tag[1]=="NNS":
                nouns.append(tag[0])
        for word in nouns:
            for attribute in Attributes:
                distance=nltk.edit_distance(word,attribute.lower())
                if distance<4:#OR LESS THAN 3
                    NLQuery=NLQuery.replace(word,attribute,1)


        from pycorenlp import StanfordCoreNLP
        nlp = StanfordCoreNLP('http://localhost:9000')

        res = nlp.annotate(str(NLQuery),properties={'annotators': 'depparse','outputFormat': 'json', 'timeout': 1000,})

        for s in res['sentences']:
            ED= s['enhancedDependencies']

        NLQuery=NLQuery.lower().split()
        stoplist = set('a of the and to in me is are'.split())
        NLQuery=[word for word in NLQuery if word not in stoplist]
        neededWords={'JJ':[1],'JJS':[1],'NN':[1]}

        for tag in tags:
            if tag[1] =='JJ':
                neededWords['JJ'].append(tag[0])
            if tag[1] =='JJS':
                neededWords['JJS'].append(tag[0])
        removed=False

        for ed in ED:
            if ed['dep'] =='compound' and ed['dependentGloss'] in neededWords['JJ'] and ed['governorGloss'] in Attributes:
                removed=True
                NLQuery.remove(ed['dependentGloss'])
            if ed['dep'] =='amod' and (ed['dependentGloss'] in neededWords['JJ'] or ed['dependentGloss'] in neededWords['JJS']) and ed['governorGloss'] in Attributes:
                removed=True
                NLQuery.remove(ed['dependentGloss'])
            if 'nmod' in ed['dep'] and (ed['dependentGloss'] in neededWords['JJS']) and ed['governorGloss'] in Attributes:
                removed=True
                NLQuery.remove(ed['dependentGloss'])

        if removed:
            NLQuery.append('AggregateWord')
        removed =False
        time=['min','mins','minutes','sec','second','minute','months','seconds','month','years','year','hour','hours','hr','day','days']
        NLQuery1=[word for word in NLQuery if word not in time]

        if NLQuery!=NLQuery1:
            NLQuery1.append('timeValue')
        NLQuery=NLQuery1
        text=filter(lambda a: a.isdigit()==False , NLQuery)
        for word in streamWords:
            text=filter(lambda a: a != word, text)

        return text
    # the similarity between the tfidf of a given query and the tfidf of each of the other queries in a class of intents is calculated, and the sum is returned

    def getSumOfCosineSimilarity(self,tfidf_value, tfidf_matrix):
        a= cosine_similarity(tfidf_value,tfidf_matrix)
        for i in list(a):
            a=i
        b= list(a)
        total=0
        for i in b:
            total=total+i
        return total