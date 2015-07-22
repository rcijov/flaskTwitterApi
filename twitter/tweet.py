# -*- coding: utf-8 -*-

from .exception import Exception


class Tweet(object):

    arguments = {}

    def set_since_id(self, id):
        if not isinstance(id, (int, long)):
            raise Exception("Tweet - set_since_id")

        if id > 0:
            self.arguments.update({'since_id': '%s' % twid})
        else:
            raise Exception("Tweet - set_since_id")

    def set_max_id(self, id):
        if not isinstance(id, (int, long)):
            raise Exception("Tweet - set_since_id")

        if id > 0:
            self.arguments.update({'max_id': '%s' % id})
        else:
            raise Exception("Tweet - set_max_id")

    def set_count(self, count):
        if isinstance(count, int) and count > 0 and count <= 100:
		            self.arguments.update({'count': '%s' % count})
        else:
            raise Exception("Tweet - set_count")

    def set_include_entities(self, include):
        if not isinstance(include, bool):
            raise Exception("Tweet - set_include_entities")
        self.arguments.update(
            {'include_entities': 'true' if include else 'false'}
        )


