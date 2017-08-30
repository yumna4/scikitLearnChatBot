import re

class QueryProcessor:
    def getWindowType(self,NLQuery):
        if re.findall('second |minut| hour |day| week| month |year',NLQuery):
            windowType="time"
        else :
            windowType="length"
        return windowType

    def getFilterCondition(self,NLQUery):




qp=QueryProcessor()
qp.getWindowType("Show the temp and s that came in the last 10 minutes")