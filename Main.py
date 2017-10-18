from IntentDetection import IntentDetector
intentDetector=IntentDetector()
from query import QueryGenerator
Q=QueryGenerator()
from testQueries import TestQueries
tq=TestQueries()
from sklearn.metrics import accuracy_score



class Main:
    # isTest=raw_input("Is this a Test? (Y/n)>")
    isTest="Y"
    if isTest=="Y":
        streamName="TempStream"
        attributes=['Temperature','RoomNo','DeviceID']
        streamWords=["temperature","server","room","id","device","sensor","room number","humidity","temp","temperatures","degree","temps","ids","rooms","numbers","degrees","server","office","area"]
        queries=tq.getQueries()
        # predictions=[]
        # for query in queries:
        #     values,intents = intentDetector.detectIntent(query,streamWords)
        #     for value in values:
        #         predictions.append(value)
        actual=tq.getValues()
        actualqueries=tq.getSiddhiQueries()
        i=0
        j=["filter",'aggregate','window','group']
        siddhiQueries=[]
        for query in queries:
            val=actual[4*i:4*i+4]
            intents=[j[k] for k in range (4) if val[k]==1]
            print query
            # print intents
            siddhiQuery=Q.generateQuery(query,intents,streamName,attributes)
            siddhiQueries.append(siddhiQuery)
            if siddhiQuery== actualqueries[i]:
                print "OK"
            else:
                print siddhiQuery
                print actualqueries[i]
            print " "
            i+=1
            # print accuracy_score(predictions,actual)

        print "accuracy of final query",accuracy_score(siddhiQueries,actualqueries)




    if isTest=="n":

        streamName=raw_input("Enter Stream Name>")


        numberOfAttributes=raw_input("Enter number of attributes>")
        attributes=[]
        for i in range (int(numberOfAttributes)):
            attribute=raw_input("Enter attribute>")
            attributes.append(attribute)


        numberOfWords=raw_input("Enter number of stream relevant words>")
        words=[]
        for i in range (int(numberOfWords)):
            word=raw_input("Enter word>")
            words.append(word)




        nLQuery=raw_input("User>") #input given by user
        while len(nLQuery)>0:
            values,intents = intentDetector.detectIntent(nLQuery,words)
            print "Query is classified as a: %s"%(intents)
            Q.generateQuery(nLQuery,intents,streamName,attributes)
            nLQuery=raw_input("User>")









