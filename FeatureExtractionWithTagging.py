from nltk.stem.snowball import SnowballStemmer
stemmer=SnowballStemmer("english")
import nltk
import operator

tags=['VBG', 'VBN', 'VBP', 'WDT', 'JJ', 'VBZ', 'DT', 'NN','PRP', 'RB', 'NNS', 'NNP', 'VB', 'CC', 'PDT', 'CD', 'IN','FUNCTION1','FUNCTION2','FUNCTION3','FUNCTION4','FUNCTION6','FUNCTION7','FUNCTION8','FUNCTION9','FUNCTION10','FUNCTION13']
# tags=['PRP$', 'VBG', 'VBD', 'VBN', 'VBP', 'WDT', 'JJ', 'VBZ', 'DT', 'RP', 'NN', 'TO', 'PRP', 'RB', 'NNS', 'NNP', 'VB', 'WRB', 'CC', 'PDT', 'RBS', 'CD', 'EX', 'IN', 'JJS', 'JJR','FUNCTION1','FUNCTION2','FUNCTION3','FUNCTION4','FUNCTION5','FUNCTION6','FUNCTION7','FUNCTION8','FUNCTION9','FUNCTION10','FUNCTION13']

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
                # bag.append(0.8)
            else:
                bag.append(0)

        qt=[word[1] for word in sentence]
        # print qt
        qt.extend(labels)
        for tag in tags:
            if tag in qt:
                tagCount[tag]+=1
        # print len(tagCount)
        # print len(tags)
        # print sorted(tagCount.items(), key=operator.itemgetter(1))


        # print tagCount
        # tot=0
        # for i in range (len(tags)):
        #     tot=tot+bag[i]*(2**i)
        # print tot
        # print len(bag)
        return bag
# print sorted(tagCount.items(), key=operator.itemgetter(1))

# f=TaggingPreparer()
# f.prepareTagging("show values greater than 6")
#
