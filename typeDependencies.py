from pycorenlp import StanfordCoreNLP
import json
import nltk
nlp = StanfordCoreNLP('http://localhost:9000')


# cd stanford-corenlp-full-2017-06-09
# java -mx5g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 10000


with open('intents.json') as json_data:
     intentsData=json.load(json_data)





for intent in intentsData['intents']:
    for pattern  in intent['pattern']:
        print ""
        print ""
        print "New Query"
        print intent['tag']
        pattern = pattern.replace(u'\xa0', u' ')
        pattern=str(pattern)

        dependencies = nlp.annotate(pattern,properties={'annotators': 'depparse','outputFormat': 'json', 'timeout': 1000,})
        posTags = nlp.annotate(pattern,properties={'annotators': 'pos','outputFormat': 'json', 'timeout': 1000,})


        print posTags
        for ps in posTags:
            print ps['pos']
        for s in dependencies['sentences']:
            ED= s['enhancedDependencies']
        for ed in ED:
            print "type: %s words:'%s', %s : %d , %d" % (ed['dep'], ed['governorGloss'], ed['dependentGloss'],ed['governor'],ed['dependent'])


