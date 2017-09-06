from __future__ import absolute_import, print_function

import os
import tweepy
import csv
import time
import random

def emoji():
    emojis = ['F600',"F642","F3BC","F60C","F643","F632","F468","F57A","F447","F44C","F442","F952","F3A8","F508","F50A","F4E2","F3BC","F3B5","F3B7","F3B9","F3BB","F4FC"]
    #return ("\U0001"+emojis[random.randrange(len(emojis))]).decode('unicode-escape').encode("utf-8")

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key=os.environ["CONSUMER_KEY"]
consumer_secret=os.environ["CONSUMER_SECRET"]

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
access_token=os.environ["ACCESS_TOKEN"]
access_token_secret=os.environ["ACCESS_TOKEN_SECRET"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# If the authentication was successful, you should
# see the name of the account print out
#print(api.me().name)

# If the application settings are set for "Read and Write" then
# this line should tweet out the message to your account's
# timeline. The "Read and Write" setting is on https://dev.twitter.com/apps
day = time.strftime("%d").lstrip('0')
month = time.strftime("%m").lstrip('0')
fixedday = day
fixedmonth = month
if(len(day) == 1):
    fixedday = "0" + day
if(len(month) == 1):
    fixedmonth = "0" + month
#print(fixedday,fixedmonth)

datesfound = []
with open('clean_mmw_youtube.csv', 'rt') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        datestring = row[3].split("&")
        #print(datestring)
        for date in datestring:
            date = date.replace(" ","")
            if(date.find(month+"/"+day+"/")==0):
                #print ("oh fuk", date)
                row[3] = date;
                datesfound.append(row);
            else:
                if(date.find("-"+fixedmonth+"-"+fixedday)==4):
                    row[3] = date;
                    datesfound.append(row);
print("day: ",day,"month: ",month)
if len(datesfound)>0:
    choice = datesfound[random.randrange(len(datesfound))]
    print("choice ",choice)
    year = ""
    if choice[3].find("/")>-1:
        year = choice[3].split("/")[2];
    else:
        year = choice[3].split("-")[0];
    #mmw
    #info
    #real
    #date
    #part?
    #elapsed
    #youtube id
    tweet = "On this day in "+year+", Tony recorded this: https://www.youtube.com/watch?v="+choice[6]+" "#+emoji();
    print (tweet)
    api.update_status(status=tweet)
else:
    print("no performances today")
