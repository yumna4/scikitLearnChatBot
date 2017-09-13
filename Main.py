from IntentDetection import IntentDetector
from Training import Trainer

trainer=Trainer()
trainer.createTrainingSet()

class Main:

    intentDetector=IntentDetector()
    nLQuery=raw_input("User>") #input given by user
    while len(nLQuery)>0:
        intent = intentDetector.detectIntent(nLQuery)
        print "Query is classified as a: %s"%(intent)
        nLQuery=raw_input("User>")









