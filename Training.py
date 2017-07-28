import json
import nltk
from nltk.stem.lancaster import LancasterStemmer
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import pickle


with open('intents.json') as json_data:
    intents=json.load(json_data)
global model
MLmodel = svm.SVC(kernel='rbf',max_iter=-1,)

stemmer = LancasterStemmer()


class Trainer:

    def createModel(self):
        global  words
        words=[]
        # possible words that the user can give as input
        global  documents
        documents=[] # contains match of every word with its intent (pattern)
        global  classes
        classes=[]#possible intents/patterns/classes
        global training
        training=[]
        for intent in intents['intents']:
            for pattern in intent['pattern']:
                w=nltk.word_tokenize(pattern)
                words.extend(w)
                documents.append((w,intent['value']))
                if intent['tag'] not in classes:
                    classes.append(intent['tag'])

        words= [stemmer.stem(w.lower()) for w in words]
        words = sorted(list(set(words)))

        classes = sorted(list(set(classes)))
        output_empty=[0]*len(classes)


        for doc in documents:

            bag=[]
            pattern_words=doc[0]
            pattern_words = [stemmer.stem(w.lower()) for w in pattern_words]
            for w in words:
                bag.append(1) if w in pattern_words else bag.append(0)
                value=doc[1]
                training.append([bag,value])
        self.trainModel(training)




    def trainModel(self,training):

        x=[element[0] for element in training]
        y  =[element[1] for element in training]
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)
        #model = MLPClassifier ( solver = 'lbfgs', max_iter = 2000 )
        model=MLmodel.fit(x_train,y_train)
        predictions=model.predict(x_test)
        print "Accuracy of testing results is:"
        print accuracy_score(y_test, predictions)
        filename = 'finalized_model.sav'
        print len(words)
        pickle.dump(model, open(filename, 'wb'))

        #model.save('model.sklearn')

        pickle.dump({'words': words, 'classes': classes, 'x_train': x_train, 'y_train': y_train}, open("training_data", "wb"))

#
# def createModel():
#     global  words
#     words=[]
#     # possible words that the user can give as input
#     global  documents
#     documents=[] # contains match of every word with its intent (pattern)
#     global  classes
#     classes=[]#possible intents/patterns/classes
#     for intent in intents['intents']:
#         for pattern in intent['pattern']:
#             w=nltk.word_tokenize(pattern)
#             words.extend(w)
#             documents.append((w,intent['value']))
#             if intent['tag'] not in classes:
#                 classes.append(intent['tag'])
#
#     words= [stemmer.stem(w.lower()) for w in words]
#     words = sorted(list(set(words)))
#     classes = sorted(list(set(classes)))
#     output_empty=[0]*len(classes)
#
#     global training
#     training=[]
#     for doc in documents:
#
#         bag=[]
#         pattern_words=doc[0]
#         pattern_words = [stemmer.stem(w.lower()) for w in pattern_words]
#         for w in words:
#             bag.append(1) if w in pattern_words else bag.append(0)
#             value=doc[1]
#             training.append([bag,value])
#     print training
#     trainModel(training)
#
#
#
#
# def trainModel(training):
#
#     x=[element[0] for element in training]
#     y  =[element[1] for element in training]
#     x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)
#     #model = MLPClassifier ( solver = 'lbfgs', max_iter = 2000 )
#     model=MLmodel.fit(x_train,y_train)
#     predictions=model.predict(x_test)
#     print "Accuracy of testing results is:"
#     print accuracy_score(y_test, predictions)
#     filename = 'finalized_model.sav'
#
#     pickle.dump(model, open(filename, 'wb'))
   # def getModel(self):
#         return model
# tr=Trainer()
# tr.createModel()