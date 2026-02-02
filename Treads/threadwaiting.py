"""                                      Очікування виконання потоку

​Коли потрібно в основному застосунку дочекатися виконання потоку, можна скористатися блокуючим 
методом join."""

from threading import Thread
import logging
from time import sleep


def example_work(params):
    sleep(params)
    logging.debug('Wake up!')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    logging.debug('Start program')
    # Створюємо та запускаємо потоки
    threads = []
    for i in range(5):
        thread = Thread(target=example_work, args=(i,))
        thread.start()
        # додаємо потік до списку потоків
        threads.append(thread)

# Очікуємо завершення всіх потоків
    [el.join() for el in threads]

# Або можна так:
#    for thread in threads:
#        thread.join()

    # виводим повідомлення про завершення програми
    logging.debug('End program')

# У консолі ви побачите:

# MainThread Start program
# Thread-1 Wake up!
# Thread-2 Wake up!
# Thread-3 Wake up!
# Thread-4 Wake up!
# Thread-5 Wake up!
# MainThread End program
