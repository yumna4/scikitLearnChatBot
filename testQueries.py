class TestQueries:
    def getQueries(self):

        queries=["Per room, calculate the average temperature over the last 10 minutes",
                 "Give me the average temperatures that are above 30 of rooms details that arrived in past 10 minutes",
                 "Show the sum of temperatures in the past 1 minute",
                 "display the roomNo and temperature of rooms having temperature between 99 and 100",
                 "Show the deviceID and the average temperature per room for the last 10 minutes",
                 "Within a 10 minutes window, calculate the average Temperature per device and display the  event details if the average temperature is less than 45",

                 "show all the rooms having a temperature greater than 40 degrees",
                 "get the average temperature for each room within the 10 minutes window",
                 "for all the events in the past 10 minutes display the average temperatures which are bigger than 30 along with their roomNo and deviceID and group all of this by the roomNo",
                 "For every group of deviceIDs in the temperature stream display the deviceID and maximum temperature for events in the past 10 seconds",
                 "Show the temperatures below 100 degrees",
                 "show all the details most recent 10 events",

                 "Show the temperatures higher than 6 degrees",
                 "show the average sum of temperatures in the last 10 minutes",
                 "Per device, calculate the maximum temperature over last 10 temperature events each device has emitted",
                 "for every device, calculate the lowest temperature each device has emitted in the past 10 minutes,",
                 "tell me the rooms having a temperature lesser than 40",
                 "Show the rooms which have temperature higher than 20 degrees",


                 "display all the events in the past 1 minute from the temperature stream",
                 "average temperature in the most recent 10 events",
                 "tell me the temperature each device has emitted in a group of devices",
                 "group the temperature stream by deviceID and display the temperatures",
                 "for past 10 events in each temperature group for a deviceID, get the deviceID and maximum temperature",
                 "lowest temperature in the last 4 events"]
        return queries

    def getValues(self):

        # answers=[-1,1,1,1,   1,1,1,-1,   -1,1,1,-1,   1,-1,-1,-1,        -1,1,1,1,      1,1,1,1,        1,-1,-1,-1,     -1,1,1,1,     1,1,1,1,     -1,1,1,1,      1,-1,-1,-1,     -1,-1,1,-1,
        #          1,-1,-1,-1,     -1,1,1,-1,   -1,1,1,1,    -1,1,1,1,    1,-1,-1,-1,   1,-1,-1,-1,     -1,-1,1,-1,     -1,1,1,-1,    -1,-1,-1,1,    -1,-1,-1,1,     -1,1,1,1,      -1,1,1,-1   ]
        answers=[[-1,1,1,1],   [1,1,1,-1],   [-1,1,1,-1],  [ 1,-1,-1,-1],        [-1,1,1,1],      [1,1,1,1],        [1,-1,-1,-1],     [-1,1,1,1],     [1,1,1,1],     [-1,1,1,1],      [1,-1,-1,-1],     [-1,-1,1,-1],
                 [1,-1,-1,-1],     [-1,1,1,-1],   [-1,1,1,1],    [-1,1,1,1],    [1,-1,-1,-1],   [1,-1,-1,-1],     [-1,-1,1,-1],     [-1,1,1,-1],    [-1,-1,-1,1],    [-1,-1,-1,1],     [-1,1,1,1],      [-1,1,1,-1]   ]


        return answers
    def getIndividuals(self):
        # filter,aval,wval,gval
        return ([-1,1, -1 ,1 ,-1,1,1,-1,1,-1,1,-1,1,-1,-1,-1 ,1,1,-1,-1,-1,-1,-1,-1],[1,1, 1 ,-1 ,1 ,1 ,-1 ,1,1,1,-1 ,-1,-1 ,1,1,1,-1,-1 ,-1,1,-1,-1,1,-1 ], [1,1,1,-1,1,1,  -1,1,1 ,1 ,-1 ,1,   -1,1,1,1 ,-1,-1,   1,1,-1,-1,1,1 ], [1,-1,-1,-1,1,1,-1,1 ,1,1,-1,-1,-1,-1,1,1 ,-1 ,-1,-1,-1,-1,1,1,-1 ])

    def getSiddhiQueries(self):
        queries=["from TempStream#window.time(10 min) select avg(Temperature) as avgTemperature group by RoomNo",
                 "from TempStream#window.time(10 min) select avg(Temperature) as avgTemperature having avgTemperature>30",
                 "from TempStream#window.time(1 min) select sum(Temperature) as sumTemperature",
                 "from TempStream [Temperature between 99 and 100] select RoomNo, Temperature",
                 "from TempStream#window.time(10 min) select avg(Temperature) as avgTemperature, DeviceID group by RoomNo",
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



                 "from TempStream#window.time(1 min) select *",
                 "from TempStream#window.length(10) select avg(Temperature) as avgTemperature",
                 "from TempStream select Temperature group by DeviceID",
                 "from TempStream select Temperature group by DeviceID",
                 "from TempStream#window.length(10) select max(Temperature) as maxTemperature, DeviceID group by DeviceID",
                 "from TempStream#window.length(4) select min(Temperature) as minTemperature"]
        return queries