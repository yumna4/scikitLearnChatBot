from nltk.stem.snowball import SnowballStemmer
stemmer=SnowballStemmer("english")

class NLQueryPreparer:
    def prepareNLQuery(self,NLQuery,streamWords):
        NLQuery=filter(lambda a: a.isdigit()==False , NLQuery)

        NLQuery=NLQuery.split()

        NLQuery=[word.lower() for word in NLQuery]

        ignoreWords=["is","the","a","me","let","know","get","tell","show","display","notify","inform","identify","alert"]
        for word in ignoreWords:
            NLQuery=filter(lambda a: a != word, NLQuery)


        for word in streamWords:
            NLQuery=filter(lambda a: a != word, NLQuery)


        NLQuery= [stemmer.stem(word) for word in NLQuery]


        NLQuery=(" ".join(NLQuery))


        return NLQuery