from nltk.stem.snowball import SnowballStemmer
stemmer=SnowballStemmer("english")

from sklearn.metrics.pairwise import cosine_similarity

class Preparer:
    def prepare(self,NLQuery):

        stoplist = set('a of the and to in'.split())
        streamWords=["temperature","room","id","device","sensor","room number","humidity","temp","temperatures","degree","temps","ids","rooms","numbers","degrees","server","office","area"]

        NLQuery=NLQuery.lower().split()

        NLQuery=[word for word in NLQuery if word not in stoplist]
        text=filter(lambda a: a.isdigit()==False , NLQuery)

        for word in streamWords:
            text=filter(lambda a: a != word, text)


        return text

    def getSumOfCosineSimilarity(self,tfidf_value, tfidf_matrix):
        a= cosine_similarity(tfidf_value,tfidf_matrix)
        for i in list(a):
            a=i
        b= list(a)
        total=0
        for i in b:
            total=total+i
        return total


