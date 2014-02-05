from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import json
import threading
import time
import imp
from os.path import expanduser

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

#just try followers every 2 hours
def monitor_followers():
    threading.Timer(120.0, monitor_followers).start()
    follow_back()
    
class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def __init__( self, delay ):
        self.SEC_BETWEEN_TWEET = delay #24.0
        self.last_tweet = 0
    
    def clear_to_tweet( self ):
        now = time.time()
        elapsed = now - self.last_tweet
        if elapsed > self.SEC_BETWEEN_TWEET:
            self.last_tweet = now
            return True
        else:
            return False
    
    def on_data(self, data):
        decoded = json.loads(data)
        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        try:
            print 'Tweet from!  @%s ' % (decoded['user']['screen_name'] )
            if decoded['user']['screen_name'] != '@mypibot' and self.clear_to_tweet():
                api.retweet(decoded['id'])
            else:
                print 'Skipped Retweet!'
        except KeyError:
            print 'KeyError: Skipped Retweet!'
            pass
        return True

    def on_error(self, status):
        print status

def monitorText( text, delay ):
    l = StdOutListener(delay)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track=[text])

def monitorPrPig( ):
    while True:
        try:
            monitorText( '#prpig', 12 )
        except tweepy.TweepError as e:
            print 'Exception PrPig'

def monitorRasPi( ):
    while True:
        try:
            monitorText( 'raspberry pi', 20 )
        except tweepy.TweepError as e:
            print 'Exception RasPi - wait some time before resuming'
            tim.sleep( 30 )

#if __name__ == '__main__':    
    #l = StdOutListener()
    #auth = OAuthHandler(consumer_key, consumer_secret)
    #auth.set_access_token(access_token, access_token_secret)
    ##Monitor followers
    #monitor_followers()
    
    #stream = Stream(auth, l)
    #stream.filter(track=['my super tweet'])
    #print 'Continued!!'
    
    ##launch follow back monitor
    ##Monitor followers
    #monitor_followers()

if __name__ == '__main__':    
    #Monitor followers
    monitor_followers()    
    threading.Timer(15.0, monitorPrPig ).start()
    threading.Timer(25.0, monitorSuperBowl ).start()    
    monitorRasPi()
