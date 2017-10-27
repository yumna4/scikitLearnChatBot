from IntentDetection import IntentDetector
intentDetector=IntentDetector()
from query import QueryGenerator
Q=QueryGenerator()
from testQueries import TestQueries
tq=TestQueries()

import os
os.system("java -mx5g -cp \"*\" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 10000")


class Main:

    # streamName=raw_input("Enter Stream Name>")
    # numberOfAttributes=raw_input("Enter number of attributes>")
    # attributes=[]
    # for i in range (int(numberOfAttributes)):
    #     attribute=raw_input("Enter attribute>")
    #     attributes.append(attribute)
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
        values,intents = intentDetector.detectIntent(nLQuery,words)
        # print "Query is classified as a: %s"%(intents)
        siddhiQuery=Q.generateQuery(nLQuery,intents,streamName,attributes)
        print "Siddhi Query: ",siddhiQuery
        print ""
        nLQuery=raw_input("Natural Language Query>")









