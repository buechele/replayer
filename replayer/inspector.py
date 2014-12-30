import logging
import os

from hurry.filesize import size

from log_constants import LogConstants


class Inspector(object):
    def __init__(self):
        self.__count = 0
        self.__failed = 0
        self.__status_match = 0
        self.__length_match = 0
        self.__size = 0

    def __add__(self, other):
        self.__count += other.__count
        self.__failed += other.__failed
        self.__status_match += other.__status_match
        self.__length_match += other.__length_match
        self.__size += other.__size
        return self

    def __str__(self):
        result = 'Requests:\t\t' + str(self.__count) + os.linesep
        result += os.linesep

        failed_perc = 0
        if self.__count > 0:
            failed_perc = (self.__failed * 100) / self.__count
        result += 'Failed requests:\t' + str(failed_perc) + '% (' + str(self.__failed) + ' from ' + str(
            self.__count) + ')' + os.linesep

        status_perc = 0
        if self.__count > 0:
            status_perc = (self.__status_match * 100) / self.__count
        result += 'Status code matched:\t' + str(status_perc) + '% (' + str(
            self.__status_match) + ' from ' + str(self.__count) + ')' + os.linesep

        result += 'Content transferred:\t' + size(self.__size) + ' (' + str(self.__size) + ' bytes)' + os.linesep
        result += 'Size matched:\t\t' + str(self.__length_match) + ' from ' + str(self.__count)

        return result

    def inspect_fail(self, thread_id, url, reason):
        self.__count += 1
        self.__failed += 1

        logging.error('[Thread %i] Request %s failed with reason %s', thread_id, url, str(reason))

    def inspect_succeed(self, thread_id, url, log_data, response):
        self.__count += 1

        code = str(response.status_code)
        if code == log_data[LogConstants.STATUSCODE]:
            self.__status_match += 1

        content = response.text
        length = len(content)
        self.__size += length
        if str(length) == log_data[LogConstants.BYTES]:
            self.__length_match += 1

        logging.debug('[Thread %i] URL: %s Status: %s Length: %i', thread_id, url, code, length)