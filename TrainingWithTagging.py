import json
import pickle
from FeatureExtractionWithTagging import TaggingPreparer

taggingPreparer=TaggingPreparer()
from sklearn.svm import SVC

class TaggingTrainer:


    def createTrainingSet(self):

        model = SVC(kernel='rbf')


        x_train=[]
        y_train=[]
        with open('intents2.json') as json_data:
            intentsData=json.load(json_data)
        for intent in intentsData['intents']:
            for pattern in intent['pattern']:
                x_train.append(pattern)
                y_train.append(int(intent['number']))


        train=[]
        for NLQuery in x_train:
            bag,queryChunks=taggingPreparer.prepareTagging(NLQuery)
            train.append(bag)

        x_train=train
        # for i in range(87):
            # print x_train[i],y_train[i]
            # print len(x_train[i])
        model.fit(x_train,y_train)




        filename = 'finalized_TagModel.sav'
        pickle.dump(model, open(filename, 'wb'))



taggingTrainer=TaggingTrainer()
taggingTrainer.createTrainingSet()


