#this file takes input from user and shows the chatBot's response
from entity import extractEntity
from entity import updateQuery
from entity import getExtractedEntities
from query import generateQuery
from IntentDetection import IntentDetector

class Main:

    intentDetector=IntentDetector()
    nLQuery=raw_input("User>") #input given by user
    while len(nLQuery)>0:
        intent = intentDetector.detectIntent(nLQuery)
        print "Query is classified as a: %s"%(intent)

        # neededEntities=extractEntity(res,intent)
        # if neededEntities is not None:
        #     for entity in neededEntities:
        #         print entity
        #         res=raw_input("User>")
        #         updateQuery(entity,res)
        # entities=getExtractedEntities()
        # print generateQuery(intent,entities)
        nLQuery=raw_input("User>")


