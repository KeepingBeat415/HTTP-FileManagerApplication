from cmath import log
from locale import THOUSEP
import os, logging, sys, json, re, threading, time


# CURRENT_FILES = {}

class FileManager():
    
    THREAD = threading.Lock()
    
    def __init__(self, verbose, dir_path, accept_type):

        self.dir_path = dir_path
        self.code = ""
        self.content = ""
        self.accept_type = accept_type
        self.status = { "200":"OK", "400":"Bad Request", "401":"Unauthorized", "404":"Not Found"}
        self.disposition = ""
        # Set Logging info
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y/%m/%d %H:%M:%S', stream=sys.stdout, level=logging.DEBUG)
        self.thread = threading.Lock()

    def post_file_handler(self):

            self.code = "200"

            # self.thread.acquire()
            # print(threading.active_count())
            logging.debug(f"File Manager Writing Thread Lock with {self.dir_path}")
            count = 3
            while count:
                time.sleep(1)
                print ("%s %s" % (time.ctime(time.time()), count) + "\n")
                count -= 1

            # self.thread.release()
            logging.debug(f"File Manager Writing Thread Unlock with {self.dir_path}")


file1 = FileManager(True, "data-1", "JSON")
file2 = FileManager(True, "data 2", "JSON")

file1.post_file_handler()
file2.post_file_handler()

