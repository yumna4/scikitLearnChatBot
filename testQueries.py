class TestQueries:
    def getQueries(self):

        queries=["Per office area calculate the average temperature over the last 10 minutes",
                 "Give me the average temperatures above 30 of rooms details that arrived in past 10 minutes",
                 "Show the sum of temperatures in the past 1 minute",
                 "display the roomNo and temperature of rooms having temperature between 99 and 100",
                 "Show the device ID and the average temperature per room for the last 10 minutes",
                 "Within a 10 minutes window, calculate the average Temperature per device and display the  event details if the average temperature is less than 45",

                 "Filtering all server rooms having temperature greater than 40 degrees",
                 "get the average temperature for each room within the 10 minutes window",
                 "for all the events in the past 10 minutes display the average temperatures which are bigger than 30 along with their roomNo and device ID and group all of this by the roomNo",
                 "For every group of device IDs in the temperature stream display the device ID and maximum temperature for events in the past 10 seconds",
                 "Show the temperatures below 100 degrees",
                 "show all the details most recent 10 events",

                 "Show the temperatures higher than 6 degrees",
                 "show the average sum of temperature values in the last 10 minutes",
                 "Per device, calculate the maximum temperature over last 10 temperature events each device has emitted",
                 "for every device, calculate the lowest temperature each device has emitted in the past 10 minutes,",
                 "let me know if the temperature values are lesser than 40 in server rooms",
                 "Show the server rooms which have a temperature that is higher than 20 degrees from the temperature stream",


                 "display all the expired events in the past 1 minute from the temperature stream",
                 "average temperature in the most recent 10 events",
                 "let me know the temperature each device has emitted in a group of devices",
                 "group the temperature stream by device ID and display all the temperatures",
                 "for past 10 events in each temperature group for a device ID get the, device ID maximum temperature",
                 "lowest temperature in the last 4 events"]
        return queries

    def getValues(self):
        # old version
        # answers=[-1,1, -1 ,1 ,-1,1,1,-1,1,-1,1,-1,1,-1,-1,-1 ,1,1,-1,-1,-1,-1,-1,-1        ,1,1, 1 ,-1 ,1 ,1 ,-1 ,1,1,1,-1 ,-1,-1 ,1,1,1,-1,-1 ,-1,1,-1,-1,1,-1              ,1,1,1,-1,1,1,    -1,1,1 ,1 ,-1 ,1,     -1,1,1,1 ,-1,-1,      1,1,-1,-1,1,1          ,1,-1,-1,-1,1,1,-1,1 ,1,1,-1,-1,-1,-1,1,1 ,1 ,-1,-1,-1,-1,1,1,-1                          ]

        answers=[-1,1,1,1,   1,1,1,-1,   -1,1,1,-1,   1,-1,-1,-1,        -1,1,1,1,      1,1,1,1,        1,-1,-1,-1,     -1,1,1,1,     1,1,1,1,     -1,1,1,1,      1,-1,-1,-1,     -1,-1,1,-1,
                 1,-1,-1,-1,     -1,1,1,-1,   -1,1,1,1,    -1,1,1,1,    1,-1,-1,-1,   1,-1,-1,-1,     -1,-1,1,-1,     -1,1,1,-1,    -1,-1,-1,1,    -1,-1,-1,1,     -1,1,1,1,      -1,1,1,-1   ]

        # print "filter accuracy"
        # print accuracy_score([-1,1, -1 ,1 ,-1,1,1,-1,1,-1,1,-1,1,-1,-1,-1 ,1,1,-1,-1,-1,-1,-1,-1],id.fval)
        # print "aggregate accuracy"
        # print accuracy_score([1,1, 1 ,-1 ,1 ,1 ,-1 ,1,1,1,-1 ,-1,-1 ,1,1,1,-1,-1 ,-1,1,-1,-1,1,-1 ],id.aval)
        # print "window accuracy"
        # print accuracy_score([1,1,1,-1,1,1,  -1,1,1 ,1 ,-1 ,1,   -1,1,1,1 ,-1,-1,   1,1,-1,-1,1,1 ],id.wval)
        # print "group accuracy"
        # print accuracy_score([1,-1,-1,-1,1,1,-1,1 ,1,1,-1,-1,-1,-1,1,1 ,-1 ,-1,-1,-1,-1,1,1,-1 ],id.gval)
        return answers

    def getSiddhiQueries(self):
        queries=["from TempStream#window.time(10 min) select avg(Temperature) as avgTemperature group by office",
                 "from TempStream#window.time(10 min) select avg(Temperature) as avgTemperature having avgTemperature>30",
                 "from TempStream#window.time(1 min) select sum(Temperature) as sumTemperature",
                 "from TempStream [Temperature between 99 and 100] select RoomNo, Temperature",
                 "from TempStream#window.time(10 min) select avg(Temperature) as avgTemperature, DeviceID group by roomNo",
                 "from TempStream#window.time(10 min) select avg(Temperature) as avgTemperature group by DeviceID having avgTemperature<45",

                 "from TempStream [Temperature>40] select RoomNo",
                 "from TempStream#window.time(10 min) select avg(Temperature) as avgTemperature group by RoomNo",
                 "from TempStream#window.time(10 min) select avg(Temperature) as avgTemperature group by RoomNo having avgTemperature>30",
                 "from TempStream#window.time(10 sec) select max(Temperature) as maxTemperature, DeviceID group by DeviceID",
                 "from TempStream [Temperature<100] select Temperature",
                 "from TempStream#window.length(10) select *",
                 
                 "from TempStream [Temperature>6] select Temperature",
                 "from TempStream#window.time(10 min) select sum(Temperature) as sumTemperature",
                 "from TempStream#window.length(10) select max(Temperature) as maxTemperature group by DeviceID",
                 "from TempStream#window.length(10) select min(Temperature) as minTemperature group by DeviceID",
                 "from TempStream [Temperature<40] select RoomNo",
                 "from TempStream [Temperature>20] select RoomNo",



                 "from TempStream#window.time(1 min) select expired events",
                 "from TempStream#window.length(10) select avg(Temperature) as avgTemperature",
                 "from TempStream select Temperature group by DeviceID",
                 "from TempStream select Temperature group by DeviceID",
                 "from TempStream#window.length(10) select max(Temperature) as maxTemperature group by DeviceID",
                 "from TempStream#window.length(4) select min(Temperature) as minTemperature"]
        return queries