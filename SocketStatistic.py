import threading


class SocketStatistic:
    def __init__(self):
        self.thread_lock = threading.Lock()
        self.probe_send = 0
        self.errors = 0
        self.responses = 0

    def add_probe_send(self, value=1):
        self.thread_lock().acquire()
        self.probe_send += value
        self.thread_lock().release()

    def add_errors(self, value=1):
        self.thread_lock().acquire()
        self.errors += value
        self.thread_lock().release()

    def add_responses(self, value=1):
        self.thread_lock().acquire()
        self.responses += value
        self.thread_lock().release()

    def __str__(self):
        return 'probe send:' + str(self.probe_send) + '\n' + 'response errors:' + str(self.errors) + '\n' + \
               'response hits:' + str(self.responses)