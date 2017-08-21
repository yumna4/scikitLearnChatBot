import json
import nltk
from nltk.stem.lancaster import LancasterStemmer
import pickle
from TokenWords import TokenWords

tw=TokenWords()
stemmer = LancasterStemmer()
data = pickle.load(open("training_data", "rb"))
vocabulary = data['vocabulary']
intents = data['intents']
# x_train = data['x_train']
# y_train = data['y_train']


with open('intents.json') as json_data:
    intents = json.load(json_data)

windowModel=pickle.load(open('finalized_windowModel.sav', 'rb'))
patternModel=pickle.load(open('finalized_patternModel.sav', 'rb'))
sequenceModel=pickle.load(open('finalized_sequenceModel.sav', 'rb'))
partitionModel=pickle.load(open('finalized_partitionModel.sav', 'rb'))



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

        wordsPattern=tw.getTokenWordsPattern(w)
        print wordsPattern

        window=(windowModel.predict(wordsPattern))
        print window
        pattern=(patternModel.predict(wordsPattern))
        print pattern
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
id.detectIntent("within")
print "two"
id.detectIntent("Show the temp and room IDs that came in the last 10 minutes")
