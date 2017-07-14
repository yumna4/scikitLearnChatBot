import json
import nltk
from nltk.stem.lancaster import LancasterStemmer
from sklearn.neural_network import MLPClassifier

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
        documents.append((w,intent['tag']))
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
    temp=list(output_empty)
    temp[classes.index(doc[1])]=1
    training.append([bag,temp])

x_train=[element[0] for element in training]
y_train =[element[1] for element in training]

model = MLPClassifier ( solver = 'lbfgs', max_iter = 2000 )
model=model.fit(x_train,y_train)

def find_class(bag):
    result=model.predict([bag])
    result = [item for sublist in result for item in sublist]
    if result in y_train:
        fclassnum= y_train.index(result)
    else:
        return "try another way"
    fclass=documents[fclassnum][1]
    return fclass

def response(sentence):
    sentence_words=nltk.word_tokenize(sentence)
    sentence_words= [stemmer.stem(w.lower()) for w in sentence_words]
    bag=[]
    for w in words:
        bag.append(1) if w in sentence_words else bag.append(0)

    results=find_class(bag)
    return results
