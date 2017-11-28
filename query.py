import nltk
from pycorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://localhost:9000')

# ASSUMPTION: ATTRIBUTE NAMES SHOULD BE ONE WORD AND NO TMULTIPLE WORDS
#assumption: cannot use temperature values. instead just temperatures



class QueryGenerator:
    def generateQuery(self,NLQuery,intents,stream,attributes,entities):


        sampleQuery="from <inputStreamName> [<filterCondition>]#window.<window name>(<windowParameters>) select aggregateWord(<attributes>) as <newAttribute> <attributeNames> group by <groupAttribute> having <havingCondition>"
        sampleQuery=sampleQuery.replace("<inputStreamName>",stream)



        NLQuery=NLQuery.replace(" me "," ")

        words=nltk.word_tokenize(NLQuery)
        tags =nltk.pos_tag(words)

        simple=NLQuery
        #REPLACING WITH CORRECT ATTRIBUTE NAMES, example replacing 'temp' in NLQuery with "Temperature. Note: Sensor will not be able to be replaced with device in this method"

        nouns=[]
        simpleAttributes={}
        for tag in tags:
            if tag[1]=="NN" or tag[1]=="NNS":
                nouns.append(tag[0])
        for word in nouns:
            for attribute in attributes:
                distance=nltk.edit_distance(word,attribute.lower())
                if distance<4:#OR LESS THAN 3
                    NLQuery=NLQuery.replace(word,attribute,1)
                    simpleAttributes[word]=attribute
        words=nltk.word_tokenize(NLQuery)




        if "window" in intents:
            windowType=entities['windowType']
            if windowType=="time":
                value=str(entities['windowValue'])+' '+entities["timeUnit"]
            if windowType=="length":
                value=str(entities['windowValue'])
            sampleQuery=sampleQuery.replace("<window name>",windowType)
            sampleQuery=sampleQuery.replace("<windowParameters>",value)
        else:
            sampleQuery=sampleQuery.replace("#window.<window name>(<windowParameters>)","")





        if "group" in intents:
            groupAttribute=entities['group']
            sampleQuery=sampleQuery.replace("<groupAttribute>",groupAttribute)
        else:
            sampleQuery=sampleQuery.replace("group by <groupAttribute>","")




        # cannot handle when user says coolest room or warmest room
        if "aggregate" in intents:
            word=entities['aggWord']

            aggregate={"max":["maximum","highest","highest","greatest","most"],"min":["minimum","lowest","smallest","least"],"avg":["average"],"sum":["total","sum","summation"],"count":["count"]}
            for key in aggregate.keys():
                if word in aggregate[key]:
                    aggregateWord=key
            aggregateAttribute=entities['aggregate']
            newAttribute=aggregateWord+aggregateAttribute
            aggregateExpression=aggregateWord+"("+aggregateAttribute+")"+" as "+newAttribute
            sampleQuery=sampleQuery.replace("aggregateWord(<attributes>) as <newAttribute>",aggregateExpression)
        else:
            sampleQuery=sampleQuery.replace("aggregateWord(<attributes>) as <newAttribute>","")






        # assumption: no filters along with having
        # if filter with grouo then filter is having, if filter with aggregate then filter is having
        if "filter" in intents:
            value=entities['filterValue']
            filterWord=entities['filterWord']
            filter={'>':['greater','larger','bigger','higher','above','more'],"<":['smaller','lower','below','less','lesser'],"=":['equal','same'],"between":['between']}
            attribute=entities['filterAttribute']


            for key in filter.keys():
                if filterWord in filter[key]:
                    function=key

            if function != "between":
                filterCondition=[attribute,function,str(value)]
            else:

                filterCondition=[attribute," ",function," ",str(value[0])," and ",str(value[1])]


            if "group" in intents or "aggregate" in intents:
                if "aggregate" in intents:
                    filterCondition[0]=newAttribute
                    sampleQuery=sampleQuery.replace("<havingCondition>",''.join(filterCondition))
                    sampleQuery=sampleQuery.replace(" [<filterCondition>]","")
                else:
                    sampleQuery=sampleQuery.replace("<havingCondition>",''.join(filterCondition))
                    sampleQuery=sampleQuery.replace(" [<filterCondition>]","")
            else:
                sampleQuery=sampleQuery.replace("<filterCondition>",''.join(filterCondition))
                sampleQuery=sampleQuery.replace("having <havingCondition>","")
        else:
            sampleQuery=sampleQuery.replace(" [<filterCondition>]","")
            sampleQuery=sampleQuery.replace("having <havingCondition>","")




        #what to display. this part must be improved using dependency parsing. Are they asking for Temperature or romm number values?
        # Also cannot ask to display an aggregate and a non aggregatea at the same time

        res = nlp.annotate(simple,properties={'annotators': 'depparse','outputFormat': 'json', 'timeout': 1000,})
        for s in res['sentences']:
            ED= s['enhancedDependencies']
        found=False
        toDisplay=[]
        conj=''
        for ed in ED:
            if ed['dep'] =="ROOT":
                root=ed['dependentGloss']
            if ed['dep'] == "conj:and" and ed['governorGloss']==root:
                conj=ed['dependentGloss']
            if ed['dep']=='nsubj':

                if ed['dependentGloss'] not in toDisplay and ed['dependentGloss'] in simpleAttributes.keys() and (ed['governorGloss']==root or ed['governorGloss']==conj):
                    found=True
                    toDisplay.append(simpleAttributes[ed['dependentGloss']])

        if not found:
            for ed in ED:
                if ed['dep'] =="ROOT":
                    root=ed['dependentGloss']
                if ed['dep'] == "conj:and" and ed['governorGloss']==root:
                    conj=ed['dependentGloss']
                if ed['dep']=='dobj':

                    if ed['dependentGloss'] not in toDisplay and ed['dependentGloss'] in simpleAttributes.keys() and (ed['governorGloss']==root or ed['governorGloss']==conj):
                        toDisplay.append(simpleAttributes[ed['dependentGloss']])


        if 'aggregate' in intents:
            if aggregateAttribute in toDisplay:
                toDisplay.remove(aggregateAttribute)
            if len(toDisplay)>0:
                sampleQuery=sampleQuery.replace(aggregateExpression,aggregateExpression+",")
        if len(toDisplay)>=1:
            toDisplay=', '.join(toDisplay)
            sampleQuery=sampleQuery.replace("<attributeNames>",toDisplay)
        else:
            if 'aggregate' in intents:
                sampleQuery=sampleQuery.replace("<attributeNames>","")
            else:
                sampleQuery=sampleQuery.replace("<attributeNames>"," *")



        sampleQuery=sampleQuery.split()
        sampleQuery=' '.join(sampleQuery)
        return sampleQuery

