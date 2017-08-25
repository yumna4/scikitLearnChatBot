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
     # print ""
     # print ""
     # print "New Query"
     # print intent['tag']

     pattern = pattern.replace(u'\xa0', u' ')
     pattern=str(pattern)

     dependencies = nlp.annotate(pattern,properties={'annotators': 'depparse','outputFormat': 'json', 'timeout': 1000,})
     posTags = nlp.annotate(pattern,properties={'annotators': 'pos','outputFormat': 'json', 'timeout': 1000,})
     relation = nlp.annotate(pattern,properties={'annotators': 'relation','outputFormat': 'json', 'timeout': 1000,})

     # print "POS TAGS"
     # print posTags
     # print "Relation"
     # print relation
     # for ps in posTags:
     #     print ps['pos']

     #
     for s in dependencies['sentences']:
          ED= s['enhancedDependencies']

     for i in posTags['sentences']:
         T= i['tokens']



     for ed in ED:
         for t in T:

             # if ed['dep']=="case":
             #    a=ed['dependentGloss']
             #    if t['word']==a and t['pos']=='IN':
             #        print "GROUP"
             #        print pattern
             #
             #

             if ed['dep']=="advmod" or ed['dep']=="amod":

                a=ed['dependentGloss']

                if t['word']==a and t['pos']=='JJR':
                    # print "DOING SOME COMPARISON IN VALUES. CAN BE A FILTER/HAVING/SEQUENCE"
                    print intent['tag']
                    print pattern

             if ed['dep']=="amod":

                a=ed['dependentGloss']

                if t['word']==a and t['pos']=='JJ':
                    #last minute, recent minutes
                    print "window, pattern, sequence"
                    print intent['tag']
                    print pattern

     #     # print "type: %s words:'%s', %s : %d , %d" % (ed['dep'], ed['governorGloss'], ed['dependentGloss'],ed['governor'],ed['dependent'])


#
# patternS = ["Show the temp and room IDs that came in the last 10 minutes", "show the most recent 200 events of temp and room ID","show temp and roomID in the last 200 events"]
# for pattern in patternS:
#
#     print pattern
#     pattern = pattern.replace(u'\xa0', u' ')
#     pattern=str(pattern)
#
#     dependencies = nlp.annotate(pattern,properties={'annotators': 'depparse','outputFormat': 'json', 'timeout': 1000,})
#     posTags = nlp.annotate(pattern,properties={'annotators': 'pos','outputFormat': 'json', 'timeout': 1000,})
#     # relation = nlp.annotate(pattern,properties={'annotators': 'relation','outputFormat': 'json', 'timeout': 1000,})
#     # natlog=nlp.annotate(pattern,properties={'annotators': 'natlog','outputFormat': 'json', 'timeout': 1000,})
#     # sentiment=nlp.annotate(pattern,properties={'annotators': 'sentiment,pos','outputFormat': 'json', 'timeout': 1000,})
#
#
#
#     print "POS TAGS"
#     print posTags
#
#     for s in dependencies['sentences']:
#         ED= s['enhancedDependencies']
#     for ed in ED:
#
#         print "type: %s words:'%s', %s : %d , %d" % (ed['dep'], ed['governorGloss'], ed['dependentGloss'],ed['governor'],ed['dependent'])


