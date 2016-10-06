from __future__ import division, print_function
import time
import datetime
from pytz import timezone
import numpy as np
import threading

from ScientificProjects.Client import Client
from ScientificProjects.Entities.Log import Log
from ScientificProjects.Entities.Session import Session


class ClientThread(threading.Thread):

    def __init__(self, config_file_name, log_treeview, sessions_treeview):
        self.start_datetime = datetime.datetime.utcnow()
        self.last_log_id = 0
        self.config_file_name = config_file_name
        self.sessions_treeview = sessions_treeview
        self.log_treeview = log_treeview
        self.categories = ['Information', 'Warning', 'Error']
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
                fg_color = '#000000'
                bg_color = '#FFFFFF'
                if record.category.category == 'Error':
                    bg_color = '#FF0000'
                elif record.category.category == 'Warning':
                    bg_color = '#FFA500'
                self.log_treeview.add_record((date, record.category.category,
                                              record.session.user.login, project, record.record,
                                              fg_color, bg_color, True))
            q = self.client.session.query(Session).filter(Session.active == 1)
            results = q.all()
            treeview_data = []
            for record in results:
                date = record.opened.replace(tzinfo=timezone('UTC')) + self.dst_offset
                date = date.strftime('%Y-%m-%d %H:%M:%S')
                data_row = [record.user.login,
                            [record.token, date, record.host, record.platform, record.python]]
                treeview_data.append(data_row)
            # print(treeview_data)
            self.sessions_treeview.update_treeview(treeview_data)
            time.sleep(0.5)
            if np.random.randint(2) or 1:
                category = self.categories[np.random.randint(len(self.categories))]
                self.client.user_manager.log_manager.log_record('Test %s log message' % category, category=category)
        self.client.user_manager.sign_out()
        self.client.session.close()
        self.client.engine.dispose()

    def join(self, timeout=None, balancing=True):
        self.stop_request.set()
        super(ClientThread, self).join(timeout)
