import json
import nltk
from nltk.stem.lancaster import LancasterStemmer
from Training import Trainer
import pickle


data = pickle.load(open("training_data", "rb"))
words = data['words']

classes = data['classes']
x_train = data['x_train']
y_train = data['y_train']
stemmer = LancasterStemmer()

with open('intents.json') as json_data:
    intents = json.load(json_data)
filename = 'finalized_model.sav'
model = pickle.load(open(filename, 'rb'))

class IntentDetector:




    def find_class(self,bag):
        trainer=Trainer()
        #model=trainer.getModel()
        #print bag
        result=model.predict([bag])

        if result in y_train:
            return result
        else:
            return "try another way"

    def detectIntent(self,sentence):
        #print len(words)
        sentence_words=nltk.word_tokenize(sentence)
        sentence_words= [stemmer.stem(w.lower()) for w in sentence_words]
        bag=[]
        for w in words:
            bag.append(1) if w in sentence_words else bag.append(0)

        results=IntentDetector.find_class(self,bag)

        for intent in intents['intents']:
            if intent['value']==results:
                return intent['responses']
#
# def find_classs(bag):
#     trainer=Trainer()
#     model=trainer.getModel()
#     result=model.predict([bag])
#
#     if result in y_train:
#         return result
#     else:
#         return "try another way"
#
# def detectIntents(self,sentence):
#
#     sentence_words=nltk.word_tokenize(sentence)
#     sentence_words= [stemmer.stem(w.lower()) for w in sentence_words]
#     bag=[]
#     for w in words:
#         bag.append(1) if w in sentence_words else bag.append(0)
#
#     results=IntentDetector.find_classs(self,bag)
#
#     for intent in intents['intents']:
#         if intent['value']==results:
#             return intent['responses']
# rf=IntentDetector()
# rf.detectIntent("sdfghj")