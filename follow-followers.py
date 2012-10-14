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

import sys
import os

blacklisted_ids = set()
blacklisted_names = set()
f = open('blacklist.txt')
for line in f.readlines():
    data = json.loads(line)
    blacklisted_ids.add(data['id'])
    blacklisted_names.add(data['name'])

blacklist = open('blacklist.txt', 'a+')

for follower in me.followers():
    if not follower.following:
        if follower.id in blacklisted_ids:
            continue
        os.system('clear')
        try:
            print '* %s (%s) t#=%d fg=%d ff=%d l=%s' % (
                    follower.name,
                    follower.screen_name,
                    follower.statuses_count,
                    follower.friends_count,
                    follower.followers_count,
                    follower.lang
                    )
            print ' ', follower.description

            for st in follower.timeline()[:4]:
                print '    ', '-' * 70
                i = 0
                while i < len(st.text):
                    print '    ', st.text[i:i+70]
                    i += 70
                print '    ', st.created_at.strftime('%Y-%m-%d %H:%M')

        except tweepy.error.TweepError, e:
            print '* %s (%s)' % (
                    follower.name,
                    follower.screen_name,
                    )
            print '  Error:', e
        print
        print '[F]ollow?, [B]lacklist?, (anything else to skip) ',
        line = sys.stdin.readline()
        if line.lower().startswith('f'):
            follower.follow()
        elif line.lower().startswith('b'):
            data = {
                    'name': follower.name,
                    'screen_name': follower.screen_name,
                    'id': follower.id,
                    }
            blacklist.write(json.dumps(data))
            blacklist.write('\n')
            blacklist.flush()
        

# eof
