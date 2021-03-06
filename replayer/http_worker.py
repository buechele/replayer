import logging
from time import sleep
import datetime
from multiprocessing import Process, Event
from Queue import Empty

import requests

from inspector import Inspector
from block_cookie_policy import BlockCookiePolicy


class HTTPWorker(Process):
    def __init__(self, name, headers, request_queue, url_filter, url_builder, result_queue, pause_time=0,
                 allow_cookies=True):
        Process.__init__(self, name=name)
        self.__kill_event = None
        self.__request_queue = request_queue
        self.__url_filter = url_filter
        self.__url_builder = url_builder
        self.__pause_time = pause_time
        self.__exit = Event()
        self.__result_queue = result_queue
        self.inspector = Inspector()
        self.__session = requests.Session()
        self.__session.headers = headers
        if not allow_cookies:
            self.__session.cookies.set_policy(BlockCookiePolicy())

    @property
    def kill_event(self):
        return self.__kill_event

    @kill_event.setter
    def kill_event(self, kill_event):
        self.__kill_event = kill_event

    def __request(self, log_entry):
        url = self.__url_builder.build(log_entry)
        try:
            start_request = datetime.datetime.now()
            response = self.__session.get(url)
            end_request = datetime.datetime.now()
            elapsed_time = end_request - start_request
        except requests.RequestException as e:
            self.inspector.inspect_fail(self.name, url, str(e.message))
        else:
            self.inspector.inspect_succeed(self.name, url, log_entry, response, elapsed_time)

    def run(self):
        logging.debug('[%s] Starting worker', self.name)
        while (self.__kill_event and not self.__kill_event.is_set()) and (not self.__exit.is_set() or (not self.__request_queue.empty())):
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
        logging.debug('[%s] Worker finished', self.name)

    def exit(self):
        self.__exit.set()
