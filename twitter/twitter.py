# -*- coding: utf-8 -*-

import requests
from requests_oauthlib import OAuth1
from .exception import Exception
from .tweet import Tweet
from .search import Search
from .timeline import Timeline
from .status import Status

from urlparse import parse_qs
from sys import maxint


class Twitter(object):
    _base_url = 'https://api.twitter.com/1.1/'
    _verify_url = 'account/verify_credentials.json'
    _search_url = 'search/tweets.json'
    _lang_url = 'help/languages.json'
    _user_url = 'statuses/user_timeline.json'

    def __init__(self, consumer_key, consumer_secret,
                 access_token, access_token_secret, **attr):
        # app
        self.__consumer_key = consumer_key
        self.__consumer_secret = consumer_secret

        # user
        self.__access_token = access_token
        self.__access_token_secret = access_token_secret

        # init internal variables
        self.__response = {}
        self.__nextMaxID = maxint
        self.__next_tweet = 0

        if "proxy" in attr:
            self.set_proxy(attr["proxy"])
        else:
            self.__proxy = None

        # callback
        self.__callback = None

        # verify
        if "verify" in attr:
            self.authenticate(attr["verify"])
        else:
            self.authenticate(True)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.__access_token)

    def authenticate(self, verify=True):
        self.__oauth = OAuth1(self.__consumer_key,
                              client_secret=self.__consumer_secret,
                              resource_owner_key=self.__access_token,
                              resource_owner_secret=self.__access_token_secret)

        if verify:
            r = requests.get(self._base_url + self._verify_url,
                             auth=self.__oauth,
                             proxies={"https": self.__proxy})
            Status(r.status_code)

    def search_tweets_iterable(self, tweet, callback=None):
        if callback:
            if not callable(callback):
                raise Exception("Twitter - search_tweets_iterable")
            self.__callback = callback

        self.search_tweets(tweet)
        return self

    def get_minimal_id(self):
        if not self.__response:
            raise Exception("Twitter - get_minimal_id")

        return min(
            self.__response['content']['statuses'] if self.__order_is_search
            else self.__response['content'],
            key=lambda i: i['id']
            )['id'] - 1

    def send_search(self, url):
        if not isinstance(url, basestring):
            raise Exception("Twitter - send_search")

        endpoint = self._base_url + (self._search_url if self.__order_is_search else self._user_url)

        r = requests.get(endpoint + url, auth=self.__oauth, proxies={"https": self.__proxy})

        self.__response['meta'] = r.headers

        Status(r.status_code)

        self.__response['content'] = r.json()

        # update statistics
        seen_tweets = self.get_amount_of_tweets()

        # call callback if available
        if self.__callback:
            self.__callback(self)

        # leading ? does not work with parse_qs()
        if url[0] == '?':
            url = url[1:]
        given_count = int(parse_qs(url)['count'][0])

        # Search API does have valid count values
        if self.__order_is_search and seen_tweets == given_count:
            self.__next_max_id = self.get_minimal_id()

        # Timelines doesn't have valid count values
        elif (not self.__order_is_search and
              len(self.__response['content']) > 0):
            self.__next_max_id = self.get_minimal_id()

		# Less Tweets
        else:
            self.__next_max_id = None

        return self.__response['meta'], self.__response['content']

    def search_tweets(self, tweet):
        if isinstance(tweet, Timeline):
            self.__order_is_search = False
        elif isinstance(tweet, Search):
            self.__order_is_search = True
        else:
            raise Exception("Twitter - search_tweets")

        self._start_url = tweet.create_search_url()
        self.send_search(self._start_url)
        return self.__response

    def search_next_results(self):
        if not self.__next_max_id:
            raise Exception("Twitter - search_next_results")

        self.send_search(
            "%s&max_id=%i" % (self._start_url, self.__next_max_id)
        )
        return True

    def get_metadata(self):
        if not self.__response:
            raise Exception("Twitter - get_metadata")
        return self.__response['meta']

    def get_tweets(self):
        if not self.__response:
            raise Exception("Twitter - get_tweets")
        return self.__response['content']

    def get_amount_of_tweets(self):
        if not self.__response:
            raise Exception("Twitter - get_amount_of_tweets")

        return (len(self.__response['content']['statuses'])
                if self.__order_is_search
                else len(self.__response['content']))

    # Iteration
    def __iter__(self):
        self.__next_tweet = 0
        return self

    def next(self):
        return self.__next__()

    def __next__(self):
        if not self.__response:
            raise Exception("Twitter - __next__")

        if self.__next_tweet < self.get_amount_of_tweets():
            self.__next_tweet += 1
            if self.__order_is_search:
                return (self.__response['content']
                        ['statuses'][self.__next_tweet-1])
            else:
                return self.__response['content'][self.__next_tweet-1]

        try:
            self.search_next_results()
        except Exception:
            raise StopIteration

        if self.get_amount_of_tweets() != 0:
            self.__next_tweet = 1
            if self.__order_is_search:
                return (self.__response['content']
                        ['statuses'][self.__next_tweet-1])
            else:
                return self.__response['content'][self.__next_tweet-1]
        raise StopIteration
