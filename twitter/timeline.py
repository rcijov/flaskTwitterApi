# -*- coding: utf-8 -*-

import datetime
from .exception import Exception
from .tweet import Tweet

from urlparse import parse_qs
from urllib import quote_plus, unquote


class Timeline(Tweet):

    _max_count = 20

    def __init__(self, user):

        self.arguments.update({'count': '%s' % self._max_count})
        self.set_include_rts(True)
        self.set_exclude_replies(False)
        self.url = ''

        if isinstance(user, (int, long)):
            self.arguments.update({'user_id': '%i' % user})
        elif isinstance(user, basestring):
            self.arguments.update({'screen_name': user})
        else:
            raise Exception("Timeline - __init__")
				
    def set_trim_user(self, trim):
        if not isinstance(trim, bool):
            raise Exception("Timeline - set_trim_user")
        self.arguments.update({'trim_user': 'true' if trim else 'false'})

    def set_include_rts(self, rts):
        if not isinstance(rts, bool):
            raise Exception("Timeline - set_include_rts")
        self.arguments.update({'include_rts': 'true' if rts else 'false'})

    def set_exclude_replies(self, exclude):
        if not isinstance(exclude, bool):
            raise Exception("Timeline - set_exclude_replies")
        self.arguments.update({'exclude_replies': 'true' if exclude else 'false'})

    def set_contributor_details(self, contdetails):
        if not isinstance(contdetails, bool):
            raise Exception("Timeline - set_contributor_details")
        self.arguments.update({'contributor_details': 'true' if contdetails else 'false'})

    def create_search_url(self):
        url = '?'
        for key, value in self.arguments.items():
            url += '%s=%s&' % (quote_plus(key), quote_plus(value))
        self.url = url[:-1]
        return self.url

    def set_search_url(self, url):
        if url[0] == '?':
            url = url[1:]
        self.arguments = {}
        for key, value in parse_qs(url).items():
            self.arguments.update({key: unquote(value[0])})

