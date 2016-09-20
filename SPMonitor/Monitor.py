from __future__ import division, print_function
import time
import datetime
from pytz import timezone
import threading

from ScientificProjects.Client import Client
from ScientificProjects.Entities.Log import LogCategory, Log
from ScientificProjects.Entities.Project import Project
from ScientificProjects.Entities.Session import Session
from ScientificProjects.Entities.User import User

class ClientThread(threading.Thread):

    def __init__(self, config_file_name, log_treeview):
        self.start_datetime = datetime.datetime.utcnow()
        self.last_log_id = 0
        self.config_file_name = config_file_name
        self.log_treeview = log_treeview
        try:
            self.client = Client(config_file_name=self.config_file_name)
        except (ValueError, IOError):
            print('Config file error catched')
            raise ValueError('Error in config file')
        super(ClientThread, self).__init__()
        self.stop_request = threading.Event()

        self.std_offset = datetime.timedelta(seconds=-time.timezone)
        if time.daylight:
            self.dst_offset = datetime.timedelta(seconds=-time.altzone)
        else:
            self.dst_offset = self.std_offset

    def run(self):
        time.sleep(2)
        self.client.user_manager.sign_in('john_smith', 'secret_password')
        self.client.user_manager.sign_out()
        while not self.stop_request.isSet():
            q = self.client.session.query(Log).filter(Log.created > self.start_datetime).\
                filter(Log.id > self.last_log_id)
            results = q.all()
            for record in results:
                if record.id > self.last_log_id:
                    self.last_log_id = record.id
                date = record.created.replace(tzinfo=timezone('UTC')) + self.dst_offset
                date = date.strftime('%Y-%m-%d %H:%M:%S')
                if record.project:
                    project = record.project.name
                else:
                    project = ''
                self.log_treeview.add_record((date, record.category.category,
                                              record.session.user.login, project, record.record))
            time.sleep(2)
        self.client.session.close()
        self.client.engine.dispose()

    def join(self, timeout=None, balancing=True):
        self.stop_request.set()
        super(ClientThread, self).join(timeout)
