from QueryProcessing import QueryProcessor
# from pattern.en import referenced
import nltk

QP=QueryProcessor()

class QueryGenerator:
    def generateQuery(self,NLQuery,intents,stream,attributes):

        sampleQuery="from <inputStreamName>[<filterCondition>]#window.<window name>(<windowParameters>)select <attributeNames> group by <groupAttribute> having <havingCondition>"
        sampleQuery=sampleQuery.replace("<inputStreamName>",stream)


        intent=nltk.word_tokenize(NLQuery)
        sentence =nltk.pos_tag(intent)

        for i in sentence:

            if i[1]=="NN" and i[0] in attributes:
                attributeNames=i[0]
                sampleQuery=sampleQuery.replace("<attributeNames>",attributeNames)
                break




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
            sampleQuery=sampleQuery.replace("group by <groupAttribute>","")


        if "filter" in intents:

            filterCondition=QP.getFilterCondition(NLQuery,attributes)
            sampleQuery=sampleQuery.replace("<filterCondition>",filterCondition)
        else:

            sampleQuery=sampleQuery.replace("[<filterCondition>]","")


        if "having" in intents:
            havingCondition=QP.getFilterCondition(NLQuery,attributes)
            sampleQuery=sampleQuery.replace("<havingCondition>",havingCondition)
        else:
            sampleQuery=sampleQuery.replace("having <havingCondition>","")

        print sampleQuery
        return sampleQuery


# q=QueryGenerator()
# q.generateQuery("Calculate the maximum temperature over last 10 temperature events display if it's greater than 40",["filter","window","aggregate"],"TempStream",["roomNo", "deviceID","temperature","humidity"])
# q.generateQuery("Per sensor, calculate the maximum temperature over last 10 minutes and display if it's greater than 40",["having","window","group","aggregate"],"TempStream",["roomNo", "deviceID","temperature","humidity"])
# q.generateQuery("give me every 10th temperature of each device",["group"],"TempStream",["roomNo", "deviceID","temperature","humidity"])
# q.generateQuery("for each device, give me every 10th temperature",["group"],"TempStream",["roomNo", "deviceID","temperature","humidity"])