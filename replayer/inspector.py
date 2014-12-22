import logging
import os

from log_constants import LogConstants


class Inspector(object):
    def __init__(self):
        self.__count = 0
        self.__status_match = 0
        self.__size_match = 0

    def __add__(self, other):
        self.__count += other.__count
        self.__status_match += other.__status_match
        self.__size_match += other.__size_match
        return self

    def __str__(self):
        result = '[Overview]' + os.linesep
        result += 'Requests: ' + str(self.__count) + os.linesep
        result += '[Responses matched / mismatched]' + os.linesep
        result += "Status codes: " + str(self.__status_match) + ' / ' + str(
            self.__count - self.__status_match) + os.linesep
        result += "Size: " + str(self.__size_match) + ' / ' + str(self.__count - self.__size_match)

        return result

    def compare(self, url, log_data, response):
        self.__count += 1
        status = response.getcode()
        length = len(response.read())

        if str(status) == log_data[LogConstants.STATUSCODE]:
            self.__status_match += 1

        logging.debug('URL: ' + url + ' Length: ' + str(length) + ' Status: ' + str(status))