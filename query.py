from QueryProcessing import QueryProcessor
QP=QueryProcessor()
class QueryGenerator:
    def generateQuery(self,NLQuery,intents):
        sampleQuery="from <inputStreamName>[<filterCondition>]#window.<window name>(<parameters>)select <attributeNames>"
        if "window" in intents:
            windowType=QP.getWindowType(NLQuery)
            sampleQuery.replace("<window name>",windowType)
        if "group" in intents:
            C=2
        if "filter" in intents:
            filterCondition=QP.getFilterCondition(NLQuery)
            sampleQuery.replace("<filterCondition>",filterCondition)


        return sampleQuery

