from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

class TFIDF:

    def getIDF(self,train_set):
        ignoreWords=["events", "event","stream","a", "about", "all", "also", "and", "as", "at", "be", "because", "but", "by", "can", "come", "could", "day", "do", "even", "find", "first", "for", "from", "get", "give", "go", "have", "he", "her", "here", "him", "his", "how", "I", "if", "in", "into", "it", "its", "just", "know", "like", "look", "make", "man", "many", "me", "more", "my", "new", "no", "not", "now", "of", "on", "one", "only", "or", "other", "our", "out", "people", "say", "see", "she", "so", "some", "take", "tell", "than", "that", "the", "their", "them", "then", "there", "these", "they", "thing", "think", "this", "those", "time", "to", "two", "up", "use", "very", "want", "way", "we", "well", "what", "when", "which", "who", "will", "with", "would", "year", "you"," your"]

        count_vectorizer = CountVectorizer(stop_words=ignoreWords)

        count_vectorizer.fit_transform(train_set)
        # print count_vectorizer.vocabulary_
        tfidf = TfidfTransformer(norm="l2" ,use_idf=True)
        freq_term_matrix = count_vectorizer.transform(train_set)
        print count_vectorizer.vocabulary_

        tfidf.fit(freq_term_matrix)

        # print tfidf.idf_
        print count_vectorizer.vocabulary_
        return count_vectorizer,tfidf


    def getTFIDF(self,document,count_vectorizer,tfidf):


        freq_term_matrix = count_vectorizer.transform(document)


        tf_idf_matrix = tfidf.transform(freq_term_matrix)


        return  tf_idf_matrix.todense()



