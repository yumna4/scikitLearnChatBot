import json
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer()



documents=[]
with open('intents.json') as json_data:
    intentsData=json.load(json_data)

for intent in intentsData['intents']:
    count=0

    for pattern in intent['pattern']:
        documents.append(pattern)

print documents
stoplist = set('a of the and to in'.split())

texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]
a=[]
streamWords=["temperature","room","id","device","sensor","room number","humidity","temp","temperatures","degree","temps","ids","rooms","numbers","degrees","server"]


for text in texts:
    text=filter(lambda a: a.isdigit()==False , text)


    for word in streamWords:
        text=filter(lambda a: a != word, text)
    a.append(text)


texts=a
from collections import defaultdict
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1
texts = [[token for token in text if frequency[token] > 1] for text in texts]

# from pprint import pprint  # pretty-printer

texts=[' '.join(word) for word in texts]

tfidf_matrix = tfidf_vectorizer.fit_transform(texts)

# freq_term_matrix = count_vectorizer.transform(document)

print tfidf_matrix.shape
print tfidf_matrix

a= cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
print a
index=[]
print texts

for i in a:
    val= list(enumerate(list(i)))
    print val
    for i in val:
        if i[1]>0.3:
            index.append(i[0])

for i in index:
    print i
    print texts[i]