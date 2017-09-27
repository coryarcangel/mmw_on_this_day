from __future__ import absolute_import, print_function
from functools import reduce

import sys
import string
import os
import tweepy
import csv
import time
import random

YOUTUBE_BASE_URL = "https://www.youtube.com/watch?v="
consumer_key=os.environ["CONSUMER_KEY"]
consumer_secret=os.environ["CONSUMER_SECRET"]
access_token=os.environ["ACCESS_TOKEN"]
access_token_secret=os.environ["ACCESS_TOKEN_SECRET"]
counter = 0

def main():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) #https://dev.twitter.com/apps
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth) # OK WE ARE IN
    day = sys.argv[2] if len(sys.argv)>2 else time.strftime("%d").lstrip('0')
    month = sys.argv[1] if len(sys.argv)>1 else time.strftime("%m").lstrip('0')
    performances = getPerformances(month,day)#[]
    total = len(performances)
    minutetotal = 0
    theId = None
    if len(performances)>0:
        for i in range(0,total):
            minutetotal += int(parseMinutes(performances[i][5]))
        for i in range(0,total):
            session = performances[i]
            info = getSessionInfo(session,i,total)
            info['minutes'] = str(minutetotal)
            info['which'] = "("+info['count']+'/'+info['total']+")"
            if(i == 0):
                tweet = getFirstTweet(info)#formatTweet(i,info["year"],total,info["minutes"],info["youtubeId"])+" "+emoji();
            else:
                tweet = getSecondTweet(info)
            print(tweet)
            #api.update_status(tweet,theId)
            #if(theId == None):
            #    theId = api.user_timeline()[0].id
    else:
        print("no performances today")

def parseMinutes(timestamp):
    return timestamp.split(":")[0]

def printEmoji(inp):
    #if we in python 2.*
    #return input.decode('unicode-escape').encode("utf-8")
    print(inp)
    return input

def emoji(code=False):
    emojis = ['F600',"F642","F3BC","F60C","F643","F632","F468","F57A","F447","F44C","F442","F952","F3A8","F508","F50A","F4E2","F3BC","F3B5","F3B7","F3B9","F3BB","F4FC"]
    if(code):
        return printEmoji(("\U0001f604"))
    else:
        return printEmoji(("\U0001f604"))#return printEmoji(('\U0001'+emojis[random.randrange(len(emojis))]))

def eGroup(amnt=0):
    out = ""
    groups = [["F3A7","","F3BC","F3A4"],["F4DE","F4DF","F39B"],["F550","F39B","F39E"],["F49A","F499","F49C"],["F192","F193"],["F3B5","F3B6","2714"],["F550","F555","F556"],["F551","F55A","F55B"]] #["262F","262E","F4AF"]
    groups = [["F3A7","","F3BC","F3A4"],["F4DE","F4DF","F39B"],["23F0","F39B","F39E"],["F49A","F499","F49C"],["F192","F193"],["F3B5","F3B6","2714"],["F550","F555","F556"],["F551","F55A","F55B"]] #["262F","262E","F4AF"]
    groups = [["\U0001F3A7","\U0001F3BC","\U0001F3A4"],["\U0001F4DE","\U0001F4DF","\U0001F39B"],["⏰","\U0001F39B","\U0001F39E"],["\U0001F49A","\U0001F499","\U0001F49C"],["\U0001F192","\U0001F193","\U0001F193"],["\U0001F3B5","\U0001F3B6","✔️"],["\U0001F550","\U0001F555","\U0001F556"],["\U0001F551","\U0001F55A","\U0001F55B"],["☯️","☮️","💯"]]
    group = groups[random.randrange(len(groups))]
    if(amnt == 0):
        amnt = 1+random.randrange(len(group)-1)
    for i in range(0,amnt):
        # python 2.****out+= " "+emoji(group[i])
        out+= "" + group[i]
    return out

def getYear(datefound):
    year = ""
    if datefound[3].find("/")>-1:
        year = datefound[3].split("/")[2];
    else:
        year = datefound[3].split("-")[0];
    return year

def getSessionInfo(session,i,total):
    year = getYear(session)
    #if(session[3].index("/")):
    if("/" in session[3]):
        date = session[3]
    else:
        date = session[3].split("-")[1]+"/"+session[3].split("-")[2]+ "/"+session[3].split("-")[0]
    return {
    'piano' : ("" if session[7] =="piano" else session[7]),
    'where': ("" if session[8] =="where" else session[8]).replace("&",","),
    'who': ("" if session[9] =="who" else session[9]),
    'minutes': parseMinutes(session[5]),
    #'date': session[3],
    'date': date,#session[3].split("-")[1]+"/"+session[3].split("-")[2]+ "/"+session[3].split("-")[0],
    'youtubeId': session[6],
    'year': year,
    'yearsAgo': 2017-int(year),
    'count' : str(i+1),
    'part': session[4],
    'total': str(total)
    }

def getFirstTweet(info):
    infoknown = (len(info["piano"]) + len(info["where"]) + len(info["who"])>0)
    if(infoknown):
        pianoArticle = "a "
        if("David" in info["piano"] or "Ted" in info["piano"]):
            pianoArticle = ""
        pianoPhrase =(pianoArticle+ info["piano"]) if info["piano"] != "" else 'piano'
        locationPhrase = (" @ "+ info["where"]) if info["where"] != "" else ''
        whoPhrase = ("w/ "+ info["who"]) if len(info["who"]) and info["who"] != "" else ''
        #out = str(info["yearsAgo"])+" yrs ago, "+info["date"]+ " \U0001F4C6 Tony Conrad"+ eGroup() +"  played a "+info["piano"]+ eGroup() +"  @ "+info["where"]
        out = str(info["yearsAgo"])+ " yrs ago, "+info["date"]+ " \U0001F4C6 Tony Conrad "+ eGroup() +" played "+pianoPhrase+ eGroup()+ " " +locationPhrase+" "+whoPhrase 
    else:
        out = str(info["yearsAgo"])+" yrs ago, "+info["date"]+ " \U0001F4C6 Tony Conrad played piano \U0001F3A4\U0001F3B5🎹  for "+info["minutes"]+ " minutes, location and piano unknown"
    out += " " +YOUTUBE_BASE_URL+info["youtubeId"]+ " " + info['which']
    return out

def getSecondTweet(info):
    out = "Tony Conrad, "+ info["date"]+", part "+ info["part"] + " "+eGroup(3)+" "
    out +=YOUTUBE_BASE_URL+info["youtubeId"]+ " " + info['which']

    return out

def formatTweet(count,year,total,minutes,youtubeId):
    count = "("+str(count+1)+"/"+str(total)+")"
    tweet = "On this day in "+year+", Tony recorded this: "# if count>0 else '')
    tweet+= minutes+" minutes,"
    tweet+= YOUTUBE_BASE_URL+youtubeId+ " "
    tweet+= count
    return tweet

def fixZero(num):
    if(len(num) == 1):
        return "0" + num
    return num

def getPerformances(month,day):
    performancesFound = []
    outPerformances = []
    with open('clean_mmw_youtube2.csv', 'rt') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            datestring = row[3].split("&")
            for date in datestring:
                date = date.replace(" ","")
                if(date.find(month+"/"+day+"/")==0):
                    row[3] = date;
                    performancesFound.append(row);
                else:
                    if(date.find("-"+fixZero(month)+"-"+fixZero(day))==4):
                        row[3] = date;
                        performancesFound.append(row);
    #now, pick a year and remove everything else not in that year
    if(len(performancesFound) == 0):
        return outPerformances
    randomPerformance = performancesFound[random.randrange(len(performancesFound))]
    randomYear = getYear(randomPerformance)
    for perf in performancesFound:
        if(perf[3].find(randomYear)>-1):
            outPerformances.append(perf)
    #return performancesFound
    return outPerformances

main()
