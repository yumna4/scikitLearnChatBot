import json
import nltk
from nltk.stem.lancaster import LancasterStemmer
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.cross_validation import train_test_split

with open('intents.json') as json_data:
    intents=json.load(json_data)

stemmer = LancasterStemmer()

words=[]# possible words that the user can give as input
documents=[] # contains match of every word with its intent (pattern)
classes=[]#possible intents/patterns/classes
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


x=[element[0] for element in training]

y  =[element[1] for element in training]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.5)

model = MLPClassifier ( solver = 'lbfgs', max_iter = 2000 )
model=model.fit(x_train,y_train)


predictions=model.predict(x_test)
print "Accuracy of testing results are:"
print accuracy_score(y_test, predictions)



def find_class(bag):
    result=model.predict([bag])
    if result in y_train:

        return result
    else:
        return "try another way"

def response(sentence):
    sentence_words=nltk.word_tokenize(sentence)
    sentence_words= [stemmer.stem(w.lower()) for w in sentence_words]
    bag=[]
    for w in words:
        bag.append(1) if w in sentence_words else bag.append(0)

    results=find_class(bag)

    for intent in intents['intents']:
        if intent['value']==results:
            return intent['responses']
