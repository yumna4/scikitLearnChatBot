from pycorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://localhost:9000')
import nltk

def extractEntity(sentence):
    res = nlp.annotate(sentence,properties={'annotators': 'depparse','outputFormat': 'json', 'timeout': 1000,})

    for s in res['sentences']:
        ED= s['enhancedDependencies']
    for ed in ED:
        print "type: %s words:'%s', %s : %d , %d" % (ed['dep'], ed['governorGloss'], ed['dependentGloss'],ed['governor'],ed['dependent'])
    print ""
    NLQuery=sentence
    words=nltk.word_tokenize(NLQuery)
    tags =nltk.pos_tag(words)
    print tags
    print ""


#
extractEntity("Give me the temperatures above 25 along with roomids")
extractEntity("Show the RoomNo which have a temperature higher than 20 degrees")
extractEntity("what is the RoomNo which have a Temperature higher than 20 degrees")