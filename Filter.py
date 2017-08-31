import nltk
import re

class FilterChecker:
    def check(self, NLQuery):
        filter=False
        wordsInNLQuery=nltk.word_tokenize(NLQuery)
        tagsOfNLQuery=nltk.pos_tag(wordsInNLQuery)

        for tag in tagsOfNLQuery:
            if "JJR" in tag:

                filter=True

        if re.findall('between|above|below|more|less|few',NLQuery):

            filter=True


        return filter

