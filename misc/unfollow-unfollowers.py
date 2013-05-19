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

f = open('whitelist.txt')
whitelisted_screen_names = set()
for line in f.readlines():
    whitelisted_screen_names.add(line.strip())

whitelist = open('whitelist.txt', 'a+')

friends_ids = api.friends_ids(me.id)
followers_ids = me.followers_ids()
j = 0
for friend_id in friends_ids:
    j += 1
    if friend_id in followers_ids:
        continue
    friend = api.get_user(friend_id)
    if friend.screen_name in whitelisted_screen_names:
        continue
    if not api.exists_friendship(friend_id, me.id):
        os.system('clear')
        print 'Friend %d / %d' % (j, len(friends_ids))
        try:
            print '* %s (%s) t#=%d fg=%d ff=%d l=%s' % (
                    friend.name,
                    friend.screen_name,
                    friend.statuses_count,
                    friend.friends_count,
                    friend.friends_count,
                    friend.lang
                    )
            print ' ', friend.description

            for st in friend.timeline()[:4]:
                print '    ', '-' * 70
                i = 0
                while i < len(st.text):
                    print '    ', st.text[i:i+70]
                    i += 70
                print '    ', st.created_at.strftime('%Y-%m-%d %H:%M')

        except tweepy.error.TweepError, e:
            print '* %s (%s)' % (
                    friend.name,
                    friend.screen_name,
                    )
            print '  Error:', e
        print
        print '[U]nfollow?, [W]hitelist?, (anything else to skip) ',
        line = sys.stdin.readline()
        if line.lower().startswith('u'):
            friend.unfollow()
        elif line.lower().startswith('w'):
            whitelist.write(friend.screen_name)
            whitelist.write('\n')
            whitelist.flush()
        

# eof
