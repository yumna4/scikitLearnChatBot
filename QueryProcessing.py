import nltk
import pickle
from nltk.stem.porter import PorterStemmer
stemmer=PorterStemmer()

class QueryProcessor:

    def getFilterCondition(self,NLQuery,attributes,function,value):

        from pycorenlp import StanfordCoreNLP
        nlp = StanfordCoreNLP('http://localhost:9000')
        res = nlp.annotate(NLQuery,properties={'annotators': 'depparse','outputFormat': 'json', 'timeout': 1000,})

        for s in res['sentences']:
            ED= s['enhancedDependencies']

        attribute=''

        # for ed in ED:
        #     print "type: %s words:'%s', %s : %d , %d" % (ed['dep'], ed['governorGloss'], ed['dependentGloss'],ed['governor'],ed['dependent'])


        for ed in ED:
            if ed['governorGloss'] in attributes:
                # print "fghjk"
                # print ed['dep']
                if ("nmod" in ed['dep'] and ed['dependentGloss'].isdigit()) or ed['dep']=='amod':
                    attribute=ed['governorGloss']
                    # print attribute
                    # print "444"
                    break
            if ed['dependentGloss'] in attributes:
                if (ed['dep']=='nsubj' and ed['governorGloss'].isdigit()) :
                    attribute=ed['dependentGloss']
                    break
        print attribute
        if attribute=='':
            # print "its not there"
            for ed in ED:
                if ed['governorGloss'] in attributes:
                    if ed['dep']=='acl:relcl':
                        attribute=ed['governorGloss']
                        break

        if attribute=='':
            for word in NLQuery.split():

                if word in attributes:
                    attribute=word






        return filterCondition








