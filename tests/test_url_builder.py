from unittest import TestCase

from replayer.url_builder import URLBuilder
from replayer.log_constants import LogConstants


class TestURLBuilder(TestCase):
    def test_proceed_simple_builder(self):
        url_builder = URLBuilder('http', 'www.google.com', '80', [])
        request_data = {LogConstants.REQUEST_LINE: 'GET ' + '/test'}
        build_url = url_builder.build(request_data)
        self.assertEqual('http://www.google.com/test', build_url)