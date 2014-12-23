from unittest import TestCase

from replayer.url_filter import URLFilter
from replayer.config_constants import ConfigConstants
from replayer.log_constants import LogConstants


class TestURLFilter(TestCase):
    def test_proceed_empty_filter(self):
        url_filter = URLFilter({})
        request_data = {}
        self.assertTrue(url_filter.proceed(request_data))

    def test_proceed_filter_method_pos(self):
        url_filter = URLFilter({ConfigConstants.METHODS: ['GET']})
        request_data = {LogConstants.REQUESTLINE: 'GET http://www.google.de/'}
        self.assertTrue(url_filter.proceed(request_data))

    def test_proceed_filter_method_neg(self):
        url_filter = URLFilter({ConfigConstants.METHODS: ['GET']})
        request_data = {LogConstants.REQUESTLINE: 'POST http://www.google.de/'}
        self.assertFalse(url_filter.proceed(request_data))

    def test_proceed_filter_status_pos(self):
        url_filter = URLFilter({ConfigConstants.STATUS: ['200']})
        request_data = {LogConstants.STATUSCODE: '200'}
        self.assertTrue(url_filter.proceed(request_data))

    def test_proceed_filter_status_neg(self):
        url_filter = URLFilter({ConfigConstants.STATUS: ['200']})
        request_data = {LogConstants.STATUSCODE: '404'}
        self.assertFalse(url_filter.proceed(request_data))