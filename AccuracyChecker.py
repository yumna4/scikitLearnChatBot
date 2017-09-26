from IntentDetection import IntentDetector
from sklearn.metrics import accuracy_score



id=IntentDetector()
id.detectIntent("Per office area calculate the average temperature over last 10 minutes")
id.detectIntent("Give me the average temperatures above 30 of room in past 10 minutes")
id.detectIntent("Show the sum of temperature")
id.detectIntent("Delay all events in a stream by 1 minute",)
id.detectIntent("Show the average temperature per room and device ID for the last 10 minutes",)
id.detectIntent( "Within a 10 minutes window, calculate the average Temperature per sensor and display the  event details if the average temperature is less than 45")
id.detectIntent("Filtering all server rooms having temperature greater than 40 degrees")
id.detectIntent("get the average temperature for each room with the 10 minutes window",)
id.detectIntent( "for all the events in the past 10 minutes display the average temperature which are bigger than 30 of all the rooms along with there and device ID grouping all of this by the")
id.detectIntent("For every group of device IDs in the temperature stream display the device ID and maximum temperature for every 10 events",)
id.detectIntent("Show the temperatures below 100 degrees",)
id.detectIntent( "most recent 10 minutes",)

id.detectIntent("Show the temperatures higher than 6 degrees",)
id.detectIntent( "show the average sum of temperature values")
id.detectIntent("Per sensor, calculate the maximum temperature over last 10 temperature events each sensor has emitted")
id.detectIntent("for every sensor, calculate the lowest temperature each sensor has emitted in the past 10 minutes,")
id.detectIntent("let me know if the temperature values are lesser than 40 in server rooms")
id.detectIntent("Show the server rooms which have a temperature that is higher than 20 degrees from the temperature stream",)
id.detectIntent( "display all the expired events in the past 1 minute from the temperature stream",)
id.detectIntent("average temperature")
id.detectIntent( "let me know the temperature over temperature events each sensor has emitted in a group of sensors")
id.detectIntent("group the temperature stream by device ID and display all the temperatures of each device ID",)
id.detectIntent("for every 10 events in each temperature group for a device ID get the, device ID maximum temperature",)
id.detectIntent( "temperature in the last 4 events",)


results=id.fval+id.aval+id.wval+id.gval
print accuracy_score([-1,1, -1 ,-1 ,-1,1,1,-1,1,-1,1,-1,1,-1,-1,-1 ,1,1,-1,-1,-1,-1,-1,-1        ,1,1, 1 ,-1 ,1 ,1 ,-1 ,1,1,1,-1 ,-1,-1 ,1,1,1,-1,-1 ,-1,1,-1,-1,1,-1              ,1,1,-1,1,1,1,-1,1,1 ,-1 ,-1 ,1,-1,-1,1,1 ,-1,-1,1,-1,-1,-1,-1,1          ,1,-1,-1,-1,1,1,-1,1 ,1,1,-1,-1,-1,-1,1,1 ,1 ,-1,-1,-1,-1,1,1,-1                             ],results)
print "filter accuracy"
print accuracy_score([-1,1, -1 ,-1 ,-1,1,1,-1,1,-1,1,-1,1,-1,-1,-1 ,1,1,-1,-1,-1,-1,-1,-1],id.fval)
print "aggregate accuracy"
print accuracy_score([1,1, 1 ,-1 ,1 ,1 ,-1 ,1,1,1,-1 ,-1,-1 ,1,1,1,-1,-1 ,-1,1,-1,-1,1,-1 ],id.aval)
print "window accuracy"
print accuracy_score([1,1, 1 ,-1 ,1 ,1 ,-1 ,1,1,1,-1 ,-1,-1 ,1,1,1,-1,-1 ,-1,1,-1,-1,1,-1 ],id.aval)
print "group accuracy"
print accuracy_score([1,1, 1 ,-1 ,1 ,1 ,-1 ,1,1,1,-1 ,-1,-1 ,1,1,1,-1,-1 ,-1,1,-1,-1,1,-1 ],id.aval)


