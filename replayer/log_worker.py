import logging
from threading import Thread
from Queue import Full

import apachelog


class LogWorker(Thread):
    def __init__(self, log_format, log_file, url_queue, kill_event):
        Thread.__init__(self, name='Log Reader')
        self.__kill_event = kill_event
        self.__parser = apachelog.parser(log_format)
        self.__log_file = log_file
        self.__url_queue = url_queue

    def __queue_data(self, data):
        while not self.__kill_event.is_set():
            try:
                self.__url_queue.put(data, True, 1)
            except Full:
                logging.error('Queue is full')
            else:
                break

    def _process_data(self, data):
        return data

    def run(self):
        for line in open(self.__log_file):
            if self.__kill_event.is_set():
                break

            try:
                data = self.__parser.parse(line)
            except apachelog.ApacheLogParserError:
                logging.error('[%s] Unable to parse line %s', self.name, line)
            else:
                data = self._process_data(data)
                if data:
                    self.__queue_data(data)

        logging.debug('[%s] Worker finished', self.name)
