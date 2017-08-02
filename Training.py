import json
import nltk
from nltk.stem.lancaster import LancasterStemmer
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import pickle


stemmer = LancasterStemmer()
with open('intents.json') as json_data:
    intentsData=json.load(json_data)
MLmodel = svm.SVC(kernel='rbf',max_iter=-1,) #creates an SVM model



class Trainer:

    vocabulary=[]# possible words that the user can give as input
    intentForWord=[] # contains match of every word with its intent (pattern)
    intents=[]#possible intents/patterns/classes
    trainingSet=[] # the data set that will be used for training the bot

    def createTrainingSet(self):
        for intent in intentsData['intents']:
            for pattern in intent['pattern']:
                w=nltk.word_tokenize(pattern)
                self.vocabulary.extend(w)
                self.intentForWord.append((w, intent['number']))
                if intent['tag'] not in self.intents:
                    self.intents.append(intent['tag'])

        self.vocabulary= [stemmer.stem(w.lower()) for w in self.vocabulary]

        self.vocabulary = sorted(list(set(self.vocabulary)))


        self.intents = sorted(list(set(self.intents)))



        for each in self.intentForWord:
            bag=[]
            pattern_words=each[0]
            pattern_words = [stemmer.stem(w.lower()) for w in pattern_words]
            for w in self.vocabulary:
                bag.append(1) if w in pattern_words else bag.append(0)
                intentNumber=each[1]
                self.trainingSet.append([bag, intentNumber])

        self.trainModel(self.trainingSet)




    def trainModel(self,training):

        x=[element[0] for element in training]
        y  =[element[1] for element in training]
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)

        model=MLmodel.fit(x_train,y_train)
        predictions=model.predict(x_test)
        print "Accuracy of testing results is:"
        print accuracy_score(y_test, predictions)

        filename = 'finalized_model.sav'
        pickle.dump(model, open(filename, 'wb'))
        pickle.dump({'vocabulary': self.vocabulary, 'intents': self.intents, 'x_train': x_train, 'y_train': y_train}, open("training_data", "wb"))

