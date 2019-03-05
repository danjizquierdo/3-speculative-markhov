#!/anaconda3/bin/python
import subprocess
import random
import re
import os
import sys
import time
from twython import Twython
from raise_corpus import Necromancer

# open keys stored locally
with open('/Users/flatironschool/blogs/3-speculative-markhov/keys.txt') as f:
    content=f.readlines()
keys= [line.strip() for line in content]
# input API key, API secret key, Access token, Secret access token

twitter = Twython(keys[0],
                  keys[1],
                  keys[2],
                  keys[3])

def output_tweet(text,tweeted):
"""
Take given text and send it as a tweet. If tweeted is not 0 then the tweet will be sent as a reply to the most recent update for this profile.    
"""
	if tweeted==0:
		twitter.update_status(status=text)
	else:
		last_tweet=twitter.get_home_timeline(count=1)
		twitter.update_status(status=text,in_reply_to_status_id=last_tweet[0]['id'])

# generate title and description from Markhov chain generator class
tweet = Necromancer().shambler('title',6)
tweet+= ': '+Necromancer().shambler('description',60)
# initialize leftover text string
dregs=''
# initialize boolean to check if a tweet has already been sent
tweeted=0
# checks if a tweet is too long
while len(tweet) > 280:
    # if it is too long, try to cut off at the end of a sentence
    try:
        dregs= re.search(r"(.+?\.)(.*)", tweet).group(2)
        tweet= re.search(r"(.+?\.)(.*)", tweet).group(1)
        if len(tweet) >280:
            # at least we tried, just take the first 280 characters and
            # store the rest
            dregs=tweet[280:]+dregs
            tweet=tweet[:280]
    except:
        if len(tweet) >280:
            # at least we tried, just take the first 280 characters
            dregs=tweet[280:]+dregs
            tweet=tweet[:280]
    # send out the first part of the tweet
    output_tweet(tweet,tweeted)
    # make sure to set that we already tweeted
    tweeted=1
    time.sleep(1)
    # reset the text to only the part that has not been sent yet
    tweet=dregs
# send out whatever text is left
output_tweet(tweet,tweeted)
os._exit(0)