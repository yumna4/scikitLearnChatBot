import re
from test1.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

class TokenWords:

    def getTokenWordsPattern(self,words):
        wordsPattern=[]

        #words = [stemmer.stem(w.lower()) for w in words]

        words= ' '.join(words)
        #print words
        # #show
        # if re.findall('show |get| display |find|calc',words):
        #     wordsPattern.append(1)
        # else:
        #     wordsPattern.append(0)



        #window

        #testing for any unit of Time -window
        if re.findall('second |minut| hour |day| week| month |year',words):
            wordsPattern.append(1)
        else:
            wordsPattern.append(0)


        #testing for last,final,recent -window
        if re.findall('last|final|recent|past',words):
            wordsPattern.append(1)
        else:
            wordsPattern.append(0)


        #pattern OR filter
        if re.findall('within|inside|between|in',words):#between events NOT between two numbers
            wordsPattern.append(1)
        else:
            wordsPattern.append(0)



        #sequence consecutive, followed peak
        if re.findall('consecutive|follow|peak',words):#between events NOT between two numbers
            wordsPattern.append(1)
        else:
            wordsPattern.append(0)



        #AGGREGATE


        #avergae, maximum, minimum, sum,count
        if re.findall('maxim|greatest|largest|biggest|minim|smallest|highest|lowest|count|number|add|average|norm|sum|total|peak',words):#between events NOT between two numbers
            wordsPattern.append(1)
            #print  re.findall('maxim|greatest|largest|biggest|minim|smallest|highest|lowest|count|numb|ad|average|norm|sum|tot|peak',words)#between events NOT between two numbers

        else:
            wordsPattern.append(0)

        #output event category
        #all
        if re.findall('all|full|whol',words):#between events NOT between two numbers
            wordsPattern.append(1)
        else:
            wordsPattern.append(0)


        #window
        if re.findall('window',words):#between events NOT between two numbers
            wordsPattern.append(1)
        else:
            wordsPattern.append(0)


        #filter
        #which
        if re.findall('which|that|whatev|whichev',words):
            wordsPattern.append(1)
        else:
            wordsPattern.append(0)

        #group
        if re.findall('group',words):#between events NOT between two numbers
            wordsPattern.append(1)
        else:
            wordsPattern.append(0)


        #group, partition
        #each,a
        if re.findall('each|per',words):#between events NOT between two numbers
            wordsPattern.append(1)
        else:
            wordsPattern.append(0)

        # #events
        # if re.findall('event',words):#between events NOT between two numbers
        #     wordsPattern.append(1)
        # else:
        #     wordsPattern.append(0)

        #every
        if re.findall('every',words):#between events NOT between two numbers
            wordsPattern.append(1)
        else:
            wordsPattern.append(0)

        #reach
        if re.findall('reach|match|equal|becom|same|as',words):#between events NOT between two numbers
            wordsPattern.append(1)
        else:
            wordsPattern.append(0)

        #change
        if re.findall('next|immediate',words):#between events NOT between two numbers
            wordsPattern.append(1)
        else:
            wordsPattern.append(0)

        #filter
        if re.findall('filt',words):#between events NOT between two numbers
            wordsPattern.append(1)
        else:
            wordsPattern.append(0)


        #greater smaller in filter
        if re.findall('great|small|low|between|high|big|abov|below|mor|less',words):#between events NOT between two numbers
            wordsPattern.append(1)
        else:
            wordsPattern.append(0)



        #rate
        if re.findall('rate',words):#between events NOT between two numbers
            wordsPattern.append(1)
        else:
            wordsPattern.append(0)

        #snapshot
        if re.findall('snapshot',words):#between events NOT between two numbers
            wordsPattern.append(1)
        else:
            wordsPattern.append(0)

        #increase decrease
        if re.findall('increas|decreas|reduc|ris|limit|rais|drop',words):#between events NOT between two numbers

            wordsPattern.append(1)
        else:
            wordsPattern.append(0)


        return wordsPattern


