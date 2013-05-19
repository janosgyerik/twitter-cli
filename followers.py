''' todo '''

import tweepy

def print_followers(args):
    user = args.user
    limit = args.limit
    fmt = args.fmt
    for follower in user.followers()[:limit]:
        try:
            print fmt % follower.__dict__

        except tweepy.error.TweepError, e:
            print '* %s (%s)' % (
                    follower.name,
                    follower.screen_name,
                    )
            print '  Error:', e

