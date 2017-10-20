from IntentDetection import IntentDetector
intentDetector=IntentDetector()
from query import QueryGenerator
Q=QueryGenerator()
from testQueries import TestQueries
tq=TestQueries()
from sklearn.metrics import accuracy_score


import os
os.system("java -mx5g -cp \"*\" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 10000")


class Main:
    # isTest=raw_input("Is this a Test? (Y/n)>")
    isTest="n"
    if isTest=="Y":
        streamName="TempStream"
        attributes=['Temperature','RoomNo','DeviceID']
        streamWords=["temperature","server","room","id","device","sensor","room number","humidity","temp","temperatures","degree","temps","ids","rooms","numbers","degrees","server","office","area"]
        queries=tq.getQueries()
        predictions=[]
        fval=[]
        gval=[]
        aval=[]
        wval=[]
        for query in queries:
            values,intents = intentDetector.detectIntent(query,streamWords,attributes)
            for value in values:
                predictions.append(value)
            fval.append(values[0])
            aval.append(values[1])
            wval.append(values[2])
            gval.append(values[3])
        individuals=tq.getIndividuals()
        print individuals[0]
        actual=tq.getValues()
        print accuracy_score(predictions,actual)
        print "filter",accuracy_score(fval,individuals[0])
        print "aggrigate", accuracy_score(aval,individuals[1])
        print "window",accuracy_score(wval,individuals[2])
        print "group",accuracy_score(gval,individuals[3])

        # actualqueries=tq.getSiddhiQueries()
        # i=0
        # j=["filter",'aggregate','window','group']
        # siddhiQueries=[]
        # for q in range (24):
        #     query=queries[q]
        #     val=predictions[4*i:4*i+4]
        #     intents=[j[k] for k in range (4) if val[k]==1]
        #
        #     siddhiQuery=Q.generateQuery(query,intents,streamName,attributes)
        #
        #     siddhiQueries.append(siddhiQuery)
        #     i+=1
        #
        # print "accuracy of final query",accuracy_score(siddhiQueries,actualqueries)
        #



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
        attributes=['Temperature','RoomNo','DeviceID']
        words=["temperature","server","room","id","device","sensor","room number","humidity","temp","temperatures","degree","temps","ids","rooms","numbers","degrees","server","office","area"]





        nLQuery=raw_input("Natural Language Query>") #input given by user
        while len(nLQuery)>0:
            values,intents = intentDetector.detectIntent(nLQuery,words,attributes)
            # print "Query is classified as a: %s"%(intents)
            # intents=raw_input("intents>")
            # print intents

            siddhiQuery=Q.generateQuery(nLQuery,intents,streamName,attributes)
            print "Siddhi Query: ",siddhiQuery


            print ""
            nLQuery=raw_input("Natural Language Query>")









