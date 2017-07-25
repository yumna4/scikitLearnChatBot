from pycorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://localhost:9000')
res = nlp.annotate("take a from b and put in c",
                   properties={
                       'annotators': 'depparse',
                       'outputFormat': 'json',
                       'timeout': 1000,
                   })
for s in res['sentences']:
    ED= s['enhancedDependencies']

for ed in ED:
    print "type: %s words:'%s', %s : %d , %d" % (ed['dep'], ed['governorGloss'], ed['dependentGloss'],ed['governor'],ed['dependent'])
