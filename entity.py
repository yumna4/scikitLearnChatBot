from pycorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://localhost:9000')

for s in res['sentences']:
    ED= s['enhancedDependencies']

for ed in ED:
    print "type: %s words:'%s', %s : %d , %d" % (ed['dep'], ed['governorGloss'], ed['dependentGloss'],ed['governor'],ed['dependent'])



with open('entities.json') as json_data:
    entities=json.load(json_data)


def getEntities(tag):
    for intent in entities['intents']:
        if intent['queryType']==tag:
            return intent['entities']


def extractEntity(sentence,intent):
    res = nlp.annotate(sentence,properties={'annotators': 'depparse','outputFormat': 'json', 'timeout': 1000,})
    entities=getEntities(intent)
    print entities
    print res
    #tokens = nltk.word_tokenize(sentence)
    #tokens= [stemmer.stem(w.lower()) for w in tokens]
    #tagged = nltk.pos_tag(tokens)
    #entities = nltk.chunk.ne_chunk(sentence)
    text = pos_tagger.tag(word_tokenize(sentence))
    #print tagged
    print(text)
