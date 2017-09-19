import nltk
import re
class AggregateFunctionModel:
    documents=[]
    def getAggregateFunctionFeatures(self,NLQuery):

        # print NLQuery
        grammar = r"""FUNCTION:{<NN><IN>|<JJS>|<JJ>}"""
        cp = nltk.RegexpParser(grammar)
        intent=nltk.word_tokenize(NLQuery)
        sentence =nltk.pos_tag(intent)


        result = cp.parse(sentence)
        tagsOfQuery=list(result)
        aggre1=[]
        for node in range(len(tagsOfQuery)):
            try:
                if result[node].label()=="FUNCTION":
                    aggre1.extend(result[node])
            except:
                continue

        if re.findall('maximum|greatest|largest|biggest|minimum|smallest|highest|lowest|count|number|add|average|normal|sum|total|peak',NLQuery):
            aggre2=1
        else:
            aggre2=0

        if aggre1:
            # print "YES"
            aggre1=1
        else:
            # print "NO"
            aggre1=0
        # print [aggre1,aggre2]
        return [aggre1, aggre2]


