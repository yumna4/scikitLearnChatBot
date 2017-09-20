import json
import pickle
from sklearn import svm
from FilterFeatures import FilterModel
from AggregateFunctionFeatures import AggregateFunctionModel
from WindowFeatures import WindowModel
import matplotlib.pyplot as plt
class Trainer:


    def createTrainingSet(self):

        filterModel = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma="auto",tol=1.00500)
        aggregateModel=svm.OneClassSVM(nu=0.1, kernel="rbf", gamma="auto",tol=1.00500)
        windowModel =svm.OneClassSVM(nu=0.1, kernel="rbf", gamma="auto",tol=1.00500)



        fdoc=[]
        adoc=[]
        wdoc=[]

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





        fm=FilterModel()
        fx_train=[]
        for NLQuery in fdoc:
            fx_train.append(fm.getFilterFeatures(NLQuery))


        afm=AggregateFunctionModel()
        ax_train=[]
        for NLQuery in adoc:
            ax_train.append(afm.getAggregateFunctionFeatures(NLQuery))


        wm=WindowModel()
        wx_train=[]
        for NLQuery in wdoc:
            wx_train.append(wm.getWindowFeatures(NLQuery))


        filterModel.fit(fx_train)
        aggregateModel.fit(ax_train)
        windowModel.fit(wx_train)

        filename = 'finalized_windowModel.sav'
        pickle.dump(windowModel, open(filename, 'wb'))


        filename = 'finalized_filterModel.sav'
        pickle.dump(filterModel, open(filename, 'wb'))

        filename = 'finalized_aggregateModel.sav'
        pickle.dump(aggregateModel, open(filename, 'wb'))


tr=Trainer()
tr.createTrainingSet()
