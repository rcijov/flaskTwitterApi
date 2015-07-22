# -*- coding: utf-8 -*-

import datetime
from .exception import Exception
from .tweet import Tweet

from urlparse import parse_qs
from urllib import quote_plus, unquote


class Search(Tweet):
    # Search string
    _question = "?"

    # default value for count should be the maximum value to minimize traffic
    _max_count = 100

    iso_6391 = ('aa', 'ab', 'ae', 'af', 'ak', 'am', 'an', 'ar', 'as',
                'av', 'ay', 'az', 'ba', 'be', 'bg', 'bh', 'bi', 'bm',
                'bn', 'bo', 'br', 'bs', 'ca', 'ce', 'ch', 'co', 'cr',
                'cs', 'cu', 'cv', 'cy', 'da', 'de', 'dv', 'dz', 'ee',
                'el', 'en', 'eo', 'es', 'et', 'eu', 'fa', 'ff', 'fi',
                'fj', 'fo', 'fr', 'fy', 'ga', 'gd', 'gl', 'gn', 'gu',
                'gv', 'ha', 'he', 'hi', 'ho', 'hr', 'ht', 'hu', 'hy',
                'hz', 'ia', 'id', 'ie', 'ig', 'ii', 'ik', 'io', 'is',
                'it', 'iu', 'ja', 'jv', 'ka', 'kg', 'ki', 'kj', 'kk',
                'kl', 'km', 'kn', 'ko', 'kr', 'ks', 'kv', 'kw', 'ky',
                'la', 'lb', 'lg', 'li', 'ln', 'lo', 'lt', 'lu', 'lv',
                'mg', 'mh', 'mi', 'mk', 'ml', 'mn', 'mr', 'ms', 'mt',
                'my', 'na', 'nb', 'nd', 'ne', 'ng', 'nl', 'nn', 'no',
                'nr', 'nv', 'ny', 'oc', 'oj', 'om', 'or', 'os', 'pa',
                'pi', 'pl', 'ps', 'pt', 'qu', 'rm', 'rn', 'ro', 'ru',
                'rw', 'sa', 'sc', 'sd', 'se', 'sg', 'si', 'sk', 'sl',
                'sm', 'sn', 'so', 'sq', 'sr', 'ss', 'st', 'su', 'sv',
                'sw', 'ta', 'te', 'tg', 'th', 'ti', 'tk', 'tl', 'tn',
		'to', 'tr', 'ts', 'tt', 'tw', 'ty', 'ug', 'uk', 'ur',
                'uz', 've', 'vi', 'vo', 'wa', 'wo', 'xh', 'yi', 'yo',
                'za', 'zh', 'zu')

    def __init__(self):
        self.arguments = {'count': '%s' % self._max_count}
        self.searchterms = []
        self.url = ''

    def add_keyword(self, word, or_operator=False):
        if isinstance(word, basestring) and len(word) >= 2:
            self.searchterms.append(word if " " not in word else '"%s"' % word)
        elif isinstance(word, (tuple,list)):
            word = [ (i if " " not in i else '"%s"' % i)  for i in word ]
            self.searchterms += [" OR ".join(word)] if or_operator else word
        else:
            raise Exception("Search - add_keyword")

    def set_keywords(self, words, or_operator=False):
        if not isinstance(words, (tuple,list)):
            raise Exception("Search - set_keywords")
        words = [ (i if " " not in i else '"%s"' % i)  for i in words ]
        self.searchterms = [" OR ".join(words)] if or_operator else words

    def set_search_url(self, url):
        self.__init__()

        if url[0] == '?':
            url = url[1:]

        args = parse_qs(url)

        # urldecode keywords
        for arg in args['q']:
            self.searchterms += [ unquote(i) for i in arg.split(" ") ]
        del args['q']

        for key, value in args.items():
            self.arguments.update({key: unquote(value[0])})
    def create_search_url(self):
        if len(self.searchterms) == 0:
            raise Exception("Search - create_search_url")

        url = '?q='
        url += '+'.join([quote_plus(i) for i in self.searchterms])

        for key, value in self.arguments.items():
            url += '&%s=%s' % (quote_plus(key), (quote_plus(value) if key != 'geocode' else value))
        self.url = url
        return self.url

    def set_language(self, lang):
        if lang in self.iso_6391:
            self.arguments.update({'lang': '%s' % lang})
        else:
            raise Exception("Search - set_language")

    def set_locale(self, lang):
        if lang in self.iso_6391:
            self.arguments.update({'locale': '%s' % lang})
        else:
            raise Exception("Search - set_locale")

    def set_result_type(self, result_type):
        result_type = result_type.lower()
        if result_type in ['mixed', 'recent', 'popular']:
            self.arguments.update({'result_type': '%s' % result_type})
        else:
            raise Exception("Search - set_result_type")

    def set_callback(self, func):
        if isinstance(func, basestring) and func:
            self.arguments.update({'callback': '%s' % func})
        else:
            raise Exception("Search - set_callback")
			
    def set_until(self, date):
        if isinstance(date, datetime.date) and date <= datetime.date.today():
            self.arguments.update({'until': '%s' % date.strftime('%Y-%m-%d')})
        else:
            raise Exception("Search - set_until")

