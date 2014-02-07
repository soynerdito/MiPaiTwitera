from os.path import expanduser
from random import randint
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import json
import threading
import time
import imp

#Load auth keys from storage
home = expanduser("~")
my_keys = imp.load_source('tweet_oath', '%s/.keys/tweet_oath.py' % ( home ) )

#Information for mypibot Tweeter account
access_token = my_keys.access_token
access_token_secret = my_keys.access_token_secret
consumer_key = my_keys.consumer_key
consumer_secret = my_keys.consumer_secret

#records the last time it was tweeted
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
auth.set_access_token(access_token, access_token_secret)          
# Creation of the actual interface, using authentication  
api = tweepy.API(auth)        

def follow_back():
    for follower in tweepy.Cursor(api.followers).items():
        if follower.id not in api.friends_ids( ):
            follower.follow()
            print 'New Follower @%s' % ( follower.screen_name )


#Create a random number and tweet it
lucky_num = randint(2,1000) #Inclusive

follow_back()

# Creation of the actual interface, using authentication  
api = tweepy.API(auth)  
  
follow2 = api.followers_ids() # gives a list of followers ids  
try:
    api.update_status( ' I  have %d followers ' % len(follow2), 1  )
except:
    pass

time.sleep(5)

try:
    api = tweepy.API(auth)  
    api.update_status('Lucky number of now is %d - JUEGALO!' % lucky_num, 2 )
except:
    pass
