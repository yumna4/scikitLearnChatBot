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
    print sentence
    neededEntities=[]
    res = nlp.annotate(sentence,properties={'annotators': 'depparse','outputFormat': 'json', 'timeout': 1000,})

    for s in res['sentences']:
        ED= s['enhancedDependencies']
    # print ED
    toDisplay=[]
    for ed in ED:
        if ed['dep']=='dobj' :
            toDisplay.append(ed['dependentGloss'])

        print "type: %s words:'%s', %s : %d , %d" % (ed['dep'], ed['governorGloss'], ed['dependentGloss'],ed['governor'],ed['dependent'])
    print ""

#
extractEntity("show the roomno having temperature less than 6")
extractEntity("what are the temperatures smaller than 45")
# # extractEntity('group the temperature stream by device ID and display all the temperatures of each device ID')
# # extractEntity('display all the expired events in the past 1 minute from the temperature stream')
# # extractEntity('let me know if the temperature values are lesser than 40 in server rooms')
# # extractEntity('For every group of device IDs in the temperature stream display the device ID and maximum temperature for events in the past 10 seconds')
# # extractEntity('Within a 10 minutes window, calculate the average Temperature per device and display the  event details if the average temperature is less than 45')
# # extractEntity('display the roomNo and temperature of rooms having temperature between 99 and 100')
# # extractEntity('display the roomNo and temperature of rooms having temperature between 99 and 100')
# #
# # extractEntity("show the average sum of temperatures in the last 10 minutes")
# # extractEntity("for past 10 events in each temperature group for a deviceID get the deviceID and maximum temperature")
# # extractEntity("Show the deviceID and the average temperature per room for the last 10 minutes")
# # extractEntity("Within a 10 minutes window, calculate the average Temperature per device and display the  event details if the average temperature is less than 45")
# # extractEntity("get the average temperature for each room within the 10 minutes window")
# # extractEntity("for all the events in the past 10 minutes display the average TUCKSHOP WIZ FIXES MEDICINAL BEVERAGEtemperatures which are bigger than 30 along with their roomNo and deviceID and group all of this by the roomNo")
# # extractEntity("For every group of deviceIDs in the temperature stream display the deviceID and maximum temperature for events in the past 10 seconds")
# # extractEntity("Per device, calculate the maximum temperature over last 10 temperature events each device has emitted")
# # extractEntity("for every device, calculate the lowest temperature each device has emitted in the past 10 minutes,")
# # extractEntity("tell me the temperature each device has emitted in a group of devices")
# # extractEntity("group the temperature stream by deviceID and display all the temperatures")
# # extractEntity("for past 10 events in each temperature group for a deviceID, get the deviceID and maximum temperature")
print "Enter String"
strings=raw_input().lower()
while strings:
    alphabet="abcdefghijklmnopqrstuvwxyz"
    alphabet=list(alphabet)
    absent=[a for a in alphabet if a not in strings]
    print absent
    print "Enter string"
    strings=raw_input().lower()
