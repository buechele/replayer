import datetime
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
        self.__elapsed_time = datetime.timedelta()

    def __add__(self, other):
        self.__count += other.__count
        self.__failed += other.__failed
        self.__status_match += other.__status_match
        self.__length_match += other.__length_match
        self.__size += other.__size
        self.__elapsed_time += other.__elapsed_time
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
        result += 'Size matched:\t\t' + str(self.__length_match) + ' from ' + str(self.__count) + os.linesep

        req_count = self.__count - self.__failed
        avg_time = (self.__elapsed_time.total_seconds() * 1000) / req_count
        result += 'Average time:\t\t' + str(avg_time) + 'ms'

        return result

    def inspect_fail(self, thread_name, url, reason):
        self.__count += 1
        self.__failed += 1

        logging.error('[%s] Request %s failed with reason %s', thread_name, url, str(reason))

    def inspect_succeed(self, thread_name, url, log_data, response, elapsed_time):
        self.__count += 1

        code = str(response.status_code)
        if code == log_data[LogConstants.STATUSCODE]:
            self.__status_match += 1

        content = response.text
        length = len(content)
        self.__size += length
        if str(length) == log_data[LogConstants.BYTES]:
            self.__length_match += 1

        self.__elapsed_time += elapsed_time

        logging.debug('[%s] URL: %s Status: %s Length: %i', thread_name, url, code, length)