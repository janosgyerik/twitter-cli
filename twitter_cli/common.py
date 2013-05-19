#!/usr/bin/env python
#
# To access twitter with OAuth, you need to first obtain:
#	consumer key, consumer secret, access token, access token secret
#
# 1. Login to Twitter
# 2. Go to https://dev.twitter.com/apps/new and fill the form
#	- Application Type should be Client
#	- Default Access Type must be Read and Write
# 3. Consumer key and secret are here: https://dev.twitter.com/apps
# 4. Access token and secret are in the My Access Token menu
# 5. Go to edit profile and make sure Tweet Location is enabled
#

import tweepy  # 3rd party lib, install with: easy_install tweepy
import settings
import json

try:
    consumer_key = settings.TWITTER.get('consumer_key')
    consumer_secret = settings.TWITTER.get('consumer_secret')
    access_token = settings.TWITTER.get('access_token')
    access_token_secret = settings.TWITTER.get('access_token_secret')
except:
    raise ValueError('You must define settings.TWITTER with keys:\n'
        '  consumer_key\n'
        '  consumer_secret\n'
        '  access_token\n'
        '  access_token_secret')


# set up credentials to use Twitter api.
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# tweet with GPS coordinates
#api.update_status(tweetmsg, lat=data.gps.lat, long=data.gps.lon)

me = api.me()

# eof
