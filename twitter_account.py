"""
This module handles all communication with the Twitter API. It handles request
limits, extracts followers, and extracts tweets. Furthermore there is the
possibility to save data to a json file.
"""
#!/usr/bin/python
# -*- coding: utf-8 -*-
import tweepy
import datetime
import time

class TwitterAccount:

    """
....Class used to handle all twitter requests.
...."""

    def __init__(
            self,
            CONSUMER_KEY,
            CONSUMER_SECRET,
            OAUTH_TOKEN,
            OAUTH_TOKEN_SECRET,
            screen_name,
    ):

        self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        self.api = tweepy.API(self.auth)
        self.screen_name = screen_name
		
		self.limits = self.update_rate_limits();

    def update_rate_limits(self):
        """
........Updates the rate limits dictionary.
........This dictionary will contain the remaining user requests,
........followers requests, and statuses requests. If the limit
........for checking the rate limits is exceeded the program will
........sleep until the limit resets.
........"""

        limits = self.api.rate_limit_status( \
                    resources='users,followers,statuses,application')
		
        if limits['resources']['application'] \
                  ['/application/rate_limit_status']['remaining'] <= 0:
            print ("  Rate limit exceded, resets to {} at {:%m/%d/%Y %H:%M}"\
                        .format(limits['resources']['application']\
                            ['/application/rate_limit_status']['limit'],\
                        datetime.datetime.fromtimestamp(limits['resources']\
                            ['application']\
                            ['/application/rate_limit_status']['reset']))
            )
            self.sleep_until(datetime.datetime.fromtimestamp(\
			                    limits['resources']\
                                      ['application']\
                                      ['/application/rate_limit_status']\
                                      ['reset']))

        remain_search_limits = limits['resources']['users']\
                                     ['/users/show/:id']['remaining']

        return {
            'users': limits['resources']['users']['/users/show/:id'],
            'followers': limits['resources']['followers']['/followers/ids'],
            'statuses': limits['resources']['statuses']\
                              ['/statuses/user_timeline']
			'search': limits['resources']['search']\
							['/search/tweets']
        }

    def check_rate_limits(self, rate_limits, resources):
        """
........Checks the rate limit for a specific resource given
........a rate limits dictionary. If the remaining requests for
........the resource exceeds the program will sleep until
........it resets. The second input is which resource to check.
........"""
		rate_limits = self.limits
        if rate_limits[resources]['remaining'] <= 0:
            print "  Rate limit exceded, resets to {} at {:%m/%d/%Y %H:%M}"\
                .format(
                    rate_limits[resources]['limit'],
                    datetime.datetime.fromtimestamp(\
                        rate_limits[resources]['reset'])
            )
            return False
        else:
            print "  {} {} requests remaining until {:%m/%d/%Y %H:%M}".format(
                rate_limits[resources]['remaining'],
                resources,
                datetime.datetime.fromtimestamp(rate_limits[resources]['reset'])
            )
            return True

    def get_followers_of_user(self, user_screen_name):
        """
........Returns a list of follower ids of the input user name.
........"""
        followers = []
		
		self.limits = self.update_rate_limits()

        if self.check_rate_limits('followers'):

            for page in tweepy.Cursor(self.api.followers_ids,\
                                      screen_name=user_screen_name)\
									  .pages():
                #self.limits = self.update_rate_limits()

                if not self.check_rate_limits('followers'):
                    self.sleep_until()

                followers_temp = []
                followers_temp.append(page)

                for ids in followers_temp[0]:
                    followers.append(ids)

        else:
            self.sleep_until()
            self.get_followers_of_user(user_screen_name)

        return followers

    def get_user(self, id, limits):
        """
........Returns the user object of a user given the user id.
........Also it needs a dictionary of requests limits.
........"""
        if self.check_rate_limits('users'):
            user = 0
            try:
                user = self.api.get_user(id)
            except tweepy.TweepError, error:
                print type(error)
				# Checks if the user is suspended or not authorized to access.
                if str(error) == 'User has been suspended.':
                    print '  User suspended'
                    return 0
                if str(error) == 'Not authorized.':
                    print ' Cannot access user data - not authorized.'
                    return 0
            return user
        else:
            self.sleep_until()
            user = 0
            try:
                user = self.api.get_user(id)
            except tweepy.TweepError, error:
                print type(error)

                if str(error) == 'User has been suspended.':
                    print '  User suspended'
                    return 0
                if str(error) == 'Not authorized.':
                    print ' Cannot access user data - not authorized.'
                    return 0
            return user

    def get_tweets_from_user(self, user_id, number_of_tweets):
        """
........Extracts a specific number of tweets from a user starting from
........the most recent tweet. Input is the user id and the number of
........tweets which should be returned.
........"""
        tweets = []
        user = self.get_user(user_id, self.limits)

        # Handles if the user has a protected account or
		# another error (user = 0)
        if user == 0:
            tweets.append(' ')
            return tweets
        if user.protected == True:
            tweets.append(' ')
            return tweets

        if self.check_rate_limits('statuses'):
            try:
                tweets_temp = self.api.user_timeline(\
                                user_id, count=number_of_tweets)
            except tweepy.TweepError as e:
                print e.response.status

            # Discard all retweets (all retweets starts with "RT")
			#(tweepy's retweeted boolean does not work)
            for tweet in tweets_temp:
                if len(tweet.text) < 2:
                    tweets.append(tweet.text)
                elif tweet.text[0] != "R" and tweet.text[1] != "T":
                    tweets.append(tweet.text)
        else:
            self.sleep_until()
            self.get_tweets_from_user(user_id, number_of_tweets)

        return tweets

    def sleep_until(self, max_sleep_interval=60):
        """
........The program will sleep until the time reaches a given time stamp.
........Input is the wake up time and the maximum sleep interval.
........"""
		self.limits = self.update_rate_limits()
		wake_up_datetime = datetime.datetime.fromtimestamp(limits['statuses']['reset'])
        while True:
            # Calculate the seconds until wake up plus a 4 second
			# buffer for security
            seconds_until_wake = (wake_up_datetime - datetime.datetime.now())\
                                    .total_seconds()+4

            if seconds_until_wake < 0.0:
                break

            sleep_seconds = min(seconds_until_wake, max_sleep_interval)

            print "  {}s until wakeup, sleeping for another {}s"\
                    .format(seconds_until_wake, sleep_seconds)

            time.sleep(sleep_seconds)

        print "  Waking up"


