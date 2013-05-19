#!/usr/bin/env python
#

from time import sleep
import argparse

default_limit = 5
default_fmt = '%(screen_name)s'
#fmt = '* %(name)s (%(screen_name)s) t#=%(statuses_count)d fg=%(friends_count)d ff=%(followers_count)d l=%(lang)s\n%(description)s'

parser = argparse.ArgumentParser(description='Show users not following back')
parser.add_argument('files', metavar='FILE...', nargs='+',
        help='Files with lists of usernames')
parser.add_argument('--limit', '-l', type=int, default=default_limit)
parser.add_argument('--format', '-f', dest='fmt', default=default_fmt)

args = parser.parse_args()

from twitter_cli.common import api

me = api.me()
friends_ids = api.friends_ids(me.id)[0]

for filename in args.files:
    with open(filename) as instream:
        i = 0
        for line in instream.readlines():
            username = line.strip()
            user = api.get_user(username)
            if user.id not in friends_ids:
                continue
            i += 1
            if i > args.limit:
                break
            print 'unfollowing', username, '...'
            user.unfollow()

