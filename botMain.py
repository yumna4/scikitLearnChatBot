#this file takes input from user and shows the chatBot's response
from modelLoad import response
from entity import extractEntity
res=raw_input("User>")

#res = input given by user



while len(res)>0:
    botRes = response(res)
    print botRes
    print extractEntity(res,botRes)
    res=raw_input("User>")


