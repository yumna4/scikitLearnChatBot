from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

class TFIDF:

    def getIDF(self,train_set):

        count_vectorizer = CountVectorizer()

        count_vectorizer.fit_transform(train_set)

        tfidf = TfidfTransformer(norm="l2")
        freq_term_matrix = count_vectorizer.transform(train_set)


        tfidf.fit(freq_term_matrix)


        return count_vectorizer,tfidf


    def getTFIDF(self,document,count_vectorizer,tfidf):


        freq_term_matrix = count_vectorizer.transform(document)


        tf_idf_matrix = tfidf.transform(freq_term_matrix)


        return  tf_idf_matrix.todense()



