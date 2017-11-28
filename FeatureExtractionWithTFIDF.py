from sklearn.metrics.pairwise import cosine_similarity

class TFIDFPreparer:
    def prepareTextForTFIDF(self,NLQuery):
        NLQuery=NLQuery.lower().split()

        for n,word in enumerate(NLQuery):
            if word.isdigit():
                NLQuery[n]="number"

        return NLQuery

    # the similarity between the tfidf of a given query and the tfidf of each of the other queries in a class of intents is calculated, and the sum is returned
    def getSumOfCosineSimilarity(self,tfidf_value, tfidf_matrix):
        a= cosine_similarity(tfidf_value,tfidf_matrix)
        for i in list(a):
            a=i
        b= list(a)
        total=0
        for i in b:
            total=total+i
        return total


