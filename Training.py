import json
import nltk
from sklearn.metrics import explained_variance_score
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import pickle
from sklearn import svm
from sklearn import linear_model
from TokenWords import TokenWords

from tdidf import TFIDF

from sklearn.neural_network import MLPRegressor
from sklearn.neural_network import MLPClassifier


from sklearn import linear_model
#model = linear_model.LinearRegression()
#model = Pipeline([('poly', PolynomialFeatures(degree=3)),('linear', LinearRegression(fit_intercept=False))])
#model = linear_model.RidgeCV(alphas=[0.1, 1.0, 10.0])
windowModel =svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
patternModel = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
sequenceModel = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
partitionModel = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
mathematicalOperationModel = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
logicalOperationModel = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
functionModel = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
aggregateFunctionModel = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
groupModel = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
filterModel = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
outputEventCategoryModel = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
outputRateLimitingModel = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)


# reg = linear_model.BayesianRidge()
#model = MLPRegressor ( solver = 'lbfgs', max_iter = 200 )
#model = MLPClassifier ( solver = 'lbfgs', max_iter = 2000 )
tw=TokenWords()
#

# tfidf=list(tfidf)


with open('intents.json') as json_data:
    intentsData=json.load(json_data)


all_documents=[]

for intent in intentsData['intents']:

    all_documents.append(intent['pattern'])

h=[]
for i in all_documents:
    h.append(" ".join(i))



all_documents=h
tfidf=TFIDF()
tfidf=tfidf.getTFIDF(all_documents)

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








        self.trainModel("windowTrainingSet")

        self.trainModel("aggregateFunctionTrainingSet")

        self.trainModel("filterTrainingSet")
        #
        # self.trainModel("partitionTrainingSet")



    def trainModel(self,training):


        if training=="windowTrainingSet":
            # x_train=self.windowTrainingSet
            #x_train, x_test = train_test_split(x, test_size=0.1)
            x_train=tfidf[1]
            # print x_train
            windowModel.fit(x_train)
            # print x_test
            # predictions=windowModel.predict(x_test)
            # print predictions
            #print "Accuracy Score:", accuracy_score(y_test, predictions)


        if training=="aggregateFunctionTrainingSet":
            # x=[element[0] for element in self.patternTrainingSet]
            # y  =[element[1] for element in self.patternTrainingSet]
            # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
            # x_train=self.aggregateFunctionTrainingSet
            x_train=tfidf[2]
            aggregateFunctionModel.fit(x_train)
            #
            #
            # predictions=patternModel.predict(x_test)
            #
            # print "Accuracy Score:", accuracy_score(y_test, predictions)


        if training=="filterTrainingSet":
            x_train=tfidf[0]
            # x=[element[0] for element in self.sequenceTrainingSet]
            # print self.sequenceTrainingSet
            # y  =[element[1] for element in self.sequenceTrainingSet]
            # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
            # x_train=self.filterTrainingSet

            filterModel.fit(x_train)

            # sequenceModel.fit(x_train,y_train)
            #
            #
            # # predictions=sequenceModel.predict(x_test)
            #
            # print "Accuracy Score:", accuracy_score(y_test, predictions)
            #


        if training=="partitionTrainingSet":
            x=[element[0] for element in self.partitionTrainingSet]
            y  =[element[1] for element in self.partitionTrainingSet]
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)


            partitionModel.fit(x_train,y_train)


            predictions=partitionModel.predict(x_test)

            print "Accuracy Score:", accuracy_score(y_test, predictions)



        filename = 'finalized_windowModel.sav'
        pickle.dump(windowModel, open(filename, 'wb'))

        filename = 'finalized_aggregateModel.sav'
        pickle.dump(aggregateFunctionModel, open(filename, 'wb'))

        filename = 'finalized_filterModel.sav'
        pickle.dump(filterModel, open(filename, 'wb'))

        # filename = 'finalized_partitionModel.sav'
        # pickle.dump(partitionModel, open(filename, 'wb'))

        #pickle.dump({'vocabulary': self.vocabulary, 'intents': self.intents, 'x_train': x_train, 'y_train': y_train}, open("training_data", "wb"))

tr=Trainer()
tr.createTrainingSet()
