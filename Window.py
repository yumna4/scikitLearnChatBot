import nltk
import re

class WindowChecker:
    def check(self, NLQuery):
        window=False
        wordsInNLQuery=nltk.word_tokenize(NLQuery)
        tagsOfNLQuery=nltk.pos_tag(wordsInNLQuery)
        #
        # for tag in tagsOfNLQuery:
        #     if "JJS" in tag:
        #         aggregate=True

        if re.findall('minute|second|hour|day',NLQuery):
            window=True


        return window