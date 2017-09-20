import nltk
import re

class GroupModel:
    documents=[]


    def getGroupFeatures(self,NLQuery):



        grammar = r"""FUNCTION:{(<IN><DT><NN>)|(<NNP><NN>)}"""
        cp = nltk.RegexpParser(grammar)
        intent=nltk.word_tokenize(NLQuery)
        sentence =nltk.pos_tag(intent)


        result = cp.parse(sentence)
        tagsOfQuery=list(result)

        grp1=[]

        for node in range(len(tagsOfQuery)):
            try:
                if result[node].label()=="FUNCTION":
                    grp1.extend(result[node])
            except:
                continue

        if re.findall(' each | per | group | grouping | grouped ',NLQuery):
            grp2=1
        else:
            grp2=0
        #
        # if aggre1:
        #
        #     grp1=1
        # else:
        #
        #     grp1=0
        return [grp2]


