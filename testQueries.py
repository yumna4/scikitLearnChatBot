class TestQueries:
    def getQueries(self):

        queries=["Per office area calculate the average temperature over the last 10 minutes",
                 "Give me the average temperatures above 30 of rooms details that arrived in past 10 minutes",
                 "Show the sum of temperatures in the past 1 minute",
                 "display the roomNo and temperature of rooms having temperature between 99 and 100",
                 "Show the device ID and the average temperature per room for the last 10 minutes",
                 "Within a 10 minutes window, calculate the average Temperature per sensor and display the  event details if the average temperature is less than 45",

                 "Filtering all server rooms having temperature greater than 40 degrees",
                 "get the average temperature for each room within the 10 minutes window",
                 "for all the events in the past 10 minutes display the average temperatures which are bigger than 30 along with their roomNo and device ID and group all of this by the roomNo",
                 "For every group of device IDs in the temperature stream display the device ID and maximum temperature for events in the past 10 seconds",
                 "Show the temperatures below 100 degrees",
                 "show all the details most recent 10 events",

                 "Show the temperatures higher than 6 degrees",
                 "show the average sum of temperature values in the last 10 minutes",
                 "Per sensor, calculate the maximum temperature over last 10 temperature events each sensor has emitted",
                 "for every sensor, calculate the lowest temperature each sensor has emitted in the past 10 minutes,",
                 "let me know if the temperature values are lesser than 40 in server rooms",
                 "Show the server rooms which have a temperature that is higher than 20 degrees from the temperature stream",


                 "display all the expired events in the past 1 minute from the temperature stream",
                 "average temperature in the most recent 10 events",
                 "let me know the temperature each sensor has emitted in a group of sensors",
                 "group the temperature stream by device ID and display all the temperatures of each device ID",
                 "for past 10 events in each temperature group for a device ID get the, device ID maximum temperature",
                 "lowest temperature in the last 4 events"]
        return queries

    def getValues(self):
        # old version
        # answers=[-1,1, -1 ,1 ,-1,1,1,-1,1,-1,1,-1,1,-1,-1,-1 ,1,1,-1,-1,-1,-1,-1,-1        ,1,1, 1 ,-1 ,1 ,1 ,-1 ,1,1,1,-1 ,-1,-1 ,1,1,1,-1,-1 ,-1,1,-1,-1,1,-1              ,1,1,1,-1,1,1,    -1,1,1 ,1 ,-1 ,1,     -1,1,1,1 ,-1,-1,      1,1,-1,-1,1,1          ,1,-1,-1,-1,1,1,-1,1 ,1,1,-1,-1,-1,-1,1,1 ,1 ,-1,-1,-1,-1,1,1,-1                          ]

        answers=[-1,1,1,1,   1,1,1,-1,   -1,1,1,-1,   1,-1,-1,-1,        -1,1,1,1,      1,1,1,1,        1,-1,-1,-1,     -1,1,1,1,     1,1,1,1,     -1,1,1,1,      1,-1,-1,-1,     -1,-1,1,-1,
                 1,-1,-1,-1,     -1,1,1,-1,   -1,1,1,1,    -1,1,1,1,    1,-1,-1,1,   1,-1,-1,-1,     -1,-1,1,-1,     -1,1,1,-1,    -1,-1,-1,1,    -1,-1,-1,1,     -1,1,1,1,      -1,-1,1,-1   ]

        # print "filter accuracy"
        # print accuracy_score([-1,1, -1 ,1 ,-1,1,1,-1,1,-1,1,-1,1,-1,-1,-1 ,1,1,-1,-1,-1,-1,-1,-1],id.fval)
        # print "aggregate accuracy"
        # print accuracy_score([1,1, 1 ,-1 ,1 ,1 ,-1 ,1,1,1,-1 ,-1,-1 ,1,1,1,-1,-1 ,-1,1,-1,-1,1,-1 ],id.aval)
        # print "window accuracy"
        # print accuracy_score([1,1,1,-1,1,1,  -1,1,1 ,1 ,-1 ,1,   -1,1,1,1 ,-1,-1,   1,1,-1,-1,1,1 ],id.wval)
        # print "group accuracy"
        # print accuracy_score([1,-1,-1,-1,1,1,-1,1 ,1,1,-1,-1,-1,-1,1,1 ,1 ,-1,-1,-1,-1,1,1,-1 ],id.gval)
        return answers