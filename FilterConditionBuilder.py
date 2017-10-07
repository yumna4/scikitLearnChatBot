from sklearn import svm
from nltk.stem.snowball import SnowballStemmer
import json
import nltk
from nltk.corpus import dependency_treebank as dtb
from nltk.corpus import wordnet as wn
from sklearn.metrics import accuracy_score
from sklearn.cross_validation import train_test_split
import pickle
import matplotlib.pyplot as plt


stemmer=SnowballStemmer("english")
MLmodel = svm.SVC(C=10, cache_size=200, class_weight=None, coef0=0.0,decision_function_shape='ovo', gamma='auto', kernel='linear',max_iter=200, probability=False, random_state=None, shrinking=True,tol=0.001, verbose=False) #creates an SVM model

with open('intents.json') as json_data:
    intentsData=json.load(json_data)

class FilterFinder:


    greaterWords=[wn.synsets('greater')[0],wn.synsets('higher')[0],wn.synsets('bigger')[0],wn.synsets('above')[0],wn.synsets('more')[0],wn.synsets('larger')[0]]
    smallerWords=[wn.synsets('smaller')[0],wn.synsets('lower')[1],wn.synsets('below')[0],wn.synsets('lesser')[1],wn.synsets('less')[1],wn.synsets('fewer')[0],wn.synsets('littler')[0]]
    equalWords=[wn.synsets('equal')[1],wn.synsets('same')[2]]

    value=[]
    def prepare(self,NLQuery):
        # print NLQuery
        grammar = r"""FUNCTION:{(<JJ><IN><CD>)   |(<JJR><IN><CD>)   |     (<IN><CD><CC><CD>)     |(<IN><CD>)   |     (<JJ><TO><CD>)     |     (<VBP><TO><CD>)}"""


        cp = nltk.RegexpParser(grammar)
        intent=nltk.word_tokenize(NLQuery)
        sentence =nltk.pos_tag(intent)
        result = cp.parse(sentence)
        tagsOfQuery=list(result)

        filter=[]
        # print tagsOfQuery
        for node in range(len(tagsOfQuery)):
            try:
                if result[node].label()=="FUNCTION":
                    filter.extend(result[node])
            except:
                continue
        print filter
        self.value=[filter[i][0] for i in range(len(list(filter)))]
        # print self.value

        self.value=[int(s) for s in self.value if s.isdigit()]

        # print self.value
        tags=[filter[i][1] for i in range(len(list(filter)))]

        universalTagList=["JJR","IN","CD", "CC","JJ","TO"]

        bag=[]

        for w in universalTagList:

            bag.append(1) if w in tags else bag.append(0)






        filterWord=(str(filter[0][0]))
        # print filterWord
        if filterWord=='same':
            filterWord=wn.synsets(filterWord)[2]
        elif filterWord in ["equal","lower","less","lesser"]:
            filterWord=wn.synsets(filterWord)[1]
        else:
            filterWord=wn.synsets(filterWord)[0]


        greater=0
        for synset in self.greaterWords:
            try:
                greater+=filterWord.wup_similarity(synset)
            except:
                continue

        smaller=0
        for synset in self.smallerWords:
            try:
                smaller+=filterWord.wup_similarity(synset)
            except:
                continue

        equal=0
        for synset in self.equalWords:
            try:
                equal+=filterWord.wup_similarity(synset)
            except:
                continue


        d=[greater/0.6,smaller/0.7,equal/0.2]
        # print d

        bag.extend(d)

        # print bag
        return bag

    def getValues(self):
        return self.value
    def createModelForFindingFilter(self):
        trainingData=[]



        for intent in intentsData['intents']:
            if intent['tag']=='filter':
                i=0
                for pattern in intent['pattern']:
                    temp=[pattern]
                    a=intent['filterType'][i]

                    temp.append(int(a))
                    i+=1

                    trainingData.append(temp)



        # print trainingData
        x_train=[]
        y_train=[]
        for each in trainingData:
            prepared=self.prepare(each[0])
            x=(prepared)
            y=each[1]
            x_train.append(x)
            y_train.append(y)
        #
        # print x_train
        # print y_train

        x_ftrain, x_test, y_ftrain, y_test = train_test_split(x_train, y_train, test_size=0.3)

        model=MLmodel.fit([x_ftrain,y_ftrain])
        predictions=model.predict([x_test])

        # print "Accuracy of testing results is:"
        # print x_train
        # print ()
        # print y_train
        # print ()
        # print x_test
        # print ()
        # print y_test
        # print ()
        # print list(predictions)
        # print ()


        print accuracy_score([y_test, list(predictions)])
        filename = 'findfilter_model.sav'
        pickle.dump(model, open(filename, 'wb'))



# ff=FilterFinder()
# ff.createModelForFindingFilter()\

