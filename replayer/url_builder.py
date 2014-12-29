from log_constants import LogConstants


class URLBuilder(object):
    def __init__(self, protocol, host, port, regex_list):
        self.__protocol = protocol
        self.__host = host
        self.__port = port
        self.__url_prefix = protocol + '://' + host
        self.__regex_list = regex_list

    def build(self, request_data):
        request_line = request_data[LogConstants.REQUESTLINE].split(' ')

        if len(request_line) < 2:
            raise IOError('Problem with request line ' + request_data[LogConstants.REQUESTLINE])

        url = self.__url_prefix + request_line[1]
        for regex_tuple in self.__regex_list:
            url = regex_tuple[0].sub(regex_tuple[1], url)
        return url