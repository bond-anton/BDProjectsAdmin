from __future__ import division, print_function
import time
import threading
from ScientificProjects.Client import Client


class ClientThread(threading.Thread):

    def __init__(self, config_file_name):
        self.config_file_name=config_file_name
        try:
            self.client = Client(config_file_name=self.config_file_name)
        except (ValueError, IOError):
            print('Config file error catched')
            raise ValueError('Error in config file')
        super(ClientThread, self).__init__()
        self.stop_request = threading.Event()

    def run(self):
        self.client.user_manager.sign_in('john_smith', 'secret_password')
        self.client.user_manager.sign_out()
        while not self.stop_request.isSet():
            print('Hello')
            time.sleep(2)

    def join(self, timeout=None, balancing=True):
        self.stop_request.set()
        super(ClientThread, self).join(timeout, balancing=balancing)
