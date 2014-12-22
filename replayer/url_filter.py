from log_constants import LogConstants

class URLFilter(object):
    def __init__(self, codes, methods):
        self.__codes = codes
        self.__methods = methods

    def __check_methods(self, request_data):
        if self.__methods:
            request_line = request_data[LogConstants.REQUESTLINE]
            for method in self.__methods:
                if request_line.startswith(method + ' '):
                    return True
            return False
        else:
            return True

    def __check_codes(self, request_data):
        if self.__codes:
            status_code = request_data[LogConstants.STATUSCODE]
            if status_code in self.__codes:
                return True
            return False
        else:
            return True

    def proceed(self, request_data):
        return self.__check_methods(request_data) and self.__check_codes(request_data)