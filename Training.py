import json
import nltk
from nltk.stem.lancaster import LancasterStemmer
from sklearn import svm
from TokenWords import TokenWords
from tfidf import TFIDF
import pickle
stemmer = LancasterStemmer()
import joblib




windowModel =svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
filterModel = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)


tw=TokenWords()

with open('intents.json') as json_data:
    intentsData=json.load(json_data)


ignoreWords=["is","the","a"]


documents=[]
countList=[]
for intent in intentsData['intents']:
    count=0
    documents.append(intent['pattern'])
    for pattern in intent['pattern']:
        count+=1
    countList.append(count)

h=[]

for i in documents:
    for j in i:
        h.append("".join(j))



documents=h

class Trainer:

    vocabulary=[]# possible words that the user can give as input
    intentForWord=[] # contains match of every word with its intent (pattern)
    intents=[]#possible intents/patterns/classes


    windowTrainingSet=[] # the data set that will be used for training the bot
    patternTrainingSet=[]
    sequenceTrainingSet=[] # the data set that will be used for training the bot
    partitionTrainingSet=[]
    aggregateFunctionTrainingSet=[]
    filterTrainingSet=[]
    tfidfInstance=TFIDF()
    all_documents=[]




    def createTrainingSet(self):
        for intent in intentsData['intents']:
            for pattern in intent['pattern']:

                w=nltk.word_tokenize(pattern)

                wordsPattern=tw.getTokenWordsPattern(w)
                intentNumber = intent ['number']

                if intentNumber==1:
                    self.windowTrainingSet.append(wordsPattern)

                if intentNumber==512:
                    self.filterTrainingSet.append(wordsPattern)

                if intentNumber==128:
                    self.aggregateFunctionTrainingSet.append(wordsPattern)





        for doc in documents:

            doc=doc.split()

            doc= [stemmer.stem(word.lower()) for word in doc]

            self.all_documents.append(doc)
        b=[]


        for word in ignoreWords:

            for query in self.all_documents:
                try:
                    query.remove(word)
                except:
                    continue

        for i in self.all_documents:

            a=" ".join(i)

            b.append(a)
        self.all_documents=b



        self.trainModel("filterTrainingSet")

        self.trainModel("windowTrainingSet")


    def trainModel(self,training):

        tfidf=self.tfidfInstance.getTFIDF(self.all_documents)
        filename = 'Classifier.sav'
        joblib.dump(tfidf, filename)

        if training=="windowTrainingSet":
            x_train=tfidf[countList[0]:countList[1]+countList[0]]
            windowModel.fit(x_train)


        if training=="filterTrainingSet":
            x_train=tfidf[0:countList[0]]
            filterModel.fit(x_train)



        filename = 'finalized_windowModel.sav'
        pickle.dump(windowModel, open(filename, 'wb'))


        filename = 'finalized_filterModel.sav'
        pickle.dump(filterModel, open(filename, 'wb'))


tr=Trainer()
tr.createTrainingSet()
