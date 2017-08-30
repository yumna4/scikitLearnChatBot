import json
import nltk
from nltk.stem.lancaster import LancasterStemmer
import pickle
from TokenWords import TokenWords
from tfidf import TFIDF
tw=TokenWords()
stemmer = LancasterStemmer()
data = pickle.load(open("training_data", "rb"))
vocabulary = data['vocabulary']
intents = data['intents']
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
from Training import Trainer

tr=Trainer()
tr.createTrainingSet()


with open('intents.json') as json_data:
    intentsData=json.load(json_data)
documents=[]

for intent in intentsData['intents']:

    documents.append(intent['pattern'])



h=[]
for i in documents:
    for j in i:
        h.append("".join(j))





documents=h


all_documents=[]
for doc in documents:

    doc=doc.split()

    doc= [stemmer.stem(word.lower()) for word in doc]

    all_documents.append(doc)



b=[]
for i in all_documents:

    a=" ".join(i)

    b.append(a)

all_documents=b

windowModel=pickle.load(open('finalized_windowModel.sav', 'rb'))
filterModel=pickle.load(open('finalized_filterModel.sav', 'rb'))



class IntentDetector:
    tfidf=TFIDF()
    def detectIntent(self, NLQuery):
        NLQuery=NLQuery.split()
        NLQuery=[stemmer.stem(word.lower()) for word in NLQuery]

        NLQuery=" ".join(NLQuery)


        all_documents.append(NLQuery)


        a=self.tfidf.getTFIDF(all_documents)
        wordsPattern= a[-1]

        window=(windowModel.predict(wordsPattern))
        print window

        filter =filterModel.predict(wordsPattern)
        print filter
        #


id=IntentDetector()
print "one"
id.detectIntent("give me the averages above 30 of in past 10 minutes")
print "should be 1,1"
print "two"
id.detectIntent("Show the greater than 60")
print "should be -1, 1"
print "three"
id.detectIntent("last 10 minutes")
print "should be 1, -1"