import logging
from threading import Thread
from Queue import Full

import apachelog


class LogWorker(Thread):
    def __init__(self, log_format, log_file, log_queue):
        Thread.__init__(self, name='Log Reader')
        self.__kill_event = None
        self.__parser = apachelog.parser(log_format)
        self.__log_file = log_file
        self.__log_queue = log_queue

    @property
    def kill_event(self):
        return self.__kill_event

    @kill_event.setter
    def kill_event(self, kill_event):
        self.__kill_event = kill_event

    def __queue_data(self, log_entry):
        while not self.__kill_event.is_set():
            try:
                self.__log_queue.put(log_entry, True, 1)
            except Full:
                logging.error('Queue is full')
            else:
                break

    def _process_data(self, log_entry):
        return log_entry

    def run(self):
        for line in open(self.__log_file):
            if self.__kill_event and self.__kill_event.is_set():
                break

            try:
                log_entry = self.__parser.parse(line)
            except apachelog.ApacheLogParserError:
                logging.error('[%s] Unable to parse line %s', self.name, line)
            else:
                log_entry = self._process_data(log_entry)
                if log_entry:
                    self.__queue_data(log_entry)

        logging.debug('[%s] Worker finished', self.name)
