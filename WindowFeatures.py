import nltk
import re
class WindowModel:
    documents=[]
    def getWindowFeatures(self,NLQuery):
        # print NLQuery


        intent=nltk.word_tokenize(NLQuery)
        sentence =nltk.pos_tag(intent)

        grammar = r"""FUNCTION:{<JJ><CD>(<NN>|<NNS>)}"""
        cp = nltk.RegexpParser(grammar)
        result = cp.parse(sentence)
        tagsOfQuery=list(result)

        window=[]
        for node in range(len(tagsOfQuery)):
            try:
                if result[node].label()=="FUNCTION":
                    window.extend(result[node])
            except:
                continue
        if window:
            win1=1
            # print "YES"
        elif "window" in NLQuery:
            win1=1
            # print "YES"
        else:
            win1=0
            # print "NO"

        value=[int(s) for s in NLQuery if s.isdigit()]

        if value:
            win2=1
        else:
            win2=0
        # print [win1, win2]
        return [win1,win2]


