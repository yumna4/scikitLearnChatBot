import re
import nltk
import pickle
from FilterConditionBuilder import FilterFinder
from nltk.stem.porter import PorterStemmer
stemmer=PorterStemmer()


class QueryProcessor:


    def getWindowType(self,NLQuery):
        a= re.search('millisecond|second |minut| hour |day| week| month |year',NLQuery)
        if a:
            windowType="time"

        else :
            windowType="length"


        intent=nltk.word_tokenize(NLQuery)
        sentence =nltk.pos_tag(intent)

        grammar = r"""FUNCTION:{<JJ><CD>}"""
        cp = nltk.RegexpParser(grammar)
        result = cp.parse(sentence)
        tagsOfQuery=list(result)

        for node in range(len(tagsOfQuery)):
            try:
                if result[node].label()=="FUNCTION":
                    value=result[node].leaves()[1][0]
            except:
                continue


        return value,windowType


    def getFilterCondition(self,NLQuery,attributes):
        ff=FilterFinder()

        model=pickle.load(open('findfilter_model.sav', 'rb'))
        prepared=ff.prepare(NLQuery)
        function=model.predict([prepared])
        index=int(function)
        filterTypes=[">","<","="," between "]
        function=filterTypes[index-1]

        for word in NLQuery.split():

            if word in attributes:
                attribute=word




        value=ff.getValues()

        if function is not "between":
            filterCondition=attribute+function+str(value[0])
        else:
            filterCondition=attribute+function+str(value[0])+" and "+str(value[1])

        return filterCondition


    def getGroupAttribute(self,NLQuery,attributes):

        grammar = r"""FUNCTION:{(<IN><DT><NN>)|(<NNP><NN>)}"""


        cp = nltk.RegexpParser(grammar)
        intent=nltk.word_tokenize(NLQuery)
        sentence =nltk.pos_tag(intent)
        result = cp.parse(sentence)
        tagsOfQuery=list(result)

        filter=[]

        for node in range(len(tagsOfQuery)):
            try:
                if result[node].label()=="FUNCTION":
                    filter.extend(result[node])
            except:
                continue

        attribute=filter[-1][0]

        return attribute







qp=QueryProcessor()
qp.getFilterCondition("display the rooms with temperature of rooms between 99 and 100",["temperature", "roomNo"])
qp.getFilterCondition("Show the rooms with roomNo above 110",["temperature", "roomNo"])
qp.getFilterCondition("Show the rooms with temperature less than 25",["temperature", "roomNo"])
qp.getFilterCondition("Show the rooms with roomNo equal to 110",["temperature", "roomNo"])
#
# qp.getGroupAttribute("Emit the last temperature event per sensor for every 10 events",["temperature", "roomNo","deviceID"])
# qp.getGroupAttribute("give me every 10th temperature of each device",["temperature", "roomNo","deviceID"])
# qp.getGroupAttribute("group the temperature stream by device ID and display all the temperatures of every 10th event of each device ID",["temperature", "roomNo","deviceID"])
# qp.getGroupAttribute("get the temp of every 10th event of each device ID from temperature stream",["temperature", "roomNo","deviceID"])

