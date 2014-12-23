from config_constants import ConfigConstants
from log_constants import LogConstants


class URLFilter(object):
    def __init__(self, allow, logic=True):
        self.__status = allow[ConfigConstants.STATUS] if allow.has_key(ConfigConstants.STATUS) else {}
        self.__methods = allow[ConfigConstants.METHODS] if allow.has_key(ConfigConstants.METHODS) else {}
        self.__logic = logic

    def __check_methods(self, request_data):
        if self.__methods:
            request_line = request_data[LogConstants.REQUESTLINE]
            for method in self.__methods:
                if request_line.startswith(method + ' '):
                    return True
            return False
        else:
            return True

    def __check_status(self, request_data):
        if self.__status:
            status_code = request_data[LogConstants.STATUSCODE]
            if status_code in self.__status:
                return True
            return False
        else:
            return True

    def proceed(self, request_data):
        result = self.__check_methods(request_data) and self.__check_status(request_data)
        if self.__logic:
            return result
        else:
            return not result