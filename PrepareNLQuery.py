from nltk.stem.snowball import SnowballStemmer
stemmer=SnowballStemmer("english")
import nltk

class NLQueryPreparer:
    def prepareNLQuery(self,NLQuery):

        tags=['PRP$', 'VBG', 'VBD', 'VBN', 'VBP', 'WDT', 'JJ', 'VBZ', 'DT', 'RP', 'NN', ',', 'TO', 'PRP', 'RB', 'NNS', 'NNP', 'VB', 'WRB', 'CC', 'PDT', 'RBS', 'CD', 'EX', 'IN', 'JJS', 'JJR','FUNCTION1','FUNCTION2','FUNCTION3','FUNCTION4','FUNCTION5','FUNCTION6','FUNCTION7','FUNCTION8','FUNCTION9','FUNCTION10']


        grammar =r"""FUNCTION1:{<JJ><IN><CD>}
                     FUNCTION5:{<JJR><IN><CD>}
                     FUNCTION6:{<IN><CD><CC><CD>}
                     FUNCTION7:{<JJ><TO><CD>}
                     FUNCTION8:{<VBP><TO><CD>}
                     FUNCTION9:{<NNP><NN>}
                     FUNCTION10:{<JJ><CD><NNS>}
                     FUNCTION2:{<IN><DT><NN>}
                     FUNCTION3:{<JJ><CD><NN>}
                     FUNCTION4:{<NN><IN>}"""


        cp = nltk.RegexpParser(grammar)

        intent=nltk.word_tokenize(NLQuery)
        sentence =nltk.pos_tag(intent)
        result = cp.parse(sentence)



        sentence=list(result)

        labels=[]
        for i in sentence:
            if  type(i)==nltk.tree.Tree:

                labels.append(i.label())

        queryTags=[word[1] for word in sentence]+labels
        bag=[]
        for tag in tags:

            if tag in queryTags:

                bag.append(1)
            else:
                bag.append(0)




        return bag