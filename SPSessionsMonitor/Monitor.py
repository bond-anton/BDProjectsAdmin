from __future__ import division, print_function
import time
import datetime
from pytz import timezone
import numpy as np
import threading

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty

from ScientificProjects.Client import Client
from ScientificProjects.Entities.User import User
from ScientificProjects.Entities.Session import Session


class ClientThread(threading.Thread):

    def __init__(self, config_file_name, sessions_treeview,
                 logoff_users_queue, logoff_sessions_queue):
        self.start_datetime = datetime.datetime.utcnow()
        self.last_log_id = 0
        self.config_file_name = config_file_name
        self.sessions_treeview = sessions_treeview
        self.logoff_users_queue = logoff_users_queue
        self.logoff_sessions_queue = logoff_sessions_queue
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

            try:
                username = self.logoff_users_queue.get(True, 0.05)
                self.logoff_user(username=username)
            except Empty:
                pass

            try:
                token = self.logoff_sessions_queue.get(True, 0.05)
                self.logoff_session(token=token)
            except Empty:
                pass

            q = self.client.session.query(Session).filter(Session.active == 1)
            results = q.all()
            treeview_data = dict()
            for record in results:
                date = record.opened.replace(tzinfo=timezone('UTC')) + self.dst_offset
                date = date.strftime('%Y-%m-%d %H:%M:%S')
                project = ''
                for opened_project in record.projects_opened:
                    project += opened_project.project.name + '\n'
                data_row = [[record.token, date, record.host, record.platform, record.python, project]]
                if record.user.login in treeview_data:
                    treeview_data[record.user.login] += data_row
                else:
                    treeview_data[record.user.login] = data_row
            self.sessions_treeview.update_treeview(treeview_data)
            time.sleep(2)
            if np.random.randint(2):
                self.client.user_manager.sign_in('john_smith', 'secret_password')
                self.client.user_manager.project_manager.open_project('Super Project')
        self.client.session.close()
        self.client.engine.dispose()

    def join(self, timeout=None, balancing=True):
        self.stop_request.set()
        super(ClientThread, self).join(timeout)

    def logoff_user(self, username):
        q = self.client.session.query(User).filter(User.login == username)
        results = q.all()
        for user in results:
            self.client.user_manager.logoff_user(user=user)

    def logoff_session(self, token):
        q = self.client.session.query(Session).filter(Session.token == token)
        results = q.all()
        for session in results:
            self.client.user_manager.close_session(session=session)
