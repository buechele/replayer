import logging
import os

from log_constants import LogConstants


class Inspector(object):
    def __init__(self):
        self.__count = 0
        self.__failed = 0
        self.__status_match = 0
        self.__length_match = 0

    def __add__(self, other):
        self.__count += other.__count
        self.__failed += other.__failed
        self.__status_match += other.__status_match
        self.__length_match += other.__length_match
        return self

    def __str__(self):
        result = '[Overview]' + os.linesep
        result += 'Requests: ' + str(self.__count) + os.linesep
        result += '[Responses]' + os.linesep
        
        failed_perc = 0
        if self.__count > 0:
            failed_perc = (self.__failed * 100) / self.__count
        result += 'Failed requests: ' + str(failed_perc) + '% (' + str(self.__failed) + ' from ' + str(self.__count) + ')' + os.linesep
        
        status_perc = 0
        if self.__count > 0:
            status_perc = (self.__status_match * 100) / self.__count
        result += 'Status codes matched: ' + str(status_perc) + '% (' + str(
            self.__status_match) + ' from ' + str(self.__count) + ')' + os.linesep
        
        result += 'Size matched: ' + str(self.__length_match) + ' from ' + str(self.__count)

        return result

    def inspect_fail(self, url, reason):
        self.__count += 1
        self.__failed += 1

        logging.error('Request ' + url + ' failed with reason ' + reason)

    def inspect_status(self, url, log_data, code):
        self.__count += 1

        if code == log_data[LogConstants.STATUSCODE]:
            self.__status_match += 1

        logging.debug('URL: ' + url + ' Status: ' + code)

    def inspect(self, url, log_data, response):
        status = str(response.getcode())
        self.inspect_status(url, log_data, status)

        length = len(response.read())
        if str(length) == log_data[LogConstants.BYTES]:
            self.__length_match += 1