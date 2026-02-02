""" Event2.py - Приклад використання Event для керування виконанням потоку
Виникає закономірне питання, навіщо, якщо результат той самий що і з Condition? Справа 
в тому, що ми можемо керувати виконанням, перезапуском та зупинкою роботи потоків через 
клас Event. Наприклад, у наступному прикладі ми перериваємо виконання потоку, який 
працює в нескінченному циклі та інакше просто ніколи не завершиться."""

from threading import Thread, Event
import logging
from time import sleep


def example_work(event_for_exit: Event):
    """Function that runs in a loop until the event is set."""
    # Run until the event is set
    while True:
        sleep(1)
        logging.debug('Run event work')
# Check if the event is set to exit the loop
        if event_for_exit.is_set():
            break


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    event = Event()
    thread = Thread(target=example_work, args=(event,))
    thread.start()
    # Let the thread run for 5 seconds
    sleep(5)
    # Set the event to signal the thread to exit
    event.set()
    # Wait for the thread to finish
    thread.join()

    logging.debug('End program')

# Виведення:
# Thread-1 Run event work
# Thread-1 Run event work
# Thread-1 Run event work
# Thread-1 Run event work
# MainThread End program
