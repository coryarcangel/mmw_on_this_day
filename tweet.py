from __future__ import absolute_import, print_function
from functools import reduce

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

    day = "25"#time.strftime("%d").lstrip('0')
    month = "12"#time.strftime("%m").lstrip('0')
    performances = getPerformances(month,day)#[]
    total = len(performances)
    minutetotal = 0
    id = None
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
            #api.update_status(tweet,id)
                #once this id is set the update_status method will start posting tweets as responses
                #id = api.user_timeline()[0].id
    else:
        print("no performances today")

def parseMinutes(timestamp):
    return timestamp.split(":")[0]

def emoji(code=False):
    emojis = ['F600',"F642","F3BC","F60C","F643","F632","F468","F57A","F447","F44C","F442","F952","F3A8","F508","F50A","F4E2","F3BC","F3B5","F3B7","F3B9","F3BB","F4FC"]
    if(code):
        return ("\U0001"+code).decode('unicode-escape').encode("utf-8")
    else:
        return ("\U0001"+emojis[random.randrange(len(emojis))]).decode('unicode-escape').encode("utf-8")

def eGroup(amnt=0):
    out = ""
    groups = [['F600',"F642","F3BC","F60C"],["F643","F632","F468","F57A","F447","F44C"],["F442","F952","F3A8","F508","F50A","F4E2","F3BC"],["F3B5","F3B7","F3B9","F3BB","F4FC"]]
    groups = [["F3A7","","F3BC","F3A4"],["F4DE","F4DF","F39B"],["23F0","F39B","F39E"],["F49A","F499","F49C"],["F192","F193"],["F3B5","F3B6","2714"],["F550","F555","F556"],["F551","F55A","F55B"]] #["262F","262E","F4AF"]
    group = groups[random.randrange(len(groups))]
    if(amnt == 0):
        amnt = 1+random.randrange(len(group)-1)
    for i in range(0,amnt):
        out+= " "+emoji(group[i])
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
    return {
    'piano' : ("" if session[7] =="piano" else session[7]),
    'where': ("" if session[8] =="where" else session[8]),
    'who': ("" if session[9] =="who" else session[9]),
    'minutes': parseMinutes(session[5]),
    'date': session[3],
    'youtubeId': session[6],
    'year': year,
    'yearsAgo': 2017-int(year),
    'count' : str(i+1),
    'total': str(total)
    }

def getFirstTweet(info):
    infoknown = (len(info["piano"]) + len(info["where"]) + len(info["who"])>0)
    if(infoknown):
        out = str(info["yearsAgo"])+" yrs ago,"+info["date"]+ " "+emoji("F4C6")+"  Tony Conrad"+ eGroup() +"  played a "+info["piano"]+ eGroup() +"  @ "+info["where"]
    else:
        out = str(info["yearsAgo"])+" yrs ago,"+info["date"]+ " Tony Conrad played piano for "+info["minutes"]+ ", location and piano unknown"
    out += " " +YOUTUBE_BASE_URL+info["youtubeId"]+ " " + info['which']
    return out

def getSecondTweet(info):
    out = "Tony Conrad, "+ info["date"]+", part "+ info["count"] + eGroup(3)+"  "
    out += " " +YOUTUBE_BASE_URL+info["youtubeId"]+ " " + info['which']

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
    with open('clean_mmw_youtube2.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            datestring = row[3].split("&")
            #print(datestring)
            for date in datestring:
                date = date.replace(" ","")
                if(date.find(month+"/"+day+"/")==0):
                    #print ("oh fuk", date)
                    row[3] = date;
                    performancesFound.append(row);
                else:
                    if(date.find("-"+fixZero(month)+"-"+fixZero(day))==4):
                        row[3] = date;
                        performancesFound.append(row);
    return performancesFound

main()
