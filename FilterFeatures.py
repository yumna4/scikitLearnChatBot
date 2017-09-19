import nltk

class FilterModel:
    documents=[]
    def getFilterFeatures(self,NLQuery):


        grammar = r"""FUNCTION:{(<JJ><IN><CD>)   |(<JJR><IN><CD>)   |     (<IN><CD><CC><CD>)     |(<IN><CD>)   |     (<JJ><TO><CD>)     |     (<VBP><TO><CD>)}"""
        cp = nltk.RegexpParser(grammar)


        # self.documents=["Delay all events in a stream by 1 minute","average temperature of 10 minute window","alert if temperature increasing rate is greater than 5 per 10 minutes","Emit snapshot of the events in time window of 5 seconds every one second","Get the temperature difference between two regulator events","Alert if temperature of a room increases by 5 degrees within 10 minutes","if the temperature of a room increases by 5 degrees within a 10 minute time gap display a message","tell me if temperature of a room is raised by 5 degrees within 10 minutes","Alert if there is more than 1 degree increase in temperature between two consecutive temperature events","If the temperature of a room increases by 1 degree in the next immediate consecutive event then display that event","tell me if the temperature is increased by one"]

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


        if filter:
            fil1=1
        else:
            fil1=0

        value=[int(s) for s in NLQuery if s.isdigit()]

        if value:
            fil2=1
        else:
            fil2=0
        # print [fil1,fil2]
        return [fil1,fil2]


