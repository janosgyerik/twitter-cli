#!/usr/bin/env python
#

import argparse

default_limit = 5
default_fmt = '%(screen_name)s'
#fmt = '* %(name)s (%(screen_name)s) t#=%(statuses_count)d fg=%(friends_count)d ff=%(followers_count)d l=%(lang)s\n%(description)s'

parser = argparse.ArgumentParser(description='Twitter CLI')
parser.add_argument('command', metavar='COMMAND', nargs='?')
parser.add_argument('--limit', '-l', type=int, default=default_limit)
parser.add_argument('--format', '-f', dest='fmt', default=default_fmt)
parser.add_argument('--user', '-u')

args = parser.parse_args()

from common import me
if not args.user:
    args.user = me

if args.command == 'followers':
    import followers
    followers.print_followers(args)

# eof
