import nltk
import re

class AggregateFunctionChecker:
    def check(self, NLQuery):
        aggregate=False
        wordsInNLQuery=nltk.word_tokenize(NLQuery)
        tagsOfNLQuery=nltk.pos_tag(wordsInNLQuery)



        for tag in tagsOfNLQuery:
            if "JJS" in tag:
                aggregate=True



        if re.findall('maximum|minimum|count|number|add|average|normal|sum|total|peak',NLQuery):
            aggregate=True



        return aggregate

#
# D=AggregateFunctionChecker()
# D.check("show the average temperarure for each sensor")