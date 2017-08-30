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
# x_train = data['x_train']
# from typeDependencies import TypeDependencies
# y_train = data['y_train']
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()



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

windowModel=pickle.load(open('finalized_windowModel.sav', 'rb'))
aggregateModel=pickle.load(open('finalized_aggregateModel.sav', 'rb'))
filterModel=pickle.load(open('finalized_filterModel.sav', 'rb'))
# partitionModel=pickle.load(open('finalized_partitionModel.sav', 'rb'))



class IntentDetector:
    tfidf=TFIDF()
    # TD=TypeDependencies()
    def detectIntent(self, NLQuery):
        NLQuery=NLQuery.split()
        NLQuery=[stemmer.stem(word.lower()) for word in NLQuery]

        NLQuery=" ".join(NLQuery)

        # print self.TD.getStanfordProperties(NLQuery)

        # w=nltk.word_tokenize(NLQuery)
        # all_documents.append(NLQuery)


        all_documents.append(NLQuery)


        a=self.tfidf.getTFIDF(all_documents)
        wordsPattern= a[-1]

        window=(windowModel.predict(wordsPattern))
        print window
        #
        # # wordsPattern=tw.getTokenWordsPattern(w)
        # print wordsPattern
        #

        # # aggregate=(aggregateModel.predict(wordsPattern))
        # # print aggregate
        filter =filterModel.predict(wordsPattern)
        print filter
        #


id=IntentDetector()
print "one"
id.detectIntent("greater than")
print "two"
id.detectIntent("Show the greater than 60 with")
