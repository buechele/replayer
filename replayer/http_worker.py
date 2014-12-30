import Queue
import logging
import threading

import requests
from inspector import Inspector


class HTTPWorker(threading.Thread):
    def __init__(self, thread_id, headers, request_queue, url_filter, url_builder):
        threading.Thread.__init__(self)
        self.__thread_id = thread_id
        self.__headers = headers
        self.__request_queue = request_queue
        self.__url_filter = url_filter
        self.__url_builder = url_builder
        self.__do_work = True
        self.__killed = False
        self.__inspector = Inspector()

    def __request(self, data):
        url = self.__url_builder.build(data)
        try:
            response = requests.get(url, headers=self.__headers)
        except requests.RequestException as e:
            self.__inspector.inspect_fail(self.__thread_id, url, str(e.message))
        else:
            self.__inspector.inspect_succeed(self.__thread_id, url, data, response)

    def run(self):
        logging.debug('[Thread %i] Starting thread', self.__thread_id)
        while (not self.__killed) and (self.__do_work or (not self.__request_queue.empty())):
            try:
                data = self.__request_queue.get(True, 1)
                if self.__url_filter.proceed(data):
                    self.__request(data)
            except Queue.Empty:
                logging.debug('[Thread %i] Queue is empty', self.__thread_id)
            except IOError as e:
                logging.error(e.message)
        logging.debug('[Thread %i] Stopping thread ', self.__thread_id)

    def get_inspector(self):
        return self.__inspector

    def stop(self):
        self.__do_work = False

    def kill(self):
        self.__killed = True