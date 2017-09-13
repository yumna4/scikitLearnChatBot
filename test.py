import json
import nltk
with open('intents.json') as json_data:
    intentsData=json.load(json_data)
documents=[]

for intent in intentsData['intents']:
    documents.append(intent['pattern'])

h=[]

for i in documents:
    for j in i:
        h.append("".join(j))
documents=h

for intent in documents:
    # print intent
    intent=nltk.word_tokenize(intent)
    # print nltk.pos_tag(intent)
    # print ""
    # print ""


grammar = r"""FUNCTION:{<JJR><IN><CD>|<IN><CD><CC><CD>|<IN><CD>}"""
cp = nltk.RegexpParser(grammar)




for intent in documents:
    print intent
    intent=nltk.word_tokenize(intent)
    sentence =nltk.pos_tag(intent)
    result = cp.parse(sentence)
    # result.draw()
    s=list(result)
    print result
    for node in range(len(s)):
        try:
            if result[node].label()=="FUNCTION":
                filter=result[node]
        except:
            continue

    # print result
    print ""
    print ""

