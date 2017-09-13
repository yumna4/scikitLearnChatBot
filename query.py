from QueryProcessing import QueryProcessor

QP=QueryProcessor()

class QueryGenerator:
    def generateQuery(self,NLQuery,intents,stream,attributes):

        sampleQuery="from <inputStreamName>[<filterCondition>]#window.<window name>(<parameters>)select <attributeNames> group by <attributeNames> having <havingCondition>"
        sampleQuery.replace("<inputStreamName>",stream)


        if "window" in intents:
            windowType=QP.getWindowType(NLQuery)
            sampleQuery.replace("<window name>",windowType)
        else:
            sampleQuery.replace("#window.<window name>(<parameters>)","")


        if "group" in intents:
            s=2
        else:
            sampleQuery.replace("group by <attributeNames>","")


        if "filter" in intents:
            filterCondition=QP.getFilterCondition(NLQuery,attributes)
            sampleQuery.replace("<filterCondition>",filterCondition)
        else:
            sampleQuery.replace("[<filterCondition>]","")


        if "having" in intents:
            havingCondition=QP.getHavingCondition(NLQuery,attributes)
            sampleQuery.replace("<havingCondition>",havingCondition)
        else:
            sampleQuery.replace("having <havingCondition>","")


        return sampleQuery


q=QueryGenerator()
q.generateQuery("Calculate the maximum temperature over last 10 temperature events display if it's greater than 40",["filter","window","aggregate"],"TempStream",["roomNo", "DeviceID","Temperature","Humidity"])
q.generateQuery("Per sensor, calculate the maximum temperature over last 10 temperature events each sensor has emitted and display if it's greater than 40",["having","window","group","aggregate"],"TempStream",["roomNo", "DeviceID","Temperature","Humidity"])