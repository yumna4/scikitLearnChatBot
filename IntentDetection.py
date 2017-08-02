import json
import nltk
from nltk.stem.lancaster import LancasterStemmer
import pickle


stemmer = LancasterStemmer()
data = pickle.load(open("training_data", "rb"))
vocabulary = data['vocabulary']
intents = data['intents']
x_train = data['x_train']
y_train = data['y_train']


with open('intents.json') as json_data:
    intents = json.load(json_data)
model=pickle.load(open('finalized_model.sav', 'rb'))


class IntentDetector:

    def findIntentNumber(self,bag):
        print bag
        predictedIntentNumber=model.predict([bag])
        if predictedIntentNumber in y_train:
            return predictedIntentNumber
        else:
            return "try another way"

    def detectIntent(self, NLQuery):
        wordsInQuery=nltk.word_tokenize(NLQuery)
        wordsInQuery= [stemmer.stem(w.lower()) for w in wordsInQuery]
        bag=[]
        print vocabulary
        for w in vocabulary:
            bag.append(1) if w in wordsInQuery else bag.append(0)

        predictedIntentNumber=IntentDetector.findIntentNumber(self,bag)
        for intent in intents['intents']:
            if intent['number']==predictedIntentNumber:
                return intent['responses']


