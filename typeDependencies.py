from pycorenlp import StanfordCoreNLP
import json
nlp = StanfordCoreNLP('http://localhost:9000')


# cd stanford-corenlp-full-2017-06-09
# java -mx5g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 10000


# with open('intents.json') as json_data:
#      intentsData=json.load(json_data)
#
# for intent in intentsData['intents']:
#  for pattern  in intent['pattern']:
#
#      pattern = pattern.replace(u'\xa0', u' ')
#      pattern=str(pattern)



class TypeDependencies:
    def getStanfordProperties(self,pattern):
        dependencies = nlp.annotate(pattern,properties={'annotators': 'depparse','outputFormat': 'json', 'timeout': 1000,})
        posTags = nlp.annotate(pattern,properties={'annotators': 'pos','outputFormat': 'json', 'timeout': 1000,})


        for s in dependencies['sentences']:
            ED= s['enhancedDependencies']

        for i in posTags['sentences']:
            T= i['tokens']

        result=[]
        for ed in ED:
             for t in T:


                 if ed['dep']=="advmod" or ed['dep']=="amod":

                    a=ed['dependentGloss']

                    if t['word']==a and t['pos']=='JJR':
                        result.append("filter")

                 if ed['dep']=="amod":

                    a=ed['dependentGloss']

                    if t['word']==a and t['pos']=='JJ':
                        result.append("window")

        return result




