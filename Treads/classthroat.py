""" Custom Thread class implementation with logging and sleep functionality."""

from threading import Thread
import logging
import threading
from time import sleep


class MyThread(Thread):
    """ Custom Thread class that accepts args and kwargs. """   
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        # Initialize the base Thread class
        super().__init__(group=group, target=target, name=name, daemon=daemon)
        self.args = args
        self.kwargs = kwargs

    def run(self) -> None:
        # Thread's activity
        logging.debug('Going to sleep for 2 seconds...')
        sleep(2)
        logging.debug('Wake up!')
        logging.debug("args:%s", self.args)
        logging.debug("kwargs:%s", self.kwargs)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    for i in range(5):
        thread = MyThread(args=(f"Count thread - {i}",))
        thread.start()
    print('Usefull message')
# Stop all threads before exiting
    print('Waiting for all threads to complete...', threading.enumerate())
    for thread in threading.enumerate():
        # Avoid joining the main thread
            if thread is not threading.main_thread():
                thread.join()     
# terminate the program
print('All threads have completed. Exiting program.')
exit(0)