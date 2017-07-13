#this file takes input from user and shows the chatBot's response
from modelLoad import response

res=raw_input("User>")
#res = input given by user
while len(res)>0:
    botRes = response(res)
    print botRes
    #botRes = response given by chatBot
    res=raw_input("User>")


