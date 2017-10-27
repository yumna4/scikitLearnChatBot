from QueryProcessing import QueryProcessor
import nltk
QP=QueryProcessor()

# ASSUMPTION: ATTRIBUTE NAMES SHOULD BE ONE WORD AND NO TMULTIPLE WORDS
#assumption: cannot use temperature values. instead just temperatures



class QueryGenerator:
    def generateQuery(self,NLQuery,intents,stream,attributes):

        sampleQuery="from <inputStreamName> [<filterCondition>]#window.<window name>(<windowParameters>) select aggregateWord(<attributes>) as <newAttribute> <attributeNames> group by <groupAttribute> having <havingCondition>"
        sampleQuery=sampleQuery.replace("<inputStreamName>",stream)



        NLQuery=NLQuery.replace(" me "," ")



        words=nltk.word_tokenize(NLQuery)
        tags =nltk.pos_tag(words)


        #REPLACING WITH CORRECT ATTRIBUTE NAMES, example replacing 'temp' in NLQuery with "Temperature. Note: Sensor will not be able to be replaced with device in this method"
        nouns=[]
        for tag in tags:
            if tag[1]=="NN" or tag[1]=="NNS":
                nouns.append(tag[0])
        for word in nouns:
            for attribute in attributes:
                distance=nltk.edit_distance(word,attribute.lower())
                if distance<4:#OR LESS THAN 3
                    NLQuery=NLQuery.replace(word,attribute,1)
        words=nltk.word_tokenize(NLQuery)



        if "window" in intents:
            value,windowType=QP.getWindowType(NLQuery)
            sampleQuery=sampleQuery.replace("<window name>",windowType)
            sampleQuery=sampleQuery.replace("<windowParameters>",value)
        else:
            sampleQuery=sampleQuery.replace("#window.<window name>(<windowParameters>)","")



        if "group" in intents:
            groupAttribute=QP.getGroupAttribute(NLQuery,attributes)
            sampleQuery=sampleQuery.replace("<groupAttribute>",groupAttribute)
        else:
            sampleQuery=sampleQuery.replace("group by <groupAttribute>","")



        # cannot handle when user says coolest room or warmest room
        if "aggregate" in intents:
            for word in words:
                if word in ["maximum","highest","highest","greatest"]:
                    aggregateWord="max"
                    index=words.index(word)
                elif word in ["minimum","lowest","smallest"]:
                    aggregateWord='min'
                    index=words.index(word)
                elif word in ["average"]:
                    aggregateWord="avg"
                    index=words.index(word)
                elif word in ["total","sum","summation"]:
                    aggregateWord="sum"
                    index=words.index(word)
                elif word in ["count"]:
                    aggregateWord="count"
                    index=words.index(word)

            # this part can be improved and simplified via dependency parsing, this may be wrong when like :
            # show roomno when temp is maximum in last 10 minutes
            # remove this when intent detection accuracy is better
            try:
                words=words[index:]
            except:
                fg=0
            for word in words:
                if word in attributes:

                    aggregateAttribute=word #this will be used for aggregate function stuff
                    break
            # remove this when intent detection accuracy is better
            try:
                newAttribute=aggregateWord+aggregateAttribute
                aggregateExpression=aggregateWord+"("+aggregateAttribute+")"+" as "+newAttribute
                sampleQuery=sampleQuery.replace("aggregateWord(<attributes>) as <newAttribute>",aggregateExpression)
            except:
                fg=0
        else:
            sampleQuery=sampleQuery.replace("aggregateWord(<attributes>) as <newAttribute>","")




        # assumption: no filters along with having
        # if filter with grouo then filter is having, if filter with aggregate then filter is having
        if "filter" in intents:
            filterCondition=QP.getFilterCondition(NLQuery,attributes)
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
        from pycorenlp import StanfordCoreNLP
        nlp = StanfordCoreNLP('http://localhost:9000')
        res = nlp.annotate(NLQuery,properties={'annotators': 'depparse','outputFormat': 'json', 'timeout': 1000,})
        for s in res['sentences']:
            ED= s['enhancedDependencies']
        conj=''
        toDisplay=[]
        for ed in ED:
            if ed['dep'] =="ROOT":
                root=ed['dependentGloss']
            if ed['dep'] == "conj:and" and ed['governorGloss']==root:
                conj=ed['dependentGloss']
            elif ed['dep']=='dobj':
                if ed['dependentGloss'] not in toDisplay and ed['dependentGloss'] in attributes:
                    if ed['governorGloss']==root or ed['governorGloss']==conj:
                        toDisplay.append(ed['dependentGloss'])
        if 'aggregate' in intents:
            try:
                if aggregateAttribute in toDisplay:
                    toDisplay.remove(aggregateAttribute)
            except:
                fg=7
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
