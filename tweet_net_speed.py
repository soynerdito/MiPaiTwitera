#!/usr/bin/env python2.7  
import tweepy  
import random  
import imp
from os.path import expanduser
from speed import SpeedResults
import speed

#Load auth keys from storage
home = expanduser("~")
my_keys = imp.load_source('tweet_oath', '%s/.keys/tweet_oath.py' % ( home ) )

#Information for mypibot Tweeter account
access_token = my_keys.access_token
access_token_secret = my_keys.access_token_secret
consumer_key = my_keys.consumer_key
consumer_secret = my_keys.consumer_secret

# OAuth process, using the keys and tokens  
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
auth.set_access_token(access_token, access_token_secret)  
  
# Creation of the actual interface, using authentication  
api = tweepy.API(auth)  
  
follow2 = api.followers_ids() # gives a list of followers ids  
print "you have %d followers" % len(follow2)  
print 'Ready to use api'

results = speed.speedresults()

api.update_status('My Web now is\n %s' % (results) , 1 )
