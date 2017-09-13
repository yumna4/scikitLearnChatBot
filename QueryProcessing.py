import re
import nltk
import pickle
from FilterFinder import FilterFinder

class QueryProcessor:


    def getWindowType(self,NLQuery):
        if re.findall('second |minut| hour |day| week| month |year',NLQuery):
            windowType="time"
        else :
            windowType="length"
        return windowType


    def getFilterCondition(self,NLQuery,attributes):
        ff=FilterFinder()

        model=pickle.load(open('findfilter_model.sav', 'rb'))
        NLQuery=ff.prepare(NLQuery)
        function=model.predict(NLQuery)
        index=int(function)
        filterTypes=[">","<","=","between"]
        function=filterTypes[index-1]

        print function





        attribute=""

        value=""









qp=QueryProcessor()
qp.getFilterCondition("display the and temperature of rooms between 99 and 100",["temperature, room no"])