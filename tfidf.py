from __future__ import division
from sklearn.feature_extraction.text import TfidfVectorizer

tokenize = lambda doc: doc.lower().split(" ")

#
# document_0="average Show the temperatures greater than 60 degrees with room numbers, Filtering all server rooms having temperature greater then 40 degrees.,Show the server rooms which have a temperature greater than 40 from the temperature stream"
# document_1="get show the average temperature if window time is 10 minutes average temperature of 10 minute window, Show the average of temperature in the last 10 minutes"
# document_2=""


class TFIDF:

    def getTFIDF(self,all_documents):

        sklearn_tfidf = TfidfVectorizer(norm='l2',min_df=0, use_idf=True, smooth_idf=False, sublinear_tf=True, tokenizer=tokenize)
        sklearn_representation = sklearn_tfidf.fit_transform(all_documents)

        return sklearn_representation.todense()


