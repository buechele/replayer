import logging
from time import sleep
from multiprocessing import Process, Event
from Queue import Empty

import requests

from inspector import Inspector


class HTTPWorker(Process):
    def __init__(self, name, headers, request_queue, url_filter, url_builder, result_queue, pause_time=0):
        Process.__init__(self, name=name)
        self.__headers = headers
        self.__request_queue = request_queue
        self.__url_filter = url_filter
        self.__url_builder = url_builder
        self.__pause_time = pause_time
        self.__exit = Event()
        self.__killed = Event()
        self.__result_queue = result_queue
        self.inspector = Inspector()

    def __request(self, data):
        url = self.__url_builder.build(data)
        try:
            response = requests.get(url, headers=self.__headers)
        except requests.RequestException as e:
            self.inspector.inspect_fail(self.name, url, str(e.message))
        else:
            self.inspector.inspect_succeed(self.name, url, data, response)

    def run(self):
        logging.debug('[%s] Starting worker', self.name)
        while (not self.__killed.is_set()) and (not self.__exit.is_set() or (not self.__request_queue.empty())):
            try:
                data = self.__request_queue.get(True, 0.5)
                if self.__url_filter.proceed(data):
                    self.__request(data)
            except Empty:
                logging.debug('[%s] Queue is empty', self.name)
            except IOError as e:
                logging.error(e.message)
            else:
                sleep(self.__pause_time / 1000.0)

        self.__result_queue.put(self.inspector)
        logging.debug('[%s] Stopping worker ', self.name)

    def exit(self):
        self.__exit.set()

    def kill(self):
        self.__killed.set()