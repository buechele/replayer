import time
from datetime import datetime

from log_worker import LogWorker


class TimedLogWorker(LogWorker):
    def __init__(self, log_format, log_file, url_queue, kill_event):
        super(TimedLogWorker, self).__init__(log_format, log_file, url_queue, kill_event)
        self.__first_line = True
        self.__last_date = None

    @staticmethod
    def __parse_datetime(data):
        log_time, zone = data.split()
        log_time = log_time.translate(None, "[]")
        return datetime.strptime(log_time, '%d/%b/%Y:%H:%M:%S')

    def _process_data(self, data):
        if self.__first_line:
            self.__first_line = False
            self.__last_date = int(self.__parse_datetime(data['%t']).strftime('%s'))
        else:
            current_date = int(self.__parse_datetime(data['%t']).strftime('%s'))
            wait_time = current_date - self.__last_date
            if wait_time > 0:
                self.__last_date = current_date
                time.sleep(wait_time)
        return data
