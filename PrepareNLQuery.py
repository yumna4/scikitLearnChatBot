from nltk.stem.snowball import SnowballStemmer
stemmer=SnowballStemmer("english")
import re

class NLQueryPreparer:
    def prepareNLQuery(self,NLQuery,streamWords):
        # print NLQuery
        NLQuery=str(NLQuery).replace(",","")
        NLQuery=str(NLQuery).replace(".","")

        NLQuery=filter(lambda a: a.isdigit()==False , NLQuery)

        NLQuery=NLQuery.split()

        # NLQuery=[word.lower() for word in NLQuery]

        ignoreWords=["events", "event","stream","a", "about", "all", "also", "and", "as", "at", "be", "because", "but", "by", "can", "come", "could", "day", "do", "even", "find", "first", "for", "from", "get", "give", "go", "have", "he", "her", "here", "him", "his", "how", "I", "if", "in", "into", "it", "its", "just", "know", "like", "look", "make", "man", "many", "me", "more", "my", "new", "no", "not", "now", "of", "on", "one", "only", "or", "other", "our", "out", "people", "say", "see", "she", "so", "some", "take", "tell", "than", "that", "the", "their", "them", "then", "there", "these", "they", "thing", "think", "this", "those", "time", "to", "two", "up", "use", "very", "want", "way", "we", "well", "what", "when", "which", "who", "will", "with", "would", "year", "you"," your"]

        # ignoreWords=["is","the","a","stream","from","and","of","in","if","for","are","a","along","with","by","their","this","it","has","it's","there"]
        # for word in ignoreWords:
        #     NLQuery=filter(lambda a: a != word, NLQuery)

        for word in streamWords:
            NLQuery=filter(lambda a: a != word, NLQuery)


        NLQuery= [stemmer.stem(word) for word in NLQuery]
        NLQuery=(" ".join(NLQuery))
        NLQuery=re.sub(r'\b\w+\b'and "get|let| me |know|display|show|inform|calcul|emit|identifi|inform|alert|notifi|tell|valu|filter|detail|came|give", "verb", NLQuery,flags=re.IGNORECASE)
        NLQuery=re.sub(r'\b\w+\b'and"second|minut|hour|day|week|month|year", "timevalue", NLQuery,flags=re.IGNORECASE)
        NLQuery=re.sub(r'\b\w+\b'and'last|final|recent|past',"eventTime", NLQuery,flags=re.IGNORECASE)
        NLQuery=re.sub(r'\b\w+\b'and"maximum|greatest|largest|biggest|minimum|smallest|highest|lowest|count|number|add|averag|norm|sum|total|peak|most", "aggregateword", NLQuery,flags=re.IGNORECASE)
        NLQuery=re.sub(r'\b\w+\b'and"greater|smaller|lower|between|higher|bigger|abov|below|more|less", "filterword", NLQuery,flags=re.IGNORECASE)
        NLQuery=re.sub(r'\b\w+\b'and"which|that|whatev|whichev", "describer", NLQuery,flags=re.IGNORECASE)
        NLQuery=re.sub(r'\b\w+\b'and"within|inside|between", "placedescriber", NLQuery,flags=re.IGNORECASE)
        NLQuery=re.sub(r'\b\w+\b'and"per|each|group", "group", NLQuery,flags=re.IGNORECASE)

        NLQuery=str(NLQuery).replace("verb","")

        # print NLQuery
        return NLQuery