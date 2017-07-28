def generateQuery(intent,entities):
    if intent=="Stream definition":
        query ="define stream title (attributes)"
        query=query.replace("title",entities[0])
        query=query.replace("attributes",entities[2])
    return query
