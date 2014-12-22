import Queue
import urllib2
import logging
import threading

from inspector import Inspector

class HTTPWorker(threading.Thread):
    def __init__(self, thread_id, headers, request_queue, url_filter, url_builder):
        threading.Thread.__init__(self)
        self.__thread_id = thread_id
        self.__opener = urllib2.build_opener()
        self.__opener.addheaders = headers
        self.__request_queue = request_queue
        self.__url_filter = url_filter
        self.__url_builder = url_builder
        self.__do_work = True
        self.__inspector = Inspector()

    def run(self):
        logging.info('Start thread ' + str(self.__thread_id))
        while self.__do_work or (not self.__request_queue.empty()):
            try:
                data = self.__request_queue.get(True, 1)
                if self.__url_filter.proceed(data):
                    url = self.__url_builder.build(data)
                    response = self.__opener.open(url)
                    self.__inspector.compare(url, data, response)
                    response.close()
            except Queue.Empty:
                logging.info('Queue is empty for thread ' + str(self.__thread_id))
        logging.info('Stop thread ' + str(self.__thread_id))

    def get_inspector(self):
        return self.__inspector

    def stop(self):
        self.__do_work = False