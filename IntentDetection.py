import json
import nltk
from nltk.stem.lancaster import LancasterStemmer
import pickle
from TokenWords import TokenWords
from tdidf import TFIDF
tw=TokenWords()
stemmer = LancasterStemmer()
data = pickle.load(open("training_data", "rb"))
vocabulary = data['vocabulary']
intents = data['intents']
# x_train = data['x_train']
# y_train = data['y_train']



with open('intents.json') as json_data:
    intentsData=json.load(json_data)
all_documents=[]

for intent in intentsData['intents']:

    all_documents.append(intent['pattern'])

h=[]
for i in all_documents:
    h.append(" ".join(i))



all_documents=h

print all_documents

windowModel=pickle.load(open('finalized_windowModel.sav', 'rb'))
aggregateModel=pickle.load(open('finalized_aggregateModel.sav', 'rb'))
filterModel=pickle.load(open('finalized_filterModel.sav', 'rb'))
# partitionModel=pickle.load(open('finalized_partitionModel.sav', 'rb'))

tfidf=TFIDF()

class IntentDetector:
    #
    # def findIntentNumber(self,bag):
    #
    #     predictedIntentNumber=model.predict([bag])
    #     if predictedIntentNumber in y_train:
    #         return predictedIntentNumber
    #     else:
    #         return "try another way"

    def detectIntent(self, NLQuery):

        w=nltk.word_tokenize(NLQuery)
        all_documents.append(NLQuery)
        wordsPattern=
        # wordsPattern=tw.getTokenWordsPattern(w)
        print wordsPattern

        window=(windowModel.predict(wordsPattern))
        print window
        aggregate=(aggregateModel.predict(wordsPattern))
        print aggregate
        filter =filterModel.predict(wordsPattern)
        print filter
        # sequence=(sequenceModel.predict(wordsPattern))
        # partition=(partitionModel.predict(wordsPattern))
        # print window, pattern, sequence, partition
        # answer=[]
        # answer.extend(window)
        # answer.extend(pattern)
        # answer.extend(sequence)
        # answer.extend(partition)
        #pri # for i in binary:
        #     ans.append(int(float(i)))
        # print ans binary
        # binary = [item for sublist in binary for item in sublist]
        #
        # intent=[]
        # result=["window", "pattern","sequence","partition","mathematical","logical","function","aggregate","group","filter","Output event category","output rate limiting","","","",""]
        # for i in range (len(answer)):
        #
        #      if answer[i]==1:
        #          intent.append(result[i])
        # print intent
        # return intent


id=IntentDetector()
print "one"
id.detectIntent("average maximum")
print "two"
id.detectIntent("last minute")
