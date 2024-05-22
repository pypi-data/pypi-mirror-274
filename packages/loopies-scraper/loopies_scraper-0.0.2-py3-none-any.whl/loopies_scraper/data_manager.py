#!/usr/bin/python
import time
from enum import Enum, auto
from multiprocessing import Queue, Value, Lock

class QueueStatus(Enum):
    NOT_STARTED = auto()
    STARTED = auto()
    DONE = auto()

class DataManager:
    def __init__(self) -> None:
        self.queue = Queue()
        self.lock = Lock()
        self.queue_status = Value('i', QueueStatus.NOT_STARTED.value)

    def add_url_to_queue(self, event):
        added = False
        while not added:
            if not self.queue.full():
                try:
                    self.queue.put(event)
                    added = True
                except Exception as e:
                    print('sum aint right, waiting for 5s')
                    print(e)
                    time.sleep(5)
            else:
                print('urls queue is full, waiting for 5s')
                time.sleep(5)

    def ready_to_get_url(self):
        while self.queue_status.value is QueueStatus.NOT_STARTED.value:
            print(f"urls queue status: {self.queue_status.value}, sleeping for 5s...")
            time.sleep(5)

        while self.queue_status.value is QueueStatus.STARTED.value:
            if not self.queue.empty():
                return True
            else:
                print(f"urls queue status: {self.queue_status.value}, urls queue is empty, sleeping for 5s...")
                time.sleep(5)
        
        if self.queue_status.value is QueueStatus.DONE.value:
            if not self.queue.empty():
                return True
        
        return False

def main():
    pass

if __name__ == "__main__":
    main()