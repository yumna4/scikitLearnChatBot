from nltk.stem.snowball import SnowballStemmer
stemmer=SnowballStemmer("english")
import nltk
import operator

# tags=['VBG', 'VBN', 'VBP', 'WDT', 'JJ', 'VBZ', 'DT', 'NN','PRP', 'RB', 'NNS', 'NNP', 'VB', 'CC', 'PDT', 'CD', 'IN','FUNCTION1','FUNCTION2','FUNCTION3','FUNCTION4','FUNCTION6','FUNCTION7','FUNCTION8','FUNCTION9','FUNCTION10','FUNCTION13']
# tags=['PRP$', 'VBG', 'VBD', 'VBN', 'VBP', 'WDT', 'JJ', 'VBZ', 'DT', 'RP', 'NN', 'TO', 'PRP', 'RB', 'NNS', 'NNP', 'VB', 'WRB', 'CC', 'PDT', 'RBS', 'CD', 'EX', 'IN', 'JJS', 'JJR','FUNCTION1','FUNCTION2','FUNCTION3','FUNCTION4','FUNCTION5','FUNCTION6','FUNCTION7','FUNCTION8','FUNCTION9','FUNCTION10','FUNCTION13']
tags=['VBG', 'VBN', 'VBP', 'WDT', 'JJ', 'VBZ', 'DT', 'NN','PRP', 'RB', 'NNS', 'NNP', 'VB', 'CC', 'PDT', 'CD', 'IN']

tagCount={}
for tag in tags:
    tagCount[tag]=0

class TaggingPreparer:

    def prepareTagging(self,NLQuery):

        # tags=['PRP$', 'VBG', 'VBD', 'VBN', 'VBP', 'WDT', 'JJ', 'VBZ', 'DT', 'RP', 'NN', 'TO', 'PRP', 'RB', 'NNS', 'NNP', 'VB', 'WRB', 'CC', 'PDT', 'RBS', 'CD', 'EX', 'IN', 'JJS', 'JJR','FUNCTION1','FUNCTION2','FUNCTION3','FUNCTION4','FUNCTION5','FUNCTION6','FUNCTION7','FUNCTION8','FUNCTION9','FUNCTION10','FUNCTION13']

# [('FUNCTION5', 0), ('JJR', 0), ('RP', 1), ('WRB', 1), ('FUNCTION8', 1), ('JJS', 1),
#
        grammar =r"""FUNCTION1:{(<JJ>|<JJR>)<IN><CD>}
                     FUNCTION5:{<JJR><IN><CD>}
                     FUNCTION6:{<IN><CD><CC><CD>}
                     FUNCTION7:{<JJ><TO><CD>}
                     FUNCTION8:{<VBP><TO><CD>}
                     FUNCTION9:{<NNP><NN>}
                     FUNCTION10:{(<VBG>|<VBN>|<VBD>)<IN>(<NN>|<NNS>)}
                     FUNCTION13:{(<JJ>|<JJS>)<NN>}
                     FUNCTION2:{<IN><DT><NN>}
                     FUNCTION3:{<JJ><CD>(<NN>|<NNS>)}
                     FUNCTION4:{<NN><IN>}"""


        cp = nltk.RegexpParser(grammar)


        chunks=["JJ IN CD","JJR IN CD","JJR IN CD","IN CD CC CD", "JJ TO CD" ,"VBP TO CD","NNP NN","VBG IN NN","VBG IN NNS"
                "VBN IN NN","VBN IN NNS","VBD IN NN","VBD IN NNS","JJ NN","JJS NN","IN DT NN","JJ CD NN" "JJ CD NNS","NN IN"]


        intent=nltk.word_tokenize(NLQuery)
        sentence =nltk.pos_tag(intent)
        shortTags=[tag[1] for tag in sentence]
        shortTags=' '.join(shortTags)

        queryChunks=[]
        for chunk in chunks:
            if chunk in shortTags:
                queryChunks.append(chunk)


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
        return bag,queryChunks


    def getBag(self,chunk):
        queryTags=chunk.split()


        bag=[]

        for tag in tags:

            if tag in queryTags:

                bag.append(1)

            else:
                bag.append(0)

        return bag

