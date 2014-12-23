from log_constants import LogConstants


class URLBuilder(object):
    def __init__(self, host, regex_list):
        self.__protocol = 'http'
        self.__host = host
        self.__regex_list = regex_list

    def build(self, request_data):
        request_line = request_data[LogConstants.REQUESTLINE].split(' ')
        path = request_line[1]
        url = self.__protocol + '://' + self.__host + path
        for regex_tuple in self.__regex_list:
            url = regex_tuple[0].sub(regex_tuple[1], url)
        return url