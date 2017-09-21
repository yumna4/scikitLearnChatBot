import nltk
import re

class GroupModel:
    documents=[]


    def getGroupFeatures(self,NLQuery):



        grammar = r"""FUNCTION:{(<IN><DT><NN>)|(<NNP><NN>)}"""
        cp = nltk.RegexpParser(grammar)
        intent=nltk.word_tokenize(NLQuery)
        sentence =nltk.pos_tag(intent)

        print sentence

        result = cp.parse(sentence)
        tagsOfQuery=list(result)

        grp1=[]

        for node in range(len(tagsOfQuery)):
            try:
                if result[node].label()=="FUNCTION":
                    grp1.extend(result[node])
            except:
                continue

        if re.findall(' each | per | group | grouping | grouped ',NLQuery):
            grp2=1
        else:
            grp2=0
        #
        # if aggre1:
        #
        #     grp1=1
        # else:
        #
        #     grp1=0
        return [grp2]


F=GroupModel()
s=["Emit the last temperature event per sensor",
"give me every temperature of each device",
"group the temperature stream by device ID and display all the temperatures of each device ID",
"get the temp of each device ID from temperature stream",
"for every sensor, calculate th temperature each sensor has emitted",
"for every 10 events in each temperature group for a device ID get the, device ID, temperature",
"tell the temperature grouped with respect to room",
"find the minimum Temp for each sensor and display the event details",
"Show the temperature for each room ",
"tell the per room and device ID",
"Per office area find the temperature",
"Per office area show the temperature over",
"Per sensor, the temperature events each sensor has emitted",
"give the maximum temperature per room",
"tell the temperature grouped in terms of office area",
"display the temperature grouped by office area",
"Per office area calculate the temperature ",
"tell the temperature grouped with respect to room",
"let me know the temperature over temperature events each sensor has emitted in a group of sensors",
"Grouping with office area show the temperature",
"for every group of sensors, the temperature events each sensor has emitted",
"give the temperature grouped by room",
"tell the temperature grouped in terms of office area",
"grouping by office area find the temperature ",
"calculate the temperature over temperature events each sensor has emitted in a group of sensors"]

for a in s:
    F.getGroupFeatures(a)