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
import traceback

# https://github.com/sixohsix/twitter/tree/master
from twitter import *

class twitterReader:
    def main(self, config):
        self.specific_feed = None
        parser = argparse.ArgumentParser(
            description=config.app['description'],
            epilog=''
        )

        parser.add_argument('-f', action='store', dest='specific_feed', help='Read just one feed', default=None)
        parser.add_argument('-s', action='store', dest='save_file', help='Save the output to file named....', default=None)
        parser.add_argument('-o', action='store', dest='output_type', help='What type of output do you prefer?', default=config.app['default_output'])
        parser.add_argument('-c', type=int, action='store', dest='count', help='Read n items from specified feed', choices=config.app['count_ranges'])
        args = parser.parse_args()
        vars(args)

        if args.specific_feed:
            self.specific_feed = args.specific_feed
        if args.count:
            self.specific_count = args.count
        else:
            self.specific_count = config.app['default_count']

        if args.save_file:
            self.save_file = args.save_file
        else:
            self.save_file = None

        if args.output_type:
            self.output_type = args.output_type
        else:
            self.output_type = config.app['default_output']

        self.print_headers = config.app['print_headers']

        if not os.path.exists(os.path.expanduser(config.security['credentials'])):
            oauth_dance('twitterReader', config.security['consumer_key'], config.security['consumer_secret'], config.security['credentials'])

        # store the oauth information, so that it can be used later
        oauth_token, oauth_secret = read_token_file(config.security['credentials'])

        try:
            twitter = Twitter(auth=OAuth(oauth_token, oauth_secret, config.security['consumer_key'], config.security['consumer_secret']))

            if not self.specific_feed:
                if config.feeds:
                    if self.output_type == 'print':
                        for feed in config.feeds:
                            if feed in config.feed_config:
                                print(self.getFeed(twitter, feed, config.feed_config[feed]['count']))
                            else:
                                print(self.getFeed(twitter, feed, self.specific_count))
                    else:
                        data = {}
                        for feed in config.feeds:
                            if feed in config.feed_config:
                                data[feed] = self.getFeed(twitter, feed, config.feed_config[feed]['count'])
                            else:
                                data[feed] = self.getFeed(twitter, feed, self.specific_count)

                        if self.output_type == 'object':
                            return data
                        else:
                            json_data = json.dumps(data, indent=4)
                            if self.save_file:
                                with open(self.save_file, 'w') as save_file:
                                    save_file.write(json_data)
                            else:
                                return json_data
                else:
                    print('No feeds specified')
            else:
                data = self.getFeed(twitter, self.specific_feed, self.specific_count)
                if self.output_type == 'object':
                    return data
                else:
                    json_data = json.dumps(data, indent=4)
                    if self.save_file:
                        with open(self.save_file, 'w') as save_file:
                            save_file.write(json_data)
                    else:
                        return json_data

        except TwitterHTTPError as twitterError:
            print('There was an authentication error, re-enter your credentials')
            oauth_dance('Twitter Reader', config.security['consumer_key'], config.security['consumer_secret'], config.security['credentials'])
            oauth_token, oauth_secret = read_token_file(config.security['credentials'])

    def getUserObject(self, twitterObject, screen_name):
        lookup = twitter.users.lookup(screen_name=screen_name)
        return lookup

    # re-usable code for getting different feeds based on a screen name
    def getFeed(self, twitterObject, screen_name, count):
        entries = twitterObject.statuses.user_timeline(screen_name=screen_name, count=count)
        lookup = twitterObject.users.lookup(screen_name=screen_name)

        if self.output_type == 'object' or self.output_type == 'json':
            return entries
        else:
            data = ''
            if self.print_headers:
                data += '-------------Twitter Feed for @' + screen_name + ' (' + lookup[0]['name'] + ') -------------' + "\n"
            for entry in entries:
                data += entry['created_at'] + ' -> ' + entry['text'] + "\n"
            return data

    def dumpclean(self, obj):
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

debug = True
if __name__ == '__main__':
    try:
        twitterReader().main(config)
    except Exception as main_run_exception:
        if debug:
            print('__main__: ' + str(main_run_exception))
            print(traceback.format_exc())
        else:
            # TODO: Add logging to the application
            print('We encountered an error, please look at the log file');
    except KeyboardInterrupt:
        pass
