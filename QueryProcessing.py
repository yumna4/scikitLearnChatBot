import nltk
import pickle
from FilterConditionBuilder import FilterFinder
from nltk.stem.porter import PorterStemmer
stemmer=PorterStemmer()

class QueryProcessor:


    def getWindowType(self,NLQuery):

        String=NLQuery
        NLQuery=NLQuery.split()
        value=''
        NLQuery=[stemmer.stem(word) for word in NLQuery]

        if 'minut' in NLQuery:
            index=NLQuery.index('minut')
            value=NLQuery[index-1]+' min'
            windowType="time"

        if 'second' in NLQuery:
            index=NLQuery.index('second')
            value=value+NLQuery[index-1]+' sec'
            windowType="time"

        if 'hour' in NLQuery:
            index=NLQuery.index('hour')
            value=value+NLQuery[index-1]+' hour'
            windowType="time"

        if value=='' :
            windowType="length"


            intent=nltk.word_tokenize(String)
            sentence =nltk.pos_tag(intent)

            grammar = r"""FUNCTION:{<JJ><CD>}"""
            cp = nltk.RegexpParser(grammar)
            result = cp.parse(sentence)
            tagsOfQuery=list(result)
            for node in range(len(tagsOfQuery)):
                try:
                    if result[node].label()=="FUNCTION":
                        value=result[node].leaves()[1][0]+value
                except:
                    continue




        return value,windowType





    def getFilterCondition(self,NLQuery,attributes):
        ff=FilterFinder()

        model=pickle.load(open('findfilter_model.sav', 'rb'))
        prepared=ff.prepare(NLQuery)
        function=model.predict([prepared])
        index=int(function)
        filterTypes=[">","<","="," between "]
        function=filterTypes[index-1]

        from pycorenlp import StanfordCoreNLP
        nlp = StanfordCoreNLP('http://localhost:9000')
        res = nlp.annotate(NLQuery,properties={'annotators': 'depparse','outputFormat': 'json', 'timeout': 1000,})

        for s in res['sentences']:
            ED= s['enhancedDependencies']

        attribute=''
        for ed in ED:

            if ed['dep']=='nsubj':

                if ed['dependentGloss'] in attributes:
                    attribute=ed['dependentGloss']

        if attribute=='':
            for word in NLQuery.split():

                if word in attributes:
                    attribute=word





        value=ff.getValues()

        if function != " between ":
            filterCondition=[attribute,function,str(value[0])]
        else:
            filterCondition=[attribute,function,str(value[0])," and ",str(value[1])]




        return filterCondition








    def getGroupAttribute(self,NLQuery,attributes):

        from pycorenlp import StanfordCoreNLP
        nlp = StanfordCoreNLP('http://localhost:9000')
        res = nlp.annotate(NLQuery,properties={'annotators': 'depparse','outputFormat': 'json', 'timeout': 1000,})

        for s in res['sentences']:
            ED= s['enhancedDependencies']

        for ed in ED:

            if ed['dep']=='case':

                if ed['governorGloss'] in attributes:
                    groupAttribute=ed['governorGloss']


        return groupAttribute
