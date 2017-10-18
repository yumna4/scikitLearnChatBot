from pycorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://localhost:9000')
import os

import os

os.chdir("stanford-corenlp-full-2017-06-09")
os.system("java -mx5g -cp \"*\" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 10000")


# cd stanford-corenlp-full-2017-06-09
# java -mx5g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 10000
#
def extractEntity(sentence):

    neededEntities=[]
    res = nlp.annotate(sentence,properties={'annotators': 'depparse','outputFormat': 'json', 'timeout': 1000,})

    for s in res['sentences']:
        ED= s['enhancedDependencies']
    # print ED

    for ed in ED:
        print "type: %s words:'%s', %s : %d , %d" % (ed['dep'], ed['governorGloss'], ed['dependentGloss'],ed['governor'],ed['dependent'])
    print ""


extractEntity('display the roomNo and temperature of rooms having temperature between 99 and 100')
extractEntity("Show the device ID and the average temperature per room for the last 10 minutes")
extractEntity('group the temperature stream by device ID and display all the temperatures of each device ID')
extractEntity('display all the expired events in the past 1 minute from the temperature stream')
extractEntity('let me know if the temperature values are lesser than 40 in server rooms')
extractEntity('For every group of device IDs in the temperature stream display the device ID and maximum temperature for events in the past 10 seconds')
extractEntity('Within a 10 minutes window, calculate the average Temperature per device and display the  event details if the average temperature is less than 45')
extractEntity('display the roomNo and temperature of rooms having temperature between 99 and 100')
extractEntity('display the roomNo and temperature of rooms having temperature between 99 and 100')