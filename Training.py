import json
import nltk
from nltk.stem.lancaster import LancasterStemmer
from sklearn import svm
from TokenWords import TokenWords
from tfidf import TFIDF
# from typeDependencies import TypeDependencies
from sklearn.metrics import accuracy_score
# from sklearn.model_selection import train_test_split
import pickle
stemmer = LancasterStemmer()




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



# td=TypeDependencies()
tw=TokenWords()
#

# tfidf=list(tfidf)


with open('intents.json') as json_data:
    intentsData=json.load(json_data)


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


# print countList
documents=h


#
# typeDependenciesList=[]
#
# for i in all_documents:
#     # print i
#     i=i.replace(u'\xa0',"")
#     a=td.getStanfordProperties(str(i))
#     # print a
#     typeDependenciesList.append(a)

# print "im here"
# print len(typeDependenciesList)
# print typeDependenciesList




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




        self.trainModel("filterTrainingSet")

        self.trainModel("windowTrainingSet")

        # self.trainModel("aggregateFunctionTrainingSet")
        #
        # self.trainModel("filterTrainingSet")
        # #
        # self.trainModel("partitionTrainingSet")



    def trainModel(self,training):
        all_documents=[]

        # tfidf=self.tfidfInstance.getTFIDF(documents)
        for doc in documents:

            doc=doc.split()

            doc= [stemmer.stem(word.lower()) for word in doc]

            all_documents.append(doc)
        b=[]

        for i in all_documents:

            a=" ".join(i)

            b.append(a)
        all_documents=b
        tfidf=self.tfidfInstance.getTFIDF(all_documents)
        print "jj"
        print tfidf[1]

        if training=="windowTrainingSet":
            # x_train=self.windowTrainingSet
            #x_train, x_test = train_test_split(x, test_size=0.1)


            x_train=tfidf[countList[0]:countList[1]+countList[0]]

            windowModel.fit(x_train)
            # print x_test
            # predictions=windowModel.predict(x_test)

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
            x_train=tfidf[0:countList[0]]
            print ("filter")
            # print typeDependenciesList[0:countList[0]]
            #
            # x=x_train
            # x_train=[]



            #
            # for i in range (len(typeDependenciesList[0:countList[0]])):
            #     if "filter" in typeDependenciesList[i]:
            #         filter=1
            #     else:
            #         filter=0
            #     print x[i]
            #     x[i].tolist().append(filter)
            #     x_train.append(x[i])



            print (x_train)
            # print len(x_train)
            #
            filterModel.fit(x_train)

            # sequenceModel.fit(x_train,y_train)
            #
            #
            # # predictions=sequenceModel.predict(x_test)
            #
            # print "Accuracy Score:", accuracy_score(y_test, predictions)



        if training=="partitionTrainingSet":
            x=[element[0] for element in self.partitionTrainingSet]
            y  =[element[1] for element in self.partitionTrainingSet]
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)


            partitionModel.fit(x_train,y_train)


            predictions=partitionModel.predict(x_test)

            print ("Accuracy Score:", accuracy_score(y_test, predictions))



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
