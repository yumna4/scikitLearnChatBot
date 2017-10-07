from QueryProcessing import QueryProcessor
# from pattern.en import referenced
import nltk

QP=QueryProcessor()


class QueryGenerator:
    def generateQuery(self,NLQuery,intents,stream,attributes):

        sampleQuery="from <inputStreamName>[<filterCondition>]#window.<window name>(<windowParameters>)select <attributeNames> group by <groupAttribute> having <havingCondition>"
        sampleQuery=sampleQuery.replace("<inputStreamName>",stream)


        intent=nltk.word_tokenize(NLQuery)
        tags =nltk.pos_tag(intent)

        #REPLACING WITH CORRECT ATTRIBUTE NAMES
        nouns=[]
        for tag in tags:

            if tag[1]=="NN" or tag[1]=="NNS":
                nouns.append(tag[0])
        for word in nouns:
            for attribute in attributes:

                distance=nltk.edit_distance(word,attribute.lower())
                if distance<4:#OR LESS THAN 3
                    NLQuery=NLQuery.replace(word,attribute)

        #what to display. this part must be improved using dependency parsing
        for word in NLQuery.split():
            if word in attributes:
                sampleQuery=sampleQuery.replace("<attributeNames>",word)
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


        # if "group" in intents:
        #     attribute=QP.getGroupAttribute(NLQuery,attributes)
        #     sampleQuery=sampleQuery.replace("<groupAttribute>",attribute)
        # else:
        #     sampleQuery=sampleQuery.replace("group by <groupAttribute>","")

        if "filter" in intents:

            filterCondition=QP.getFilterCondition(NLQuery,attributes)
            sampleQuery=sampleQuery.replace("<filterCondition>",filterCondition)
        else:

            sampleQuery=sampleQuery.replace("[<filterCondition>]","")


        # if "having" in intents:
        #     havingCondition=QP.getFilterCondition(NLQuery,attributes)
        #     sampleQuery=sampleQuery.replace("<havingCondition>",havingCondition)
        # else:
        #     sampleQuery=sampleQuery.replace("having <havingCondition>","")
        #
        print sampleQuery
        # return sampleQuery


# q=QueryGenerator()
# q.generateQuery("Calculate the maximum temperature over last 10 temperature events display if it's greater than 40",["filter","window","aggregate"],"TempStream",["roomNo", "deviceID","temperature","humidity"])
# q.generateQuery("Per sensor, calculate the maximum temperature over last 10 minutes and display if it's greater than 40",["having","window","group","aggregate"],"TempStream",["roomNo", "deviceID","temperature","humidity"])
# q.generateQuery("give me every 10th temperature of each device",["group"],"TempStream",["roomNo", "deviceID","temperature","humidity"])
# q.generateQuery("for each device, give me every 10th temperature",["group"],"TempStream",["roomNo", "deviceID","temperature","humidity"])