##############################################################################
#### Program Name: Part 1: Getting Started with the Twitter Search API    ####
#### Author: Arijit Upadhyaya                                             ####
#### UIN: 423000515                                                       ####
#### email: arijit@cse.tamu.edu                                           ####
##############################################################################


__author__ = 'arijit'

import tweepy
import sys

####################################
### Enter your keys here          ##
####################################
access_token_key = ''
access_token_secret = ''
consumer_key = ''
consumer_secret = ''
######################################
######################################


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)

api = tweepy.API(auth)
## give the movie name as argument
query = sys.argv[1]
#query = "Divergent"

#########################################################################
## Collecting Tweets and dumping them in the file tweets_collected.txt ##
#########################################################################
def search_tweet(api):
    tweet_string = ''
   # query = raw_input('Enter a query to search: ')
    i = int(1)
    for tweet in tweepy.Cursor(api.search,
                           q=query,
                           rpp=100,
                          # result_type="popular",
						   result_type='recent',
						   ## Add the movie release date below
						   since="2014-4-1",
						   #until="2014-4-8",
                           include_entities=True,
                           lang="en").items():
        unicode_string = tweet.text
        encoded_string = unicode_string.encode('utf-8')
        print encoded_string
        #print i, tweet.text
        #print tweet.created_at
        #tprint encoded_string, tweet.created_at
        tweet_string += encoded_string + '\n'
        i += 1
        ### 1000000 controls the number of tweets
        if(i>10000):
            break
    with open('tweets_collected.txt', 'w') as f:
        f.write(tweet_string)

search_tweet(api)
