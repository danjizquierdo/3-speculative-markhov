#!/usr/bin/python

import subprocess
import random
import re
import os
import time
from twython import Twython
from raise_corpus import Necromancer

with open('./keys.txt') as f:
    content=f.readlines()
keys= [line.strip() for line in content]

# input API key, API secret key, Access token, Secret access token

twitter = Twython(keys[0],
                  keys[1],
                  keys[2],
                  keys[3])

def output_tweet(text,tweeted):
    if tweeted==0:
        twitter.update_status(status=text)
    else:
        last_tweet=twitter.get_home_timeline(count=1)
        twitter.update_status(status=text,in_reply_to_status_id=last_tweet[0]['id'])

# generate title and description
tweet = Necromancer().shambler('title',6)
tweet+= ': '+Necromancer().shambler('description',60)
dregs=''
tweeted=0
while len(tweet) > 280:
    # if it is too long, try to cut off at a sentence
    try:
        dregs= re.search("(.+?\.)(.*)", tweet).group(2)
        tweet= re.search("(.+?\.)(.*)", tweet).group(1)
        if len(tweet) >280:
            # at least we tried, just take the first 140 characters
            dregs=tweet[280:]+dregs
            tweet=tweet[:280]
    except:
        if len(tweet) >280:
            # at least we tried, just take the first 140 characters
            dregs=tweet[280:]+dregs
            tweet=tweet[:280]
    output_tweet(tweet,tweeted)
    tweeted=1
    time.sleep(1)
    tweet=dregs
output_tweet(tweet,tweeted)
os._exit(0)