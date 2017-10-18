from QueryProcessing import QueryProcessor
# from pattern.en import referenced
import nltk

QP=QueryProcessor()


class QueryGenerator:
    def generateQuery(self,NLQuery,intents,stream,attributes):

        sampleQuery="from <inputStreamName> [<filterCondition>]#window.<window name>(<windowParameters>) select aggregateWord(<attributes>) as <newAttribute> <attributeNames> group by <groupAttribute> having <havingCondition>"
        sampleQuery=sampleQuery.replace("<inputStreamName>",stream)


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
                    # print word
                    # print NLQuery
                    NLQuery=NLQuery.replace(word,attribute,1)
                    # print NLQuery
        words=nltk.word_tokenize(NLQuery)


        for word in words:
            if word in attributes:

                mainAttribute=word #this will be used for aggregate function stuff
                break






        # for i in sentence:
        #
        #     if i[1]=="NN" and i[0] in attributes:
        #         attributeNames=i[0]
        #
        #         break



        if "window" in intents:
            value,windowType=QP.getWindowType(NLQuery)
            sampleQuery=sampleQuery.replace("<window name>",windowType)
            sampleQuery=sampleQuery.replace("<windowParameters>",value)
        else:
            sampleQuery=sampleQuery.replace("#window.<window name>(<windowParameters>)","")


        if "group" in intents:
            attribute=QP.getGroupAttribute(NLQuery,attributes)
            sampleQuery=sampleQuery.replace("<groupAttribute>",attribute)
        else:
            sampleQuery=sampleQuery.replace("group by <groupAttribute> ","")

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
            words=words[index:]
            for word in words:
                if word in attributes:

                    aggregateAttribute=word #this will be used for aggregate function stuff
                    break
            newAttribute=aggregateWord+aggregateAttribute
            aggregateExpression=aggregateWord+"("+aggregateAttribute+")"+" as "+newAttribute
            sampleQuery=sampleQuery.replace("aggregateWord(<attributes>) as <newAttribute>",aggregateExpression)
            sampleQuery=sampleQuery.replace("<attributeNames> ","")
        else:
            sampleQuery=sampleQuery.replace("aggregateWord(<attributes>) as <newAttribute> ","")

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
                sampleQuery=sampleQuery.replace(" having <havingCondition>","")
        else:
            sampleQuery=sampleQuery.replace(" [<filterCondition>]","")
            sampleQuery=sampleQuery.replace(" having <havingCondition>","")


        #what to display. this part must be improved using dependency parsing. Are they asking for Temperature or romm number values?
        # Also cannot ask to display an aggregate and a non aggregatea at the same time
        try:
            if "aggregate" not in intents:
                sampleQuery=sampleQuery.replace("<attributeNames>",mainAttribute)


        except:
            # just a random code
            a=2
        try:
            sampleQuery=sampleQuery.replace("<attributeNames>","*")
        except:
            a=4
        return sampleQuery
#

# q=QueryGenerator()
# q.generateQuery("Calculate the maximum temperature over last 10 temperature events display if it's greater than 40",["filter","window","aggregate"],"TempStream",["roomNo", "deviceID","temperature","humidity"])
# q.generateQuery("Per sensor, calculate the maximum temperature over last 10 minutes and display if it's greater than 40",["having","window","group","aggregate"],"TempStream",["roomNo", "deviceID","temperature","humidity"])
# q.generateQuery("give me every 10th temperature of each device",["group"],"TempStream",["roomNo", "deviceID","temperature","humidity"])
# q.generateQuery("for each device, give me every 10th temperature",["group"],"TempStream",["roomNo", "deviceID","temperature","humidity"])