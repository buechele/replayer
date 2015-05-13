import logging
from threading import Thread, Event
import time
from datetime import datetime
from Queue import Full

import apachelog


class LogWorker(Thread):
    def __init__(self, log_format, log_file, url_queue, timed):
        Thread.__init__(self, name='Log Reader')
        self.__killed = Event()
        self.__parser = apachelog.parser(log_format)
        self.__log_file = log_file
        self.__url_queue = url_queue
        self.__timed = timed
        self.__first_line = True

    @staticmethod
    def __parse_datetime(data):
        log_time, zone = data.split()
        log_time = log_time.translate(None, "[]")
        return datetime.strptime(log_time, '%d/%b/%Y:%H:%M:%S')

    def __queue_data(self, data):
        while not self.__killed.is_set():
            try:
                self.__url_queue.put(data, True, 1)
            except Full:
                logging.error('Queue is full')
            else:
                break

    def run(self):
        for line in open(self.__log_file):
            if self.__killed.is_set():
                break
            try:
                data = self.__parser.parse(line)
            except:
                logging.error('Unable to parse line %s', line)

            if data:
                if self.__timed:
                    if self.__first_line:
                        self.__first_line = False
                        last_date = int(self.__parse_datetime(data['%t']).strftime('%s'))
                    else:
                        current_date = int(self.__parse_datetime(data['%t']).strftime('%s'))
                        wait_time = current_date - last_date
                        if wait_time > 0:
                            last_date = current_date
                            time.sleep(wait_time)

                self.__queue_data(data)

        logging.debug('[%s] Worker finished', self.name)
        
    def kill(self):
        self.__killed.set()