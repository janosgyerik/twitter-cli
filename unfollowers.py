#!/usr/bin/env python
#

import argparse
import os

default_limit = 5
default_fmt = '%(screen_name)s'
#fmt = '* %(name)s (%(screen_name)s) t#=%(statuses_count)d fg=%(friends_count)d ff=%(followers_count)d l=%(lang)s\n%(description)s'

parser = argparse.ArgumentParser(description='Show users not following back')
parser.add_argument('--limit', '-l', type=int, default=default_limit)
parser.add_argument('--format', '-f', dest='fmt', default=default_fmt)
parser.add_argument('--user', '-u')
parser.add_argument('--whitelisted', '-w', nargs='+',
        help='File with list of whitelisted users')

args = parser.parse_args()

if args.whitelisted:
    whitelisted = set()
    for path in args.whitelisted:
        if os.path.isfile(path):
            with open(path) as instream:
                for line in instream.readlines():
                    whitelisted.add(line.strip())
    args.whitelisted = whitelisted
else:
    args.whitelisted = ()


from twitter_cli.common import api

if args.user:
    args.user = api.get_user(args.user)
else:
    args.user = api.me()

from twitter_cli.printing import print_unfollowers
print_unfollowers(args)

# eof
