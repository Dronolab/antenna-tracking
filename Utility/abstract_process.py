from multiprocessing import Process, Queue
from abc import abstractmethod


class processAbstract:
    def __init__(self):
        self.kill_pill = Queue()
        self._process = None

    def create_new_process(self):
        self._process = Process(target=self.process)
        self._process.daemon = False

    def start(self):
        if not self._process == None:
            self._process.start()
        else:
            self.create_new_process()
            self._process.start()

    def soft_process_stop(self):
        self.kill_pill.put(None)

    def hard_process_stop(self):
        self._process.terminate()

    @abstractmethod
    def process(self):
        raise
