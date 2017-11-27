import os
os.system("java -mx5g -cp \"*\" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 10000")

import time
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
        startTime=time.time()
        streamName="TempStream"
        Attributes=['Temperature','RoomNo','DeviceID']
        streamWords=["temperature","server","room","id","deviceid","device","sensor","roomNo","roomnos","room number","devices","humidity","temp","temperatures","degree","temps","ids","rooms","numbers","degrees","server","office","area"]
        queries=tq.getQueries()
        actual=tq.getValues()
        predictions=[]
        predictions1=[]
        fval=[]
        gval=[]
        aval=[]
        wval=[]
        i=0
        for query in queries:
            # print ""
            # print query
            # intentDetector.detectIntent(query,streamWords,Attributes)
            values,intents = intentDetector.detectIntent(query,streamWords,Attributes)
            #
            # print values
            # print intents
            # for value in values:
            #     predictions.append(value)
            predictions1.append(values)
            fval.append(values[0])
            aval.append(values[1])
            wval.append(values[2])
            gval.append(values[3])
            i+=1
        individuals=tq.getIndividuals()
        # print individuals[0]
        actual=tq.getValues()
        # print (len(actual))
        count=0
        print (predictions1[0])
        print(actual[0])

        for i in range (24):
            if accuracy_score(predictions1[i],actual[i])==1.0:

                count+=1

        print (count*100/24)
        # print (accuracy_score(predictions,actual))
        # print "filter",accuracy_score(fval,individuals[0])
        # print "aggrigate", accuracy_score(aval,individuals[1])
        # print "window",accuracy_score(wval,individuals[2])
        # print "group",accuracy_score(gval,individuals[3])



        actualqueries=tq.getSiddhiQueries()
        i=0
        j=["filter",'aggregate','window','group']
        siddhiQueries=[]
        # for q in range (24):
        #     query=queries[q]
        #     val=actual[4*i:4*i+4]
        #     intents=[j[k] for k in range (4) if val[k]==1]
        #
        #     siddhiQuery=Q.generateQuery(query,intents,streamName,Attributes)
        #
        #     if siddhiQuery!=actualqueries[q]:
        #         print intents
        #         print query
        #         print siddhiQuery
        #         print actualqueries[q]
        #         print ""
        #         print ""
        #     siddhiQueries.append(siddhiQuery)
        #     i+=1
        #
        # print "accuracy of final query",accuracy_score(siddhiQueries,actualqueries)
        print (time.time()-startTime)
    if isTest=="n":

        # streamName=raw_input("Enter Stream Name>")
        #
        #
        # numberOfAttributes=raw_input("Enter number of attributes>")
        # attributes=[]
        # for i in range (int(numberOfAttributes)):
        #
        #     attribute=raw_input("Enter attribute>")
        #     attributes.append(attribute)
        #
        #
        # numberOfWords=raw_input("Enter number of stream relevant words>")
        # words=[]
        # for i in range (int(numberOfWords)):

        #     word=raw_input("Enter word>")
        #     words.append(word)

        streamName="TempStream"
        Attributes=['Temperature','RoomNo','DeviceID','Humidity','BranchID','Rainfall']
        words=["temperature","server","room","id","deviceid","device","sensor","roomNo","roomnos","room number","devices","humidity","temp","temperatures","degree","temps","ids","rooms","numbers","degrees","server","office","area"]





        nLQuery=input("Natural Language Query>") #input given by user
        while len(nLQuery)>0:
            values,intents = intentDetector.detectIntent(nLQuery,words,Attributes)
            # print "Query is classified as a: %s"%(intents)
            # intents=raw_input("intents>")
            siddhiQuery=Q.generateQuery(nLQuery,intents,streamName,Attributes)
            # print siddhiQuery
            nLQuery=input("Natural Language Query>")

# "what is the maximum humidity noted in past hour"
# tell me the branch which is having the most rainfall during last month







