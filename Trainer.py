import json
import pickle
from sklearn import svm
from PrepareNLQuery import NLQueryPreparer

prep=NLQueryPreparer()

class Trainer:


    def createTrainingSet(self):

        # filterModel = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma="auto",tol=1.00500)
        # aggregateModel=svm.OneClassSVM(nu=0.1, kernel="rbf", gamma="auto",tol=1.00500)
        # windowModel =svm.OneClassSVM(nu=0.1, kernel="rbf", gamma="auto",tol=1.00500)
        # groupModel =svm.OneClassSVM(nu=0.1, kernel="rbf", gamma="auto",tol=1.00500)


        windowModel =svm.OneClassSVM(nu=0.1, kernel="linear", gamma="auto",tol=1)
        filterModel = svm.OneClassSVM(nu=0.1, kernel="linear", gamma="auto",tol=1)
        aggregateModel=svm.OneClassSVM(nu=0.1, kernel="linear", gamma="auto",tol=1)
        groupModel=svm.OneClassSVM(nu=0.1, kernel="linear", gamma="auto",tol=1)




        fdoc=[]
        adoc=[]
        wdoc=[]
        gdoc=[]


        with open('intents.json') as json_data:
            intentsData=json.load(json_data)

        for intent in intentsData['intents']:

            for pattern in intent['pattern']:
                if intent['tag']=="filter":
                    fdoc.append(pattern)
                if intent['tag']=="window":
                    wdoc.append(pattern)
                if intent['tag']=="aggre":
                    adoc.append(pattern)
                if intent['tag']=="group":
                    gdoc.append(pattern)

        # code to get all tags
        # tags=[]
        # for NLQuery in documents:
        #     intent=nltk.word_tokenize(NLQuery)
        #     sentence =nltk.pos_tag(intent)
        #
        #     tags.extend([word[1] for word in sentence])
        #
        # tags= set(tags)

        fx_train=[]
        for NLQuery in fdoc:
            bag=prep.prepareNLQuery(NLQuery)


            fx_train.append(bag)

        ax_train=[]
        for NLQuery in adoc:
            bag=prep.prepareNLQuery(NLQuery)

            ax_train.append(bag)

        wx_train=[]
        for NLQuery in wdoc:
            bag=prep.prepareNLQuery(NLQuery)
            wx_train.append(bag)

        gx_train=[]
        for NLQuery in gdoc:
            bag=prep.prepareNLQuery(NLQuery)

            gx_train.append(bag)

        filterModel.fit(fx_train)
        aggregateModel.fit(ax_train)
        windowModel.fit(wx_train)
        groupModel.fit(gx_train)

        filename = 'finalized_windowModel.sav'
        pickle.dump(windowModel, open(filename, 'wb'))


        filename = 'finalized_filterModel.sav'
        pickle.dump(filterModel, open(filename, 'wb'))

        filename = 'finalized_aggregateModel.sav'
        pickle.dump(aggregateModel, open(filename, 'wb'))

        filename = 'finalized_groupModel.sav'
        pickle.dump(groupModel, open(filename, 'wb'))



tr=Trainer()
tr.createTrainingSet()
