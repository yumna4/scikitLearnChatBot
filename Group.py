import re

class GroupChecker:
    def check(self,NLQuery):
        group=False
        if re.findall('each| per ',NLQuery):

            group=True


        return group


