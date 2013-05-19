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


def print_unfollowers(args):
    user = args.user
    limit = args.limit
    fmt = args.fmt
    friends_ids = api.friends_ids(user.id)[0]
    followers_ids = user.followers_ids()[0]
    i = 0
    for friend_id in friends_ids:
        if friend_id in followers_ids:
            continue
        i += 1
        if i > limit:
            return
        if not api.exists_friendship(friend_id, user.id):
            friend = api.get_user(friend_id)
            try:
                print fmt % friend.__dict__

            except tweepy.error.TweepError, e:
                print '* %s (%s)' % (
                        friend.name,
                        friend.screen_name,
                        )
                print '  Error:', e

