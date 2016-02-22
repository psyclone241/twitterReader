# Learning to use Python for Twitter Applications
__author__ = "Roy Keyes"
__credits__ = [""]
__license__ = "BSD 3 Clause"
__version__ = "0.0.1"
__maintainer__ = "Roy Keyes"
__email__ = "keyes.roy@gmail.com"
__status__ = "Development"

# Get the necessary libraries
import os
import argparse
import json
import config

# https://github.com/sixohsix/twitter/tree/master
from twitter import *

def main(config):
    parser = argparse.ArgumentParser(
            description=config.app['description'],
            epilog=''
        )

    # parser.add_argument('-d', action='store', dest='data', help='Data Value: Troop Letter or County Name')
    # parser.add_argument('-t', action='store', dest='type', choices=['county', 'troop'], help='Type of Search, choose "county" or "troop"')
    # parser.add_argument('-o', action='store', dest='output', choices=['print', 'json'], help='Output data to the terminal with print or json (json will not include notes)')
    args = parser.parse_args()
    vars(args)

    if not os.path.exists(os.path.expanduser(config.security['credentials'])):
        oauth_dance('twitterReader', config.security['consumer_key'], config.security['consumer_secret'], config.security['credentials'])

    # store the oauth information, so that it can be used later
    oauth_token, oauth_secret = read_token_file(config.security['credentials'])

    try:
        twitter = Twitter(auth=OAuth(oauth_token, oauth_secret, config.security['consumer_key'], config.security['consumer_secret']))

        if config.feeds:
            for feed in config.feeds:
                if feed in config.feed_config:
                    getFeed(twitter, feed, config.feed_config[feed]['count'])
                else:
                    getFeed(twitter, feed, config.app['default_count'])
        else:
            print('No feeds specified')

    except TwitterHTTPError as twitterError:
        print('There was an authentication error, re-enter your credentials')
        oauth_dance('Twitter Reader', config.security['consumer_key'], config.security['consumer_secret'], config.security['credentials'])
        oauth_token, oauth_secret = read_token_file(config.security['credentials'])

def getUserObject(twitterObject, screen_name):
    lookup = twitter.users.lookup(screen_name=screen_name)
    return lookup

# re-usable code for getting different feeds based on a screen name
def getFeed(twitterObject, screen_name, count):
    # Now work with Twitter
    # twitterObject.statuses.update(status='Hello, world!')
    entries = twitterObject.statuses.user_timeline(screen_name=screen_name, count=count)
    lookup = twitterObject.users.lookup(screen_name=screen_name)

    print('-------------Twitter Feed for @' + screen_name + ' (' + lookup[0]['name'] + ') ------------- ')
    for entry in entries:
        print(entry['created_at'] + ' -> ' + entry['text'])

def dumpclean(obj):
    if type(obj) == dict:
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print k
                dumpclean(v)
            else:
                print '%s : %s' % (k, v)
    elif type(obj) == list:
        for v in obj:
            if hasattr(v, '__iter__'):
                dumpclean(v)
            else:
                print v
    else:
        print obj

# Run the program from here
if __name__ == '__main__':
    main(config)
