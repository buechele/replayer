import re

from log_constants import LogConstants


class URLBuilder(object):
    def __init__(self, protocol, host, port, regex_list):
        self.__protocol = protocol
        self.__host = host
        self.__port = port
        self.__url_prefix = protocol + '://' + host
        self.__regex_list = regex_list
        self.__fix_host_regex = re.compile('^http://[^/]*')

    def __fix_common_problems(self, request_line):
        if request_line.startswith('http://'):
            return self.__fix_host_regex.sub('', request_line)
        else:
            return request_line

    def build(self, request_data):
        request_line = request_data[LogConstants.REQUESTLINE].split(' ')

        if len(request_line) < 2:
            raise IOError('Ignoring request line %s', request_data[LogConstants.REQUESTLINE])

        # check and fix broken request paths
        request_path = self.__fix_common_problems(request_line[1])

        url = self.__url_prefix + request_path
        for regex_tuple in self.__regex_list:
            url = regex_tuple[0].sub(regex_tuple[1], url)
        return url