from pycorenlp import StanfordCoreNLP
import json
nlp = StanfordCoreNLP('http://localhost:9000')
from sklearn.model_selection import train_test_split
from sklearn import svm
#
# cd stanford-corenlp-full-2017-06-09
# java -mx5g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 10000


with open('entities.json') as json_data:
     entities=json.load(json_data)


# with open('gettingEntities.json') as json_data:
#     entities=json.load(json_data)


def getEntities(tag):
    for intent in entities['intents']:

        if intent['queryType']==tag:

            return intent['entities']

extracted=[]
extractedEntities=[]
#extracted.append(random.randint(0,101))
def extractEntity(sentence,intent):

    neededEntities=[]
    res = nlp.annotate(sentence,properties={'annotators': 'depparse','outputFormat': 'json', 'timeout': 1000,})
    entities=getEntities(intent)
   # print entities
    for s in res['sentences']:
        ED= s['enhancedDependencies']
    #print ED

    for ed in ED:
        print "type: %s words:'%s', %s : %d , %d" % (ed['dep'], ed['governorGloss'], ed['dependentGloss'],ed['governor'],ed['dependent'])

    if intent=="Stream definition":
        for ed in ED:
            if ed['dep']=="xcomp":
                title=ed['dependentGloss']
                extractedEntities.append(title)
                extracted.append("title")

            elif ed['dep']=="nmod" and ed['dependentGloss'] is not "name" or "title" or "label" or "make" or "create":
                title=ed['dependentGloss']
                extractedEntities.append(title)
                extracted.append("title")
            elif ed["dep"]=="case":
                title=ed['governorGloss']
                extractedEntities.append(title)
                extracted.append("title")
            elif ed["dep"]=="dep":
                if ed['dependentGloss']:
                    title=ed['dependentGloss']
                    extractedEntities.append(title)
                    extracted.append("title")


    if intent=="Rename":
        for ed in ED:
            if ed['dep']=="xcomp":
                title=ed['dependentGloss']
                extractedEntities.append(title)
                extracted.append("title")

    if intent=="Projection":
        for ed in ED:
            if ed['dep']=="xcomp":
                title=ed['dependentGloss']
                extracted.append("title")

    for entity in entities:
        if entity not in extracted:
            neededEntities.append(entity)
            #print neededEntities

    if neededEntities:
        print "Give the following information"
        return neededEntities

    return None

def updateQuery(entity,value):
    extracted.append(entity)
    extractedEntities.append(value)
    #print extracted
    #print extractedEntities
def getExtractedEntities():
    return  extractedEntities

#print extractEntity("make a stream called vythbjk","Stream definition")