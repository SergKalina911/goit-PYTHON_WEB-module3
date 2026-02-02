"""Event

​Інший примітив синхронізації — це потокобезпечний прапорець класу Event. Клас Event має 
внутрішній прапорець, який можуть встановлювати або скидати інші потоки. Для цього 
використовують метод set, щоб встановити прапор та метод clear для скидання. Методу wait 
класу Event зупиняє роботу потоку до того часу, доки інший потік не встановить прапор 
методом set. Є можливість перевірити, чи встановлено прапор методом is_set.

Таким чином, master може встановити прапорець класу Event, і всі worker потоки продовжать 
роботу тільки після отримання дозволу."""

from threading import Thread, Event
import logging
from time import sleep


def worker(evnt: Event):
    """Worker function that waits for an event to be set before proceeding."""
    logging.debug('Worker ready to work')
    # Wait until the event is set
    evnt.wait()
    logging.debug('The worker can do the work')


def master(evnt: Event):
    """Master function that does some work and then sets the event."""
    logging.debug('Master doing some work')
    sleep(2)
    logging.debug('Informing that workers can do the work')
    # Set the event to allow worker threads to proceed
    evnt.set()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    event = Event()
    master = Thread(name='master', target=master, args=(event, ))

    worker_one = Thread(name='worker_one', target=worker, args=(event, ))
    worker_two = Thread(name='worker_two', target=worker, args=(event,))
    worker_one.start()
    worker_two.start()
    master.start()

    logging.debug('End program')

# Виведення буде таке саме, як і для Condition:

# worker_one Worker ready to work
# worker_two Worker ready to work
# master Master doing some work
# MainThread End program
# master Informing that workers can do the work
# worker_one The worker can do the work
# worker_two The worker can do the work
