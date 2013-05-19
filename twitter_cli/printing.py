''' todo '''

import tweepy

from twitter_cli.common import api

def print_followers(args):
    user = args.user
    limit = args.limit
    fmt = args.fmt
    for follower in tweepy.Cursor(api.followers, id=user.id).items(limit):
        try:
            print fmt % follower.__dict__

        except tweepy.error.TweepError, e:
            print '* %s (%s)' % (
                    follower.name,
                    follower.screen_name,
                    )
            print '  Error:', e

